import cv2
import torch
import numpy as np
import open_clip


class CLIPField:

    """
    CIMA0 Phase5_4

    Internal organ.

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

        self.device = device
        
        self.cloud = None
        
        self.previous_cloud = None
        
        self.input_packet = None
        
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

        if packet.tag != "visual":

            return


        self.input_packet = packet
        
        
        #
        # initial attention signal
        #

        self.input_activity = (
            len(packet.data)
            /
            1000000.0
        )
        
    #
    # attention signal
    #

    def activity(
        self
    ):

        if self.input_packet is None:

            return None


        value=self.input_activity
            
        
        return {

            "activity":
                float(value),

            "age": 
                self.age,

            "delta": 
                float(value)

        }



    #
    # compute allocation
    #

    def apply_compute(
        self,
        amount
    ):

        self.compute_budget = amount



    #
    # evolution step
    #

    def step(
        self
    ):
        
        self.age += 1


        #
        # no resource
        #

        if self.compute_budget <= 0:

            return



        if self.input_packet is None:
            
            return



        tensor = self._decode(
            self.input_packet
        )
        
        if tensor is None:
            
            
            return



        self._forward(
            tensor
        )
        

        #
        # consume budget
        #

        self.compute_budget = 0




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

            return



        self.cloud=np.stack(

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
        
        if self.previous_cloud is not None:

            delta = np.mean(
                np.abs(
                    self.cloud - self.previous_cloud
                )
            )

            print(
                "CLOUD DELTA:",
                float(delta)
            )


        self.previous_cloud = self.cloud.copy()
                
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


        if self.cloud is None:

            return None



        return {

            "type":
                "field",

            "representation":
                "cloud",

            "organ":
                "clip",

            "bytes":
                self.cloud.tobytes(),

            "shape":
                self.cloud.shape,

            "dtype":
                "float32",

            "activity":
                self.layer_activity,

            "structure":
                self.structure,

            "timestamp":
                self.age

        }



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