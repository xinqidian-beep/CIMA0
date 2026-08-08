import torch


WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


checkpoint = torch.load(
    WEIGHT,
    map_location="cpu"
)


state_dict = checkpoint["state_dict"]


print(
    "total keys:",
    len(state_dict)
)


print()


for i, k in enumerate(state_dict.keys()):

    print(k)

    if i > 80:
        break