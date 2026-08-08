import numpy as np
import torch
import open_clip

from PIL import Image


class CLIPField:
    """
    CIMA0 CLIP visual organ.

    INPUT:

        {
            bytes,
            shape,
            dtype
        }


    OUTPUT:

        field:
            (7,7)

        embedding:
            (1,512)

        cloud:

            {
                layer0:
                    (50,768)

                ...

                layer11:
                    (50,768)
            }


    No interpretation.

    No semantic decision.

    Only feature emission.
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
        # create model
        #

        model, _, preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained=None
        )



        #
        # load checkpoint
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
            "visual missing:",
            len(missing),
            "unexpected:",
            len(unexpected)
        )



        #
        # visual organ only
        #

        self.model = model.visual


        self.model.eval()


        self.preprocess = preprocess



        #
        # input
        #

        self.input_state = None



        #
        # transformer cloud cache
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




    def receive(
        self,
        raw
    ):

        self.input_state = raw




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


        self._capture(
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




    def _register_layer_hooks(
        self
    ):

        blocks = (
            self.model
            .transformer
            .resblocks
        )


        for i,block in enumerate(blocks):

            handle = block.register_forward_hook(
                self._make_hook(i)
            )

            self.layer_handles.append(
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

            self._layers[
                f"layer{index}"
            ] = (
                output
                .detach()
                .cpu()
                .numpy()
            )


        return hook





    def _capture(
        self,
        image
    ):

        self._layers.clear()



        with torch.no_grad():

            #
            # conv patch field
            #

            x = self.model.conv1(
                image
            )


            self.field = (
                x[0]
                .mean(dim=0)
                .cpu()
                .numpy()
            )



            #
            # final embedding
            #

            output = self.model(
                image
            )


            self.embedding = (
                output
                .cpu()
                .numpy()
            )



        #
        # preserve cloud hierarchy
        #

        self.cloud = {}


        for k,v in self._layers.items():

            self.cloud[k] = (
                v[0]
                .copy()
            )




    def read(
        self
    ):

        if self.cloud is None:
            return None


        chunks = []


        for name in sorted(
            self.cloud.keys()
        ):

            chunks.append(
                self.cloud[name]
                .astype(np.float32)
                .tobytes()
            )


        data = b"".join(
            chunks
        )


        return {

            "bytes":
                data,

            "shape":
                (
                    12,
                    50,
                    768
                ),

            "dtype":
                "float32"
        }




    def display_field(
        self
    ):

        if self.field is None:
            return None


        field = self.field.copy()


        field -= field.min()


        m = field.max()


        if m > 0:

            field /= m


        field = field * 2.0 - 1.0


        return field.astype(
            np.float32
        )




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