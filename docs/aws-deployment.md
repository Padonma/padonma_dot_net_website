# AWS deployment runbook

The repository can build and validate the production site without AWS access.
Uploading is a separate, explicit action so local checks and CI never need AWS
credentials.

## Local, credential-free checks

Install the extended edition of Hugo shown in `.hugo-version`, then run:

```sh
scripts/deploy.sh build
```

This uses Hugo's `production` environment, fixes the canonical base URL at
`https://padonma.net/`, treats Hugo warnings as errors, removes OS metadata,
and validates canonical URLs, sitemap URLs, internal links/assets, and required
site files. The generated `public/` directory remains ignored by Git.

## One-time AWS setup (credentials required)

Create these resources before the first upload:

1. A private, versioned S3 bucket with all public access blocked.
2. A CloudFront distribution whose origin is that bucket, using Origin Access
   Control (OAC), not the S3 website endpoint. Grant its distribution ARN
   `s3:GetObject` in the bucket policy.
3. Set `index.html` as the default root object. Configure custom 403 and 404
   responses to return `/404.html` with status 404 if the site supplies that
   page. Do not rewrite every 404 to `/index.html`; this is not an SPA.
4. An ACM certificate in `us-east-1` covering `padonma.net` (and
   `www.padonma.net` if used), attached to CloudFront. Set the alternate domain
   name and redirect HTTP to HTTPS.
5. DNS A/AAAA alias records pointing the hostname at the distribution.

The deploy identity needs `s3:ListBucket`, `s3:GetObject`, `s3:PutObject`, and
`s3:DeleteObject` for this bucket, plus `cloudfront:CreateInvalidation` for this
distribution. It does not need permission to change the bucket or distribution.
Use an AWS CLI profile or short-lived SSO credentials; do not put secrets in
this repository.

Export only deployment identifiers (these are not secrets):

```sh
export AWS_PROFILE=your-profile
export AWS_REGION=your-bucket-region
export S3_BUCKET=your-private-bucket-name
export CLOUDFRONT_DISTRIBUTION_ID=E123EXAMPLE
```

First preview the exact S3 changes:

```sh
scripts/deploy.sh plan
```

Then deploy:

```sh
scripts/deploy.sh deploy
```

The script refuses non-`master` and dirty worktrees by default, verifies the
active AWS identity, uploads non-document assets first, uploads HTML/XML/JSON
last, deletes stale objects, and creates a CloudFront invalidation only after a
successful upload. To deploy an intentionally dirty tree, opt in with
`ALLOW_DIRTY=1`; normal releases should be committed.

## Cache policy and post-deploy verification

- HTML, XML, JSON, and `robots.txt`: `public,max-age=0,must-revalidate`
- CSS, JavaScript, images, fonts, and other assets: `public,max-age=86400`

The one-day asset lifetime is conservative for the first deployment because a
few static filenames are not content-hashed. HTML always revalidates, while
CloudFront can cache assets for a day. Every deployment invalidates `/*`, so a
changed unversioned asset does not remain stale.

After the invalidation completes, verify HTTPS and live response headers:

```sh
scripts/deploy.sh verify
```

The first request may show `x-cache: Miss from cloudfront`; repeat it to confirm
a hit. The command validates the authoritative `Cache-Control` values rather
than requiring a hit, since a newly invalidated distribution should miss.
