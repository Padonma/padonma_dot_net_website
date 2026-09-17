#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly repo_root
readonly expected_hugo_version="$(<"$repo_root/.hugo-version")"
readonly base_url="https://padonma.net/"
readonly documents_cache="public,max-age=0,must-revalidate"
readonly assets_cache="public,max-age=86400"
build_dir="${BUILD_DIR:-$repo_root/public}"
action="${1:-build}"

usage() {
  cat <<'EOF'
Usage: scripts/deploy.sh [build|plan|deploy|verify]

  build   Build and validate production output locally (default; no AWS access).
  plan    Build, validate, verify AWS identity, and show the S3 changes only.
  deploy  Build, validate, upload to S3, then invalidate CloudFront.
  verify  Check live CloudFront URLs and cache headers (no AWS credentials needed).

plan/deploy require S3_BUCKET. deploy also requires CLOUDFRONT_DISTRIBUTION_ID.
Set AWS_PROFILE/AWS_REGION as usual for the AWS CLI. Set ALLOW_DIRTY=1 only when
you intentionally want to deploy uncommitted work.
EOF
}

die() { printf 'error: %s\n' "$*" >&2; exit 1; }
require_command() { command -v "$1" >/dev/null 2>&1 || die "required command not found: $1"; }

check_source() {
  local version branch
  version="$(hugo version | sed -E 's/^hugo v([^+ ]+).*/\1/')"
  [[ "$version" == "$expected_hugo_version" ]] || die "Hugo $expected_hugo_version is required (found $version)"
  branch="$(git -C "$repo_root" branch --show-current)"
  [[ "$branch" == "master" ]] || die "deployments must be built from master (currently $branch)"
  if [[ "${ALLOW_DIRTY:-0}" != "1" ]] && [[ -n "$(git -C "$repo_root" status --porcelain)" ]]; then
    die "working tree is dirty; commit changes or explicitly set ALLOW_DIRTY=1"
  fi
}

build() {
  require_command hugo
  require_command python3
  check_source
  printf 'Building production site with Hugo %s...\n' "$expected_hugo_version"
  hugo --source "$repo_root" --environment production --baseURL "$base_url" \
    --destination "$build_dir" --cleanDestinationDir --gc --minify --panicOnWarning
  find "$build_dir" -type f \( -name '.DS_Store' -o -name 'Thumbs.db' \) -delete
  python3 "$repo_root/scripts/validate-build.py" "$build_dir" --base-url "$base_url"
}

require_aws_target() {
  require_command aws
  [[ -n "${S3_BUCKET:-}" ]] || die "S3_BUCKET is required"
  aws sts get-caller-identity --output json >/dev/null
}

sync_assets() {
  local dry_run=("$@")
  aws s3 sync "$build_dir/" "s3://$S3_BUCKET/" --delete --only-show-errors \
    --exclude '.DS_Store' --cache-control "$assets_cache" "${dry_run[@]}"
  aws s3 cp "$build_dir/" "s3://$S3_BUCKET/" --recursive --only-show-errors \
    --exclude '*' --include '*.html' --include '*.xml' --include '*.json' --include 'robots.txt' \
    --cache-control "$documents_cache" "${dry_run[@]}"
}

verify_live() {
  require_command curl
  local html_headers asset_path asset_headers
  html_headers="$(curl --fail --silent --show-error --location --head "${base_url}")"
  grep -Eiq '^cache-control:.*max-age=0.*must-revalidate' <<<"$html_headers" \
    || die "homepage Cache-Control is not '$documents_cache'"
  asset_path="$(grep -Eo 'href=/css/[^ >]+' "$build_dir/index.html" | head -n 1 | cut -d= -f2)"
  [[ -n "$asset_path" ]] || die "could not find a CSS asset in generated homepage"
  asset_headers="$(curl --fail --silent --show-error --location --head "${base_url%/}${asset_path}")"
  grep -Eiq '^cache-control:.*max-age=86400' <<<"$asset_headers" \
    || die "asset Cache-Control is not '$assets_cache'"
  printf 'Verified live HTTPS responses and cache headers for / and %s\n' "$asset_path"
}

case "$action" in
  build)
    build
    ;;
  plan)
    build
    require_aws_target
    printf 'Dry-run upload to s3://%s (documents: %s; assets: %s)\n' "$S3_BUCKET" "$documents_cache" "$assets_cache"
    sync_assets --dryrun
    ;;
  deploy)
    build
    require_aws_target
    [[ -n "${CLOUDFRONT_DISTRIBUTION_ID:-}" ]] || die "CLOUDFRONT_DISTRIBUTION_ID is required"
    printf 'Uploading to s3://%s...\n' "$S3_BUCKET"
    sync_assets
    invalidation_id="$(aws cloudfront create-invalidation \
      --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths '/*' \
      --query 'Invalidation.Id' --output text)"
    printf 'Uploaded successfully. CloudFront invalidation: %s\n' "$invalidation_id"
    printf 'After it completes, run: scripts/deploy.sh verify\n'
    ;;
  verify)
    [[ -f "$build_dir/index.html" ]] || build
    verify_live
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
