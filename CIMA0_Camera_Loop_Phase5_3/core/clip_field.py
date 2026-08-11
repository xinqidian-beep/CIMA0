import numpy as np
import torch
import open_clip

from PIL import Image


class CLIPField:
    """
    CIMA0 CLIP visual organ.

    Only one output:

        visual cloud

        shape:
            (12,50,768)


    INPUT:

        {
            bytes,
            shape,
            dtype
        }


    OUTPUT:

        {
            bytes,
            shape,
            dtype
        }


    No:

        field projection
        embedding projection
        semantic interpretation
        display conversion
        control

    """


    def __init__(
        self,
        weight_path,
        device="cpu"
    ):

        self.device = device


        self.input_packet = None


        self.cloud = None


        self.age = 0


        #
        # clock
        #

        self.compute_age = 0

        self.compute_interval = 30



        #
        # create CLIP
        #

        model, _, preprocess = (
            open_clip
            .create_model_and_transforms(
                "ViT-B-32",
                pretrained=None
            )
        )


        #
        # load visual weights
        #

        checkpoint = torch.load(
            weight_path,
            map_location="cpu"
        )


        state_dict = checkpoint["state_dict"]


        visual_state = {}


        for k,v in state_dict.items():

            if k.startswith(
                "module.visual."
            ):

                name = k.replace(
                    "module.visual.",
                    ""
                )

                visual_state[name] = v



        missing, unexpected = (
            model.visual.load_state_dict(
                visual_state,
                strict=False
            )
        )


        print(
            "CLIP visual missing:",
            len(missing)
        )

        print(
            "CLIP visual unexpected:",
            len(unexpected)
        )


        self.model = model.visual

        self.model.eval()


        self.preprocess = preprocess



        #
        # transformer capture
        #

        self.layers = {}

        self.handles = []

        self._register_hooks()



    #
    # receive byte packet
    #

    def receive(
        self,
        packet
    ):

        self.input_packet = packet



    #
    # internal clock
    #

    def step(
        self
    ):

        self.age += 1


        if self.input_packet is None:

            return



        self.compute_age += 1


        if self.compute_age < self.compute_interval:

            return



        self.compute_age = 0



        tensor = self._decode(
            self.input_packet
        )


        if tensor is None:

            return



        self._forward(
            tensor
        )



    #
    # packet decode
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


            image = raw.reshape(
                packet["shape"]
            )


        except Exception as e:

            print(
                "CLIP decode error:",
                e
            )

            return None



        #
        # BGR -> RGB
        #

        image = image[:,:,::-1]


        image = Image.fromarray(
            image
        )


        tensor = self.preprocess(
            image
        )


        return (
            tensor
            .unsqueeze(0)
            .to(self.device)
        )



    #
    # hooks
    #

    def _register_hooks(
        self
    ):

        blocks = (
            self.model
            .transformer
            .resblocks
        )


        for i,block in enumerate(blocks):

            handle = (
                block
                .register_forward_hook(
                    self._make_hook(i)
                )
            )

            self.handles.append(
                handle
            )



    def _make_hook(
        self,
        index
    ):

        def hook(
            module,
            inputs,
            output
        ):

            self.layers[
                index
            ] = (
                output
                .detach()
                .cpu()
                .numpy()
            )


        return hook



    #
    # CLIP forward
    #

    def _forward(
        self,
        tensor
    ):

        self.layers.clear()


        with torch.no_grad():

            self.model(
                tensor
            )


        cloud = []


        for i in sorted(
            self.layers.keys()
        ):

            layer = self.layers[i]


            cloud.append(
                layer[0]
            )



        if len(cloud) == 12:

            self.cloud = np.stack(
                cloud,
                axis=0
            ).astype(
                np.float32
            )


        else:

            self.cloud = None



    #
    # output packet
    #

    def packet(
        self
    ):

        if self.cloud is None:

            return None



        data = (
            self.cloud
            .astype(
                np.float32
            )
        )


        return {

            "bytes":
                data.tobytes(),


            "shape":
                data.shape,


            "dtype":
                "float32",


            "source":
                "clip_visual",


            "timestamp":
                self.age
        }



    #
    # observer snapshot
    #

    def snapshot(
        self
    ):

        return {

            "age":
                self.age,


            "cloud":
                self.cloud

        }