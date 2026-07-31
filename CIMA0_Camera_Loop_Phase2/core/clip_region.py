import torch
import open_clip


class ClipRegion:
    """
    OpenCLIP local region structure.

    Role:

        internal dynamical subsystem

    Not:

        classifier
        semantic interpreter
        controller
        global broadcaster


    Only:

        image patch
            |
            v
        visual structure
            |
            v
        local state
    """



    def __init__(
        self,
        weight_path,
        device="cpu"
    ):

        self.device = device


        print(
            "[ClipRegion] loading checkpoint..."
        )


        ckpt = torch.load(
            weight_path,
            map_location="cpu"
        )


        #
        # checkpoint extraction
        #

        if isinstance(
            ckpt,
            dict
        ):

            raw_name = str(
                ckpt.get(
                    "name",
                    ""
                )
            )


            if (
                "roberta-ViT-B-32"
                in raw_name
            ):

                arch = (
                    "roberta-ViT-B-32"
                )

            else:

                arch = (
                    "ViT-B-32"
                )


            if (
                "state_dict"
                in ckpt
            ):

                state_dict = (
                    ckpt["state_dict"]
                )

            elif (
                "model"
                in ckpt
            ):

                state_dict = (
                    ckpt["model"]
                )

            else:

                state_dict = ckpt


        else:

            arch = "ViT-B-32"

            state_dict = ckpt



        print(
            "[ClipRegion] architecture:",
            arch
        )



        #
        # build model
        #

        self.model, _, self.preprocess = (
            open_clip
            .create_model_and_transforms(
                arch,
                pretrained=None
            )
        )



        #
        # remove module prefix
        #

        if any(
            k.startswith("module.")
            for k in state_dict.keys()
        ):

            state_dict = {

                k.replace(
                    "module.",
                    "",
                    1
                ):
                v

                for k, v
                in state_dict.items()

            }



        missing, unexpected = (
            self.model
            .load_state_dict(
                state_dict,
                strict=False
            )
        )


        visual_missing = [

            k for k in missing

            if k.startswith(
                "visual."
            )

        ]


        visual_unexpected = [

            k for k in unexpected

            if k.startswith(
                "visual."
            )

        ]


        print(
            "[ClipRegion] visual missing:",
            len(visual_missing)
        )

        print(
            "[ClipRegion] visual unexpected:",
            len(visual_unexpected)
        )


        #
        # visual tower validation
        #

        self.has_clip = (

            len(visual_missing) == 0

            and

            len(visual_unexpected) == 0

        )


        if self.has_clip:

            print(
                "[ClipRegion] "
                "visual tower ready"
            )

        else:

            print(
                "[ClipRegion] "
                "visual tower mismatch"
            )



        self.model.eval()


        self.model.to(
            self.device
        )


        for p in self.model.parameters():

            p.requires_grad = False



    def encode_local(
        self,
        patch
    ):

        """
        Local visual structure.

        Input:

            preprocessed image patch


        Output:

            local state only

        """


        if (
            patch is None
            or
            not self.has_clip
        ):

            return None



        with torch.no_grad():


            image = (
                patch
                .to(
                    self.device
                )
            )


            z = (
                self.model
                .encode_image(
                    image
                )
            )



        return {

            "clip_norm":
                float(
                    z.norm()
                ),


            "clip_dim":
                int(
                    z.shape[-1]
                )

        }