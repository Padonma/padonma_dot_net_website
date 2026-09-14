"""Generate the narrowest rMQR symbols that hold one binary UUID.

For each requested symbol height and error-correction level, every supported
width is tried in ascending order. The first symbol whose encoder completes is
saved beneath ``bandgrinder/<uuid-hex>/``.
"""

import argparse
import uuid
from pathlib import Path

from rmqrcode import ErrorCorrectionLevel, QRImage, encoder, rMQR
from rmqrcode.encoder.encoder_base import EncoderBase
from rmqrcode.rmqrcode import rMQRVersions


HEIGHTS = (7, 9, 11, 13, 15, 17)
ECC_LEVELS = (("m", ErrorCorrectionLevel.M), ("h", ErrorCorrectionLevel.H))


class RawByteEncoder(EncoderBase):
    """Encode bytes directly, without interpreting them as UTF-8 text."""

    @classmethod
    def mode_indicator(cls):
        return "011"

    @classmethod
    def _encoded_bits(cls, data):
        return "".join(f"{byte:08b}" for byte in data)

    @classmethod
    def length(cls, data, character_count_indicator_length):
        return len(cls.mode_indicator()) + character_count_indicator_length + 8 * len(data)

    @classmethod
    def characters_num(cls, data):
        return len(data)

    @classmethod
    def is_valid_characters(cls, data):
        return True

    @classmethod
    def encode(cls, data, character_count_indicator_length):
        return (
            cls.mode_indicator()
            + f"{len(data):0{character_count_indicator_length}b}"
            + cls._encoded_bits(data)
        )


def version_candidates(height):
    """Return valid rMQR versions for a height, narrowest first."""
    return sorted(
        (name for name in rMQRVersions if name.startswith(f"R{height}x")),
        key=lambda name: int(name.split("x", 1)[1]),
    )


def make_symbol(version, ecc, payload):
    qr = rMQR(version, ecc)
    count_lengths = qr._qr_version["character_count_indicator_length"]
    count_lengths[RawByteEncoder] = count_lengths[encoder.ByteEncoder]
    qr.add_segment(payload, RawByteEncoder)
    qr.make()
    return qr


def smallest_symbol(height, ecc, payload):
    """Try every width experimentally and return the first fitting symbol."""
    failures = []
    for version in version_candidates(height):
        try:
            return version, make_symbol(version, ecc, payload)
        except Exception as error:  # A too-small symbol is expected here.
            failures.append(f"{version}: {error}")
    raise RuntimeError(f"No R{height} symbol fits 16 bytes: {'; '.join(failures)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--uuid",
        dest="uuid_string",
        help="UUID to encode; a UUID4 is generated when omitted.",
    )
    args = parser.parse_args()

    identifier = uuid.UUID(args.uuid_string) if args.uuid_string else uuid.uuid4()
    uuid_hex = identifier.hex
    output_dir = Path(__file__).resolve().parent / uuid_hex
    output_dir.mkdir(exist_ok=True)

    print(f"UUID: {identifier}")
    print(f"Bytes: {identifier.bytes.hex()}")
    for height in HEIGHTS:
        for ecc_suffix, ecc in ECC_LEVELS:
            version, qr = smallest_symbol(height, ecc, identifier.bytes)
            output = output_dir / f"{uuid_hex}_{version.lower()}_{ecc_suffix}.png"
            QRImage(qr, module_size=10).save(output)
            print(f"{output.name}: {version} ECC {ecc_suffix.upper()}")


if __name__ == "__main__":
    main()
