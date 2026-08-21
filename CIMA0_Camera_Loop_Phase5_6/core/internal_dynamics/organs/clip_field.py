import cv2
import torch
import numpy as np
import open_clip
from core.io.transport.packet import BitPacket

class CLIPField:

    """
    CIMA0 Phase5_4

    Internal organ organ.

    No knowledge:

        Planet
        CloudField
        InternalDynamics
        Display

    Responsible:

        decode
        feature formation
        layer state
        activity request
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
        # state field
        #
        
        self.cloud = None
        
        self.previous_cloud = None

        self.dynamic = False
                
        #
        # measurement cache
        # remove previous_cloud
        #
        
        self.input_packet = None
        
        #
        # state invalidation
        #

        self.dirty = False
        
        #
        # accumulated disturbance
        #

        self.disturbance = 0.0
        
        #
        # external input activity
        #

        self.input_activity = 0.0
        
        #
        # CLIP input normalization
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
                
        self.age = 0


        #
        # compute allocation
        #

        self.compute_budget = 0

        #
        # internal evolution activity
        #

        self.internal_activity = 0.0   

        #
        # internal states
        #

        self.layers = {}

        self.layer_activity = {}

        self.structure = {}
        
        
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

                visual_state[name] = v



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
    # input
    #

    def receive(
        self,
        packet
    ):
        
        if packet.source != "camera":

            return


        self.input_packet = packet
       
        
        #
        # invalidate current state
        #

        self.dirty = True


        #
        # state age reset
        #

        self.age = 0
        
    #
    # attention signal
    #

    def activity(
        self
    ):
        """
        Unified organ signal envelope.

        Lightweight only.

        No visual field.
        No embedding.
        No tensor.

        """
        if self.cloud is None:

            if self.input_packet is not None:

                return {

                    "activity":
                        1.0,

                    "signal":
                        1.0,

                    "changed":
                        True,

                    "source":
                        "clip"

                }
                                
            return None
        
        #
        # debug
        #
        
        print(
            "CLIP ACTIVITY:",
            self.internal_activity
        )
                
        if self.internal_activity <= 0:

            return None

        return {

            "activity":
                self.internal_activity,
                
            "signal":
                self.internal_activity,    
                
            "changed":
                True,


            "source":
                "clip",
            
            "age":
                self.age,
            
        }

    #
    # compute allocation
    #

    def apply_compute(
        self,
        amount
    ):

        self.compute_budget = amount
        

    def update(
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
        
        current = tensor.detach().cpu().numpy()


        if self.previous_input is None:

            self.disturbance = 1.0


        else:

            self.disturbance = float(
                np.mean(
                    np.abs(
                        current -
                        self.previous_input
                    )
                )
            )


        self.previous_input = current
        
        if tensor is None:

            return



        self._forward(
            tensor
        )
        
        success = self._forward(
            tensor
        )


        if not success:

            return
        
        #
        # consume resource
        #

        self.compute_budget = 0



        #
        # state becomes valid 
        #

        self.dirty = False
        
        #
        # accumulated disturbance consumed
        #

        self.disturbance = 0.0

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
            
            tensor=(tensor-self.mean.to(tensor.device))/self.std.to(tensor.device)

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
    # forward
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

            self.cloud=None

            return False



        new_cloud = np.stack(

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
        
        #
        # compare with previous state
        #

        if self.cloud is None:

            self.internal_activity = 1.0


        else:

            self.internal_activity = float(
                np.mean(
                    np.abs(
                        new_cloud -
                        self.cloud
                    ) 
                )
            )


        #
        # replace state
        #

        self.cloud = new_cloud
                
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



    #
    # output
    #

    def packet(
        self
    ):
        
        state = self.snapshot()
        
        if self.cloud is None:

            return None
            
        field = self.cloud

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