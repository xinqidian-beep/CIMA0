import torch
import open_clip


class ClipRegion:
    """
    Local visual dynamic region.

    Internal Dynamics component.

    Role:

        state
          |
        local relation
          |
        change


    Not:

        image understanding
        classification
        semantic output
        controller
        global broadcast


    External input:

        changes local visual state tendency
    """

    def __init__(
        self,
        weight_path
    ):

        print("[ClipRegion] loading checkpoint...")


        #
        # checkpoint
        #

        ckpt = torch.load(
            weight_path,
            map_location="cpu"
        )


        if isinstance(
            ckpt,
            dict
        ):

            print(
                "[ClipRegion] ckpt keys:",
                list(
                    ckpt.keys()
                )[:10]
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
        # fixed visual structure
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
            str(k).startswith(
                "module."
            )
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
        # load visual structure
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
        # freeze visual basin
        #

        self.model.eval()


        for p in self.model.parameters():

            p.requires_grad = False



        #
        # internal local state
        #

        self.local_state = None



    def encode(
        self,
        image_tensor
    ):
        """
        Local visual transition.

        No semantic meaning.

        Only feature state.
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



    def update(
        self,
        image_tensor
    ):
        """
        Internal state change.

        External input only changes
        local state tendency.


        No:

            decision
            filtering
            interpretation
        """


        z = self.encode(
            image_tensor
        )


        if z is None:

            return



        z = z.detach()



        if self.local_state is None:

            self.local_state = z


        else:

            #
            # slow local evolution
            #

            self.local_state += (

                0.01 *

                (
                    z
                    -
                    self.local_state
                )

            )



    def state(self):
        """
        Local snapshot.

        Observer may read it.

        No interpretation.
        """


        if self.local_state is None:

            return 0.0



        return float(
            self.local_state.norm()
        )