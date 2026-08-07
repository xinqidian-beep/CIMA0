import numpy as np
import torch
import open_clip
from PIL import Image

class CLIPField:
    """
    CLIP visual field.

    Input:
        byte field
        {
            bytes,
            shape,
            dtype
        }

    Output:
        visual internal layers
        final 512 dimension visual state

    Own:
        model
        layer states
        age

    Does NOT:
        classify
        understand image
        generate text
        control modules
    """


    def __init__(
        self,
        weight_path,
        device="cpu"
    ):

        self.device = device


        #
        # create empty CLIP model
        #

        model, _, preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained=None
        )


        #
        # load local checkpoint
        #

        checkpoint = torch.load(
            weight_path,
            map_location="cpu"
        )


        state_dict = checkpoint["state_dict"]


        clean = {}

        for k, v in state_dict.items():

            if k.startswith("module."):
                k = k[7:]

            clean[k] = v


        visual_state = {}

        for k, v in state_dict.items():

            if k.startswith("module.visual."):
                k = k.replace(
                    "module.visual.",
                    ""
                )

                visual_state[k] = v


        model.visual.load_state_dict(
            visual_state
        )


        self.model = model.visual


        self.model.eval()


        self.preprocess = preprocess



        #
        # local state
        #

        self.layers = {}

        self.output = None

        self.input_state = None

        self.age = 0



    def receive(
        self,
        raw
    ):
        """
        Receive external byte stream.
        """

        self.input_state = raw



    def step(
        self
    ):

        self.age += 1


        if self.input_state is None:

            return



        image = self._decode(
            self.input_state
        )


        if image is None:

            return



        with torch.no_grad():

            self.layers = self._capture(
                image
            )



    def _decode(
        self,
        packet
    ):

        try:

            raw = np.frombuffer(
                packet["bytes"],
                dtype=np.uint8
            )


            img = raw.reshape(
                packet["shape"]
            )


        except Exception as e:

            print(
                "decode error:",
                e
            )

            return None



        #
        # BGR -> RGB
        #
        

        img = img[:, :, ::-1]


        img = Image.fromarray(
            img
        )
        
        tensor = self.preprocess(
            img
        )


        return tensor.unsqueeze(
            0
        ).to(
            self.device
        )



    def _capture(
        self,
        image
    ):

        visual = self.model


        result = {}



        #
        # patch embedding
        #

        x = visual.conv1(
            image
        )


        result["patch_embedding"] = (
            x.detach()
            .cpu()
            .numpy()
        )



        #
        # flatten patches
        #

        x = x.reshape(
            x.shape[0],
            x.shape[1],
            -1
        )


        x = x.permute(
            0,
            2,
            1
        )



        #
        # add CLS token
        #

        cls = visual.class_embedding


        cls = cls.to(
            x.dtype
        )


        cls = cls + torch.zeros(
            x.shape[0],
            1,
            x.shape[-1],
            device=x.device,
            dtype=x.dtype
        )


        x = torch.cat(
            [
                cls,
                x
            ],
            dim=1
        )



        #
        # positional embedding
        #

        x = x + visual.positional_embedding



        x = visual.ln_pre(
            x
        )


        x = x.permute(
            1,
            0,
            2
        )



        #
        # transformer
        #

        for index, block in enumerate(
            visual.transformer.resblocks
        ):


            x = block(
                x
            )


            result[
                f"block_{index}"
            ] = (
                x.permute(1,0,2)
                .detach()
                .cpu()
                .numpy()
            )



        #
        # final visual state
        #

        x = x.permute(
            1,
            0,
            2
        )


        x = visual.ln_post(
            x[:,0,:]
        )


        if visual.proj is not None:

            x = x @ visual.proj



        self.output = (
            x.detach()
            .cpu()
            .numpy()
        )


        result["output"] = self.output


        return result



    def snapshot(
        self
    ):

        return {

            "age":
                self.age,


            "output_shape":
                None
                if self.output is None
                else list(self.output.shape),


            "layers":
            {

                name:
                    list(value.shape)

                for name, value
                in self.layers.items()

            }

        }