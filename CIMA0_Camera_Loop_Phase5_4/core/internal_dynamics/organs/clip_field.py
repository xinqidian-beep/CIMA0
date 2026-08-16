import numpy as np
import torch
import open_clip

from PIL import Image

print(
    "LOADED:",
    __file__
)

class CLIPField:
    """
    CIMA0 Phase5_4

    Internal cloud organ.


    Input:

        external byte field packet


    Output:

        internal cloud field packet



    Responsibility:

        byte decode

        internal feature formation

        structure preservation

        layer response generation



    Does NOT know:

        Planet

        CloudField

        InternalDynamics

        DisplayIO

        Sampling

        Compute allocation

        Semantic meaning



    Internal structure:

        transformer layers

        token states

        feature dimensions


    """



    def __init__(
        self,
        weight_path,
        device="cpu"
    ):


        self.device = device



        #
        # input packet
        #

        self.input_packet = None



        #
        # cloud output
        #

        self.cloud = None



        #
        # internal age
        #

        self.age = 0



        #
        # compute clock
        #

        self.compute_age = 0

        self.compute_interval = 30



        #
        # transformer states
        #

        self.layers = {}


        #
        # layer activity
        #
        # used for hand raising
        #

        self.layer_activity = {}



        #
        # selected compute budget
        #
        # only receive allocation
        #

        self.compute_budget = 0



        #
        # structure trace
        #

        self.structure = None



        #
        # create CLIP
        #

        model, _, preprocess = (

            open_clip
            .create_model_and_transforms(

                "ViT-B-32",

                pretrained=None

            )

        )



        #
        # load visual weights
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

            "CLIP visual missing:",

            len(missing)

        )


        print(

            "CLIP visual unexpected:",

            len(unexpected)

        )



        self.model = model.visual



        self.model.eval()



        self.preprocess = preprocess



        #
        # transformer capture
        #

        self.handles = []

        self._register_hooks()





    #
    # receive byte packet
    #

    def receive(
        self,
        packet
    ):


        if packet.tag != "visual":

            return

        self.input_packet = packet

        raw = packet.data


        shape = packet.shape


        frame = np.frombuffer(
            raw,
            dtype=np.uint8
        )
        
        frame = frame.reshape(
            shape
        )


        self.buffer = frame
        
        print(
            "CLIP buffer:",
            frame.shape
        )

    #
    # internal clock
    #

    def step(

        self

    ):


        self.age += 1



        if self.input_packet is None:


            return





        self.compute_age += 1



        if self.compute_age < self.compute_interval:


            return



        self.compute_age = 0




        tensor = self._decode(

            self.input_packet

        )



        if tensor is None:


            return



        self._forward(

            tensor
        )    
        print(
            "CLIP forward done"
        )
            

        





    #
    # packet decode
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



            image = raw.reshape(

                packet["shape"]

            )



        except Exception as e:


            print(

                "CLIP decode error:",

                e

            )


            return None





        #
        # preserve external format
        #

        if packet.get(

            "format"

        ) == "BGR":


            image = image[:,:,::-1]





        image = Image.fromarray(

            image

        )



        tensor = self.preprocess(

            image

        )



        return (

            tensor

            .unsqueeze(0)

            .to(self.device)

        )
    #
    # transformer hooks
    #

    def _register_hooks(
        self
    ):


        blocks = (

            self.model

            .transformer

            .resblocks

        )



        for i, block in enumerate(blocks):


            handle = (

                block

                .register_forward_hook(

                    self._make_hook(i)

                )

            )


            self.handles.append(

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


            data = (

                output

                .detach()

                .cpu()

                .numpy()

            )



            #
            # keep complete layer state
            #

            self.layers[index] = data[0]



            #
            # layer raises hand
            #
            # no selection here
            #

            self.layer_activity[index] = float(

                np.mean(

                    np.abs(

                        data

                    )

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





        #
        # keep all candidate layers
        #
        # selection happens outside
        #

        if len(

            self.layers

        ) != 12:


            self.cloud = None


            return





        cloud = []



        for i in sorted(

            self.layers.keys()

        ):


            cloud.append(

                self.layers[i]

            )





        self.cloud = np.stack(

            cloud,

            axis=0
            
            

        ).astype(

            np.float32

        )
        
        print(
            "CLIP cloud shape:",
            self.cloud.shape
        )
        

        #
        # internal structure
        #

        self.structure["cloud"] = {


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
    # compute request
    #
    # CLIPField only raises request
    #

    def compute_request(
        self
    ):
        print(
            "=== ENTER CLIP compute_request ==="
        )
        print(
            "FUNCTION VERSION A"
        )

        print(
            "input_packet:",
            self.input_packet is None
        )

        print(
            "cloud:",
            self.cloud is None
        )
        print(
            "CLIP compute_request called"
        )
        if self.cloud is None:

            print(
                "CLOUD EMPTY - SHOULD NOT RETURN"
            )
        if self.buffer is None:

            return None
            
        if self.layer_activity is None:

            score = 1.0
                                    
            request = {

                "type":"compute_request",

                "source":"clip",
            
                "score":
                    score,
                
                "shape":
                    self.buffer.shape
            }


            print(
                "CLIP request:",
                request
            )


            return request
             
        
    #
    # receive compute allocation
    #

    def apply_compute(

        self,

        allocation

    ):


        if allocation is None:


            return





        if isinstance(

            allocation,

            dict

        ):


            self.compute_budget = (

                allocation.get(

                    "budget",

                    0

                )

            )
            
        print(
            "CLIP budget:",
            self.compute_budget
        )





    #
    # output packet
    #

    def packet(

        self

    ):
        
        print(
            "CLIP cloud:",
            self.cloud is None
        )
        
        if self.cloud is None:


            return None





        data = (

            self.cloud

            .astype(

                np.float32

            )

        )





        return {


            "type":

                "field",



            "representation":

                "cloud",



            "organ":

                "clip",



            "bytes":

                data.tobytes(),



            "shape":

                data.shape,



            "dtype":

                "float32",



            "source":

                "clip",



            "timestamp":

                self.age,



            "structure":

                self.structure,



            "activity":

                self.layer_activity

        }





    #
    # observer snapshot
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





    #
    # cleanup
    #

    def close(

        self

    ):


        for handle in self.handles:


            handle.remove()



        self.handles.clear()