import numpy as np
import torch
import open_clip


class CLIPField:
    """
    CLIP visual multi-layer field.

    Input:

        byte field
        {
            bytes,
            shape,
            dtype
        }


    Output:

        visual internal layers


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
        # load CLIP
        #

        model, _, preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained=weight_path
        )


        self.model = model.visual

        self.model.eval()


        self.preprocess = preprocess


        #
        # local cloud state
        #

        self.layers = {}

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

        img = img[:,:,::-1]


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


        result[
            "patch_embedding"
        ] = (
            x.detach()
            .cpu()
            .numpy()
        )



        #
        # token reshape
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
        # transformer layers
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
                x.detach()
                .cpu()
                .numpy()
            )



        return result



    def snapshot(
        self
    ):

        return {

            "age":
                self.age,


            "layers":
            {

                name:
                    list(value.shape)

                for name,value
                in self.layers.items()

            }

        }