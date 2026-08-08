import numpy as np
import torch
import open_clip

from PIL import Image


class CLIPField:
    """
    CLIP visual organ.

    INPUT:

        {
            bytes,
            shape,
            dtype
        }


    OUTPUT:

        (1,512) float32


    Internal:

        CLIP visual encoder

    """

    def __init__(
        self,
        weight_path,
        device="cpu"
    ):

        self.device = device

        #
        # structural visual field
        #
        self.visual_field = None


        #
        # create empty model
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


        visual_state = {}

        for k, v in state_dict.items():

            if k.startswith(
                "module.visual."
            ):

                name = k.replace(
                    "module.visual.",
                    ""
                )

                visual_state[name] = v



        model.visual.load_state_dict(
            visual_state
        )


        #
        # only visual organ
        #

        self.model = model.visual


        self.model.eval()


        self.preprocess = preprocess



        #
        # state
        #

        self.input_state = None


        #
        # CLIP embedding
        #

        self.embedding = None


        #
        # reserved for Phase5.1 layer expansion
        #

        self.layers = {}


        self.age = 0



        #
        # inference clock
        #

        self.compute_interval = 30

        self.compute_age = 0



    #
    # input port
    #

    def receive(
        self,
        raw
    ):

        self.input_state = raw



    #
    # update
    #

    def step(
        self
    ):

        self.age += 1


        if self.input_state is None:

            return



        self.compute_age += 1


        if self.compute_age < self.compute_interval:

            return


        self.compute_age = 0



        image = self._decode(
            self.input_state
        )


        if image is None:

            return



        with torch.no_grad():

            self._capture(
                image
            )



    #
    # bytes -> tensor
    #

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



    #
    # internal CLIP
    #

    def _capture(
        self,
        image
    ):

        with torch.no_grad():


            #
            # patch spatial feature
            #

            x = self.model.conv1(
                image
            )


            #
            # x:
            #
            # (1,768,7,7)
            #

            self.visual_field = (
                x[0]
                .mean(dim=0)
                .cpu()
                .numpy()
            )



            #
            # final CLIP visual embedding
            #

            output = self.model(
                image
            )


            self.embedding = (
                output
                .detach()
                .cpu()
                .numpy()
            )



        #
        # temporary structural cache
        #

        self.layers = {

            "visual_field":
                self.visual_field,


            "embedding":
                self.embedding

        }



    #
    # output port
    #

    def read(
        self
    ):

        return self.embedding



    #
    # DisplayIO interface
    #

    def display_field(
        self
    ):
        """
        Spatial visual field.

        For DisplayIO only.

        Not semantic output.
        """

        if self.visual_field is None:

            return None


        return self.visual_field.copy()



    #
    # observer
    #

    def snapshot(
        self
    ):

        return {

            "age":
                self.age,


            "field":
                self.visual_field,


            "embedding":
                self.embedding

        }