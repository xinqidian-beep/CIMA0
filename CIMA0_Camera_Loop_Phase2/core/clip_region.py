import torch
import open_clip


class ClipRegion:
    """
    Local visual dynamic region.

    Role:

        existing visual structure
        inside internal dynamics

    Not:

        image understanding
        classification
        semantic output
        global broadcast

    State:

        local visual feature state

    Relation:

        input patch
        local visual dynamics

    Change:

        encode_image()
    """

    def __init__(
        self,
        weight_path
    ):

        print("[ClipRegion] loading checkpoint...")


        #
        # load checkpoint
        #

        ckpt = torch.load(
            weight_path,
            map_location="cpu"
        )


        if isinstance(ckpt, dict):

            print(
                "[ClipRegion] ckpt keys:",
                list(ckpt.keys())[:10]
            )


            raw_name = str(
                ckpt.get(
                    "name",
                    ""
                )
            )


            print(
                "[ClipRegion] checkpoint name:",
                raw_name
            )


            if "state_dict" in ckpt:

                sd = ckpt[
                    "state_dict"
                ]

            else:

                sd = ckpt


        else:

            sd = ckpt



        #
        # only visual structure
        #

        arch = "ViT-B-32"


        print(
            "[ClipRegion] architecture:",
            arch
        )


        self.model, _, self.preprocess = (
            open_clip
            .create_model_and_transforms(
                arch,
                pretrained=None
            )
        )


        #
        # remove distributed prefix
        #

        if any(
            str(k).startswith("module.")
            for k in sd.keys()
        ):

            sd = {

                k.replace(
                    "module.",
                    "",
                    1
                ):
                v

                for k, v in sd.items()

            }



        #
        # load
        #

        missing, unexpected = (
            self.model.load_state_dict(
                sd,
                strict=False
            )
        )


        missing = list(
            missing
        )

        unexpected = list(
            unexpected
        )


        print(
            "[ClipRegion] missing:",
            len(missing),
            "unexpected:",
            len(unexpected)
        )


        missing_visual = [

            k for k in missing

            if str(k).startswith(
                "visual."
            )

        ]


        unexpected_visual = [

            k for k in unexpected

            if str(k).startswith(
                "visual."
            )

        ]


        print(
            "[ClipRegion] visual missing:",
            len(missing_visual),
            "| visual unexpected:",
            len(unexpected_visual)
        )


        if missing_visual[:5]:

            print(
                "[ClipRegion] visual missing examples:",
                missing_visual[:5]
            )


        if unexpected_visual[:5]:

            print(
                "[ClipRegion] visual unexpected examples:",
                unexpected_visual[:5]
            )


        #
        # local visual basin available
        #

        self.has_clip = (

            len(missing_visual) == 0

            and

            len(unexpected_visual) == 0

        )


        if self.has_clip:

            print(
                "[ClipRegion] visual structure loaded"
            )

        else:

            print(
                "[ClipRegion] visual structure mismatch"
            )



        #
        # freeze local structure
        #

        self.model.eval()


        for p in self.model.parameters():

            p.requires_grad = False



    def encode(
        self,
        image_tensor
    ):
        """
        Local state transition.

        Input:

            local image patch

        Output:

            local visual state

        No semantic meaning.
        """


        if not self.has_clip:

            return None



        with torch.no_grad():

            z = (
                self.model
                .encode_image(
                    image_tensor
                )
            )


        return z



    def state(
        self,
        image_tensor
    ):
        """
        Return local dynamic state.
        """

        z = self.encode(
            image_tensor
        )


        if z is None:

            return None



        return {

            "feature":

                z,

            "norm":

                float(
                    z.norm()
                )

        }