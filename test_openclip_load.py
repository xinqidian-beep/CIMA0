import torch

path = r"C:\CIMA0\models\open_clip_pytorch_model.bin"

print("loading:", path)

data = torch.load(
    path,
    map_location="cpu"
)

print("type:", type(data))

if isinstance(data, dict):
    print("keys:")
    for k in list(data.keys())[:10]:
        print(" ", k)

print("PASS: model file readable")