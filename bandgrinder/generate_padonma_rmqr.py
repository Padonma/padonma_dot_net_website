import os

from rmqrcode import ErrorCorrectionLevel, QRImage, rMQR


TEXT = "Padonma"
SYMBOL = "R9x43"


# R9x43 is the smallest rMQR with height 9 that fits "Padonma" at ECC M.
qr = rMQR(SYMBOL, ErrorCorrectionLevel.M)
qr.add_segment(TEXT)
qr.make()

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "padonma-r9x43.png")

image = QRImage(qr, module_size=10)
image.save(output_path)

print(f"Text:    {TEXT}")
print(f"Symbol:  {SYMBOL} (ECC M)")
print(f"Saved:   {output_path}")
