import cv2
import torch
import numpy as np
import open_clip

from core.io.transport.packet import BitPacket


class CLIPField:
    """
    CIMA0 Phase5_7

    Internal organ.

    Responsibility:

        camera packet
            |
            v

        decode

            |
            v

        CLIP visual field

            |
            v

        cloud representation


    Does NOT know:

        Planet

        CloudCollision

        Attention

        Display

        Compute policy


    Provides:

        activity()

        packet()

        collision_projection()

    """



    def __init__(
        self,
        weight_path,
        device="cpu"
    ):


        print(
            "LOAD CLIP:",
            __file__
        )


        self.device = device


        #
        # internal cloud state
        #

        self.cloud = None


        self.previous_cloud = None



        #
        # input cache
        #

        self.input_packet = None


        self.previous_input = None



        #
        # state status
        #

        self.dirty = False

        self.need_initialization = True


        self.age = 0



        #
        # activity
        #

        self.internal_activity = 0.0



        #
        # compute
        #

        self.compute_budget = 0



        #
        # normalization
        #

        self.mean = torch.tensor(
            [
                0.48145466,
                0.4578275,
                0.40821073
            ]
        ).view(
            3,
            1,
            1
        )


        self.std = torch.tensor(
            [
                0.26862954,
                0.26130258,
                0.27577711
            ]
        ).view(
            3,
            1,
            1
        )



        #
        # layer storage
        #

        self.layers = {}

        self.layer_activity = {}

        self.structure = {}



        #
        # load model
        #

        model, _, preprocess = (
            open_clip
            .create_model_and_transforms(
                "ViT-B-32",
                pretrained=None
            )
        )



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


                visual_state[name]=v



        model.visual.load_state_dict(
            visual_state,
            strict=False
        )


        self.model = model.visual


        self.model.eval()


        self.preprocess = preprocess



        self.handles=[]


        self._register_hooks()





    #
    # receive camera packet
    #

    def receive(
        self,
        packet
    ):


        if packet.source != "camera":

            return



        self.input_packet = packet


        self.dirty = True


        self.age = 0





    #
    # activity signal
    #

    def activity(
        self
    ):


        if self.cloud is None:


            if self.need_initialization:


                return {

                    "activity":0.0,

                    "signal":0.0,

                    "changed":False,

                    "source":"clip",

                    "request":
                        "initialize"

                }


            return None




        if self.internal_activity <= 0:

            return None



        return {


            "activity":
                float(
                    self.internal_activity
                ),


            "signal":
                float(
                    self.internal_activity
                ),


            "changed":
                True,


            "source":
                "clip"

        }





    #
    # compute allocation
    #

    def apply_compute(
        self,
        amount
    ):

        self.compute_budget = amount


    def debug_state(self):

        state = {
            "source":"clip",
            "shape":
                None if self.cloud is None
                else self.cloud.shape,
            "activity":self.activity()
        }


        if self.cloud is not None:

            if isinstance(
                self.cloud,
                dict
            ):

                if "field" in self.cloud:

                    state["shape"] = (
                        self.cloud["field"].shape
                    )

                else:

                    state["shape"] = (
                        self.cloud.shape
                    )


        else:

            state["shape"] = None


        return state

    #
    # update cloud
    #

    def step(
        self
    ):


        if self.compute_budget <= 0:

            return


        if not self.dirty:

            return


        if self.input_packet is None:

            return



        tensor = self._decode(
            self.input_packet
        )


        if tensor is None:

            return



        success = self._forward(
            tensor
        )


        if not success:

            return



        self.compute_budget = 0


        self.dirty = False


        self.need_initialization=False



        self.age += 1





    #
    # decode
    #

    def _decode(
        self,
        packet
    ):


        try:


            frame=np.frombuffer(
                packet.data,
                dtype=np.uint8
            )


            frame=frame.reshape(
                packet.shape
            )



            frame=cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )



            frame=cv2.resize(
                frame,
                (224,224)
            )



            tensor=torch.from_numpy(
                frame
            )



            tensor=tensor.permute(
                2,
                0,
                1
            )


            tensor=tensor.float()/255.0



            tensor=(

                tensor

                -

                self.mean

            ) / self.std



            tensor=tensor.unsqueeze(
                0
            )


            return tensor.to(
                self.device
            )


        except Exception:


            return None






    #
    # hooks
    #

    def _register_hooks(
        self
    ):


        blocks=(

            self.model
            .transformer
            .resblocks

        )


        for i,block in enumerate(blocks):


            h=block.register_forward_hook(

                self._make_hook(i)

            )


            self.handles.append(h)





    def _make_hook(
        self,
        index
    ):


        def hook(
            module,
            inputs,
            output
        ):


            data=(

                output
                .detach()
                .cpu()
                .numpy()

            )


            self.layers[index]=data[0]


            self.layer_activity[index]=float(

                np.mean(
                    np.abs(data)
                )

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

        self.layer_activity.clear()



        with torch.no_grad():


            self.model(
                tensor
            )



        if len(self.layers)!=12:


            return False




        new_cloud=np.stack(

            [

                self.layers[i]

                for i in sorted(
                    self.layers.keys()
                )

            ],

            axis=0

        ).astype(
            np.float32
        )



        if self.cloud is None:


            self.internal_activity=1.0


        else:


            self.internal_activity=float(

                np.mean(

                    np.abs(

                        new_cloud

                        -

                        self.cloud

                    )

                )

            )



        print(
            "CLIP CLOUD DELTA:",
            self.internal_activity
        )



        self.previous_cloud=self.cloud


        self.cloud=new_cloud



        self.structure={


            "representation":

                "multilevel_cloud",


            "levels":

                12,


            "tokens":

                50,


            "dimension":

                768

        }



        return True





    #
    # collision interface
    #

    def collision_projection(
        self
    ):
        """
        Export CLIP cloud.

        Read only.

        Used by CloudCollision.

        No modification.
        """


        if self.cloud is None:

            return None



        field=self.cloud

        cloud = {

            "mean":
                float(
                    np.mean(field)
                ),


            "energy":
                float(
                    np.mean(
                        np.abs(field)
                    )
                ),


            "variance":
                float(
                    np.var(field)
                ),


            "density":
                float(
                    np.count_nonzero(field)
                    /
                    field.size
                )
        }

        return {


            "source":

                "clip",



            "representation":
                "clip_cloud",



            "cloud":
                cloud,



            "shape":
                field.shape,
                
                
            
        }







    #
    # output packet
    #

    def packet(
        self
    ):


        if self.cloud is None:

            return None



        field=self.cloud.astype(
            np.float32
        )



        return BitPacket(


            source="clip",


            tag="visual",


            data=field.tobytes(),


            shape=field.shape,


            dtype=str(field.dtype),


            schema="continuous_field",


            meta={

                "representation":

                    "multilevel_cloud"

            }

        )






    #
    # snapshot
    #

    def snapshot(
        self
    ):


        return {


            "age":

                self.age,


            "cloud":

                self.cloud,


            "activity":

                self.layer_activity,


            "structure":

                self.structure

        }





    def close(
        self
    ):


        for h in self.handles:

            h.remove()


        self.handles.clear()