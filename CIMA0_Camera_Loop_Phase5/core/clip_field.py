import numpy as np
import torch
import open_clip

from PIL import Image


class CLIPField:
    """
    CLIP visual organ.

    INPUT:

        {
            bytes,
            shape,
            dtype
        }


    OUTPUT:

        (1,512) float32


    Internal:

        CLIP visual encoder

    """

    def __init__(
        self,
        weight_path,
        device="cpu"
    ):

        self.device = device
        self.visual_field = None


        #
        # create empty model
        #

        model, _, preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained=None
        )


        #
        # load local checkpoint
        #

        checkpoint = torch.load(
            weight_path,
            map_location="cpu"
        )


        state_dict = checkpoint["state_dict"]


        visual_state = {}

        for k, v in state_dict.items():

            if k.startswith(
                "module.visual."
            ):

                name = k.replace(
                    "module.visual.",
                    ""
                )

                visual_state[name] = v


        model.visual.load_state_dict(
            visual_state
        )


        self.model = model.visual


        self.model.eval()


        self.preprocess = preprocess



        #
        # state
        #

        self.input_state = None

        self.output = None

        self.layers = {}

        self.age = 0
        
        self.compute_interval = 30
        self.compute_age = 0 



    #
    # input port
    #

    def receive(
        self,
        raw
    ):

        self.input_state = raw



    #
    # update
    #

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
             
        with torch.no_grad():

            self._capture(
                image
            )



    #
    # bytes -> tensor
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

        img = img[:, :, ::-1]


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



    #
    # internal CLIP
    #

    def _capture(
        self,
        image
    ):
        """
        CLIP visual capture.

        Own:

            visual field
            embedding output

        Output:

            field:
                internal spatial visual feature

            output:
                final CLIP visual vector
        """ 
        visual = self.model   
        #
        # patch embedding field
        #
        # image:
        #   (1,3,224,224)
        #
        # conv1:
        #   (1,768,7,7)
        #
        patch = visual.conv1(
            image
        )
        self.visual_field = (
            patch.detach()
            .cpu()
            .numpy()
        )    
        #
        # normal CLIP visual output
        #
        output = self.model(
            image
        )
        self.output = (
            output.detach()
            .cpu()
            .numpy()
        )
             
        #
        # output ports
        #
        self.layers = {

            "field":
                self.visual_field,


            "output":
                self.output

        }
        
        
   
        
        output = self.model(
            image
        )


        self.output = (
            output.detach()
            .cpu()
            .numpy()
        )


        self.layers = {

            "output":
                self.output

        }



    #
    # output port
    #

    def read(
        self
    ):

        return self.output



    #
    # observer
    #

    def snapshot(
        self
    ):

        return {

            "age":
                self.age,


            "output_shape":

                list(
                    self.output.shape
                )
                if self.output is not None
                else None,


            "layers":

            {

                name:
                    list(value.shape)

                for name,value
                in self.layers.items()

            }

        }