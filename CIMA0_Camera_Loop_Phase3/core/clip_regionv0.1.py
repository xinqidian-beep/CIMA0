import torch
import open_clip

import numpy as np
from PIL import Image



class ClipRegion:
    """
    Local visual dynamic region.

    Internal Dynamics component.


    Principle:

        state
          |
        local relation
          |
        change


    Role:

        frozen visual structure
        local visual state evolution


    Not:

        image understanding
        classification
        semantic output
        controller
        selector
    """



    def __init__(
        self,
        weight_path
    ):


        print(
            "[ClipRegion] loading checkpoint..."
        )


        #
        # load checkpoint
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



            print(
                "[ClipRegion] checkpoint name:",
                ckpt.get(
                    "name",
                    ""
                )
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
        # architecture
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

                for k,v in sd.items()

            }




        #
        # load structure
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
        # local dynamic state
        #

        self.local_state = None




    def encode(
        self,
        frame
    ):
        """
        Raw camera frame
        ->
        local visual feature


        No semantic interpretation.
        """



        if not self.has_clip:

            return None



        #
        # numpy camera frame
        #

        if isinstance(
            frame,
            np.ndarray
        ):

            frame = Image.fromarray(
                frame
            )



        #
        # visual tensor
        #

        image_tensor = (
            self.preprocess(
                frame
            )
            .unsqueeze(0)
        )



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
        frame
    ):
        """
        Internal local evolution.


        External input:

            changes state tendency


        Does not:

            control
            classify
            select
        """



        z = self.encode(
            frame
        )


        if z is None:

            return



        z = z.detach()



        if self.local_state is None:


            self.local_state = z



        else:


            #
            # slow state evolution
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
        Raw local state snapshot.

        Observer reads this.
        """



        if self.local_state is None:

            return {

                "active": False,

                "norm": 0.0

            }



        return {


            "active": True,


            "norm":

                float(
                    self.local_state.norm()
                ),


            "shape":

                list(
                    self.local_state.shape
                )

        }