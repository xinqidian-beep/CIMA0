import open_clip
import torch


model_path = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained=None
)


checkpoint = torch.load(
    model_path,
    map_location="cpu"
)


model.load_state_dict(
    checkpoint,
    strict=False
)


print("Model loaded")

print(
    "parameters:",
    sum(
        p.numel()
        for p in model.parameters()
    )
)

print("PASS")