import uuid
import os
from rmqrcode import rMQR, ErrorCorrectionLevel, encoder
from rmqrcode import QRImage
from rmqrcode.encoder.encoder_base import EncoderBase

# Supply your UUID as a string here
UUID_STRING = "97e41923-8681-4f84-a075-dc652cf7d3bc"

# Parse and convert to raw 16 bytes
u = uuid.UUID(UUID_STRING)
uuid_bytes = u.bytes  # 16 raw bytes

# The built-in ByteEncoder calls encode("utf-8"), which inflates bytes > 0x7F
# into multi-byte sequences. We subclass it to encode raw bytes instead.
class RawByteEncoder(EncoderBase):
    @classmethod
    def mode_indicator(cls):
        return "011"

    @classmethod
    def _encoded_bits(cls, s):
        res = ""
        for byte in s:
            res += bin(byte)[2:].zfill(8)
        return res

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
        res = cls.mode_indicator()
        res += bin(len(data))[2:].zfill(character_count_indicator_length)
        res += cls._encoded_bits(data)
        return res


# R7x77 at ECC M: 160 data bits available.
# Byte mode overhead = 3 (mode) + 5 (count indicator for R7x77) = 8 bits.
# 16 bytes * 8 bits = 128 bits. Total = 136 bits. Fits comfortably.
qr = rMQR('R7x77', ErrorCorrectionLevel.M)

# The version table keys character_count_indicator_length by encoder class.
# Register RawByteEncoder with the same indicator length as ByteEncoder.
qr._qr_version["character_count_indicator_length"][RawByteEncoder] = \
    qr._qr_version["character_count_indicator_length"][encoder.ByteEncoder]

qr._segments.append({"data": uuid_bytes, "encoder_class": RawByteEncoder})
qr.make()

# Save PNG in the same directory as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, f"{UUID_STRING}.png")

image = QRImage(qr, module_size=10)
image.save(output_path)

print(f"UUID:    {UUID_STRING}")
print(f"Bytes:   {uuid_bytes.hex()}")
print(f"Symbol:  R7x77 (smallest R7 fitting 16 bytes at ECC M)")
print(f"Saved:   {output_path}")
