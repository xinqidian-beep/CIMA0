import os
import sys
import torch
import open_clip


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    ROOT
)


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



def main():

    print(
        "CIMA0 Phase5.1 CLIP Text Test"
    )


    #
    # create empty full CLIP model
    #

    model, _, _ = open_clip.create_model_and_transforms(
        "ViT-B-32",
        pretrained=None
    )


    #
    # load complete checkpoint
    #

    checkpoint = torch.load(
        CLIP_WEIGHT,
        map_location="cpu"
    )


    state_dict = checkpoint["state_dict"]


    clean_state = {}

    for k, v in state_dict.items():

        name = k

        if name.startswith(
            "module."
        ):

            name = name.replace(
                "module.",
                "",
                1
            )


        clean_state[name] = v



    missing, unexpected = (
        model.load_state_dict(
            clean_state,
            strict=False
        )
    )


    print()

    print(
        "missing:",
        len(missing)
    )

    print(
        "unexpected:",
        len(unexpected)
    )


    model.eval()



    #
    # text encoder test
    #

    tokenizer = open_clip.get_tokenizer(
        "ViT-B-32"
    )


    text = [
        "a photo of a person",
        "a photo of an object",
        "a photo of nature"
    ]


    tokens = tokenizer(
        text
    )


    with torch.no_grad():

        text_features = model.encode_text(
            tokens
        )


        text_features /= (
            text_features.norm(
                dim=-1,
                keepdim=True
            )
        )


    print()

    print(
        "text embedding:"
    )

    print(
        text_features.shape
    )


    print(
        text_features.dtype
    )



if __name__ == "__main__":

    main()