import torch
import open_clip

import numpy as np
from PIL import Image



class ClipRegion:
    """
    Local visual dynamic region.

    Responsibility:

        external bytes / field disturbance
                |
                v
          local projection
                |
                v
          local state evolution


    Does NOT:

        understand camera
        understand image meaning
        classify
        control
        allocate resources


    Own state:

        input_state
        local_state
        age
        response timing
    """



    def __init__(
        self,
        weight_path
    ):

        print(
            "[ClipRegion] loading checkpoint..."
        )


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

                sd = ckpt["state_dict"]

            else:

                sd = ckpt


        else:

            sd = ckpt



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
        # frozen structure
        #

        self.model.eval()


        for p in self.model.parameters():

            p.requires_grad = False



        #
        # local dynamics state
        #

        self.local_state = None


        #
        # external disturbance buffer
        #

        self.input_state = None



        #
        # internal time
        #

        self.age = 0



        #
        # local response period
        #

        self.response_period = 5





    def receive(
        self,
        data
    ):
        """
        External disturbance input.

        Store only.

        No computation.
        No interpretation.
        """

        self.input_state = data





    def step(
        self
    ):
        """
        Local evolution.

        Internal timing decides response.
        """


        self.age += 1



        if self.input_state is None:

            return



        if (
            self.age %
            self.response_period
            != 0
        ):

            return



        z = self.encode(
            self.input_state
        )



        if z is None:

            return



        z = z.detach()



        if self.local_state is None:

            self.local_state = z



        else:

            self.local_state += (
                0.01 *
                (
                    z -
                    self.local_state
                )
            )







    def encode(
        self,
        data
    ):
        """
        External disturbance
        ->
        frozen local structure projection

        No semantic interpretation.
        """

        if not self.has_clip:

            return None



        frame = self._to_frame(
            data
        )


        if frame is None:

            return None



        if isinstance(
            frame,
            np.ndarray
        ):

            if frame.ndim == 2:

                frame = Image.fromarray(
                    frame
                )


            elif (
                frame.ndim == 3
                and frame.shape[-1]
                in (1,3,4)
            ):


                if frame.shape[-1] == 1:

                    frame = Image.fromarray(
                        frame[:, :, 0]
                    )

                else:

                    frame = Image.fromarray(
                        frame
                    )


            else:

                return None



        image_tensor = (
            self.preprocess(frame)
            .unsqueeze(0)
        )



        with torch.no_grad():

            z = self.model.encode_image(
                image_tensor
            )



        return z






    def _to_frame(
        self,
        data
    ):

        if data is None:

            return None



        if isinstance(
            data,
            bytes
        ):

            if len(data) == 0:

                return None


            arr = np.frombuffer(
                data,
                dtype=np.uint8
            )


            if arr.size == 0:

                return None


            side = int(
                np.sqrt(
                    arr.size
                )
            )


            if side <= 0:

                return None



            arr = arr[
                :
                side * side
            ].reshape(
                side,
                side
            )


            return arr





        if isinstance(
            data,
            np.ndarray
        ):


            arr = np.asarray(
                data
            )


            if arr.size == 0:

                return None



            if arr.dtype != np.uint8:

                arr = np.nan_to_num(
                    arr,
                    nan=0.0,
                    posinf=0.0,
                    neginf=0.0
                )


                arr = arr.astype(
                    np.float32
                )


                arr -= np.min(
                    arr
                )


                mx = np.max(
                    arr
                )


                if mx > 0:

                    arr /= mx



                arr = (
                    arr *
                    255.0
                ).clip(
                    0,
                    255
                ).astype(
                    np.uint8
                )



            if arr.ndim == 1:

                arr = arr[None,:]



            return arr





        if isinstance(
            data,
            Image.Image
        ):

            return data





        if isinstance(
            data,
            dict
        ):

            for key in (
                "data",
                "frame",
                "image",
                "field",
                "state",
                "matrix"
            ):

                if key in data:

                    return self._to_frame(
                        data[key]
                    )



        return None







    def state(
        self
    ):
        """
        Read only snapshot.
        """

        if self.local_state is None:


            return {

                "active": False,

                "norm": 0.0,

                "shape": None

            }




        ls = self.local_state.detach()



        return {


            "active": True,


            "norm": float(
                ls.norm()
            ),


            "shape": list(
                ls.shape
            ),


            "mean": float(
                ls.mean()
            ),


            "std": float(
                ls.std()
            ),


            "max": float(
                ls.max()
            ),


            "min": float(
                ls.min()
            )

        }