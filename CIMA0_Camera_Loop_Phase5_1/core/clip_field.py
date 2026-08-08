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

        field
            (7,7)

        embedding
            (1,512)

        cloud
            (600,768)


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
        # output state
        #

        self.field = None

        self.embedding = None

        self.cloud = None



        #
        # create empty model
        #

        model, _, preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained=None
        )



        #
        # load local visual checkpoint
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
        # visual organ only
        #

        self.model = model.visual


        self.model.eval()


        self.preprocess = preprocess



        #
        # input state
        #

        self.input_state = None



        #
        # internal transformer cache
        #

        self._layers = {}

        self.layer_handles = []


        self._register_layer_hooks()



        #
        # clock
        #

        self.age = 0

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
    # transformer hooks
    #

    def _register_layer_hooks(
        self
    ):

        blocks = (
            self.model
            .transformer
            .resblocks
        )


        for i, block in enumerate(blocks):

            handle = block.register_forward_hook(
                self._make_layer_hook(i)
            )


            self.layer_handles.append(
                handle
            )



    def _make_layer_hook(
        self,
        index
    ):


        def hook(
            module,
            inputs,
            output
        ):

            self._layers[
                f"layer{index}"
            ] = (
                output
                .detach()
                .cpu()
                .numpy()
            )


        return hook



    #
    # CLIP computation
    #

    def _capture(
        self,
        image
    ):

        self._layers.clear()



        with torch.no_grad():


            #
            # spatial field
            #

            x = self.model.conv1(
                image
            )


            #
            # (1,768,7,7)
            #

            self.field = (
                x[0]
                .mean(dim=0)
                .cpu()
                .numpy()
            )



            #
            # transformer + projection
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
        # transformer layers -> visual cloud
        #

        cloud = {}


        for layer_name, value in self._layers.items():

            #
            # value:
            #
            # (1,50,768)
            #

            cloud[layer_name] = (
                value[0]
                .copy()
            )


        self.cloud = cloud



    #
    # output port
    #

    def read(
        self
    ):

        if self.cloud is None:

            return None


        buffer = []


        for layer_name in sorted(
            self.cloud.keys()
        ):

            layer = self.cloud[layer_name]


            buffer.append(
                layer.astype(
                    np.float32
                ).tobytes()
            )


        return b"".join(
            buffer
        )



    #
    # DisplayIO interface
    #

    def display_field(
        self
    ):

        if self.field is None:

            return None


        return self.field.copy()



    #
    # observer interface
    #

    def snapshot(
        self
    ):

        return {

            "age":
                self.age,


            "field":
                self.field,


            "embedding":
                self.embedding,


            "cloud":
                self.cloud

        }