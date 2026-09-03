
import cv2
import torch
import numpy as np
import open_clip

from core.io.transport.packet import BitPacket


class CLIPField:
    """
    CIMA0 Phase5_8

    CLIP internal organ.

    Core principle:

        receive
            |
            v
        dirty
            |
            v
        receive compute opportunity
            |
            v
        one forward
            |
            v
        12 internal states
            |
            v
        12 local responses
            |
            v
        select strongest response
            |
            v
        local winner

    CLIPField does NOT know:

        Planet
        PlanetField
        CloudCollision
        Attention
        Sampler
        ComputeSystem
        Display

    Compute ownership:

        ComputeSystem
            |
            | allocation
            v
        CLIPField.compute_budget
            |
            | consume
            v
        one forward

    Important:

        One allocation produces one forward opportunity.

        After the forward is completed, the opportunity
        is consumed.

        If another forward is needed, CLIPField waits
        for another allocation.

    Representation:

        complete cloud:

            (12, 50, 768)

        The 12 layers are preserved.

        A winner is selected only as a local response.
        It does not delete the other 11 layers.
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

        # -------------------------------------------------
        # complete internal cloud
        # -------------------------------------------------

        self.cloud = None

        self.previous_cloud = None

        self.cloud_levels = 12
        self.cloud_tokens = 50
        self.cloud_dimension = 768

        # -------------------------------------------------
        # input
        # -------------------------------------------------

        self.input_packet = None

        self.dirty = False

        # -------------------------------------------------
        # lifecycle
        # -------------------------------------------------

        self.need_initialization = True

        self.age = 0
        self.input_activity = 0.0

        # -------------------------------------------------
        # local response
        # -------------------------------------------------

        self.layer_response = {}
        
        self.winner = None
        self.winner_layer = None
        self.winner_response = 0.0

        self.internal_activity = 0.0

        # -------------------------------------------------
        # compute
        # -------------------------------------------------

        self.compute_budget = 0.0

        # -------------------------------------------------
        # normalization
        # -------------------------------------------------

        self.mean = torch.tensor(
            [
                0.48145466,
                0.4578275,
                0.40821073
            ],
            dtype=torch.float32
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
            ],
            dtype=torch.float32
        ).view(
            3,
            1,
            1
        )

        # -------------------------------------------------
        # forward capture
        #
        # Hooks only keep detached torch tensors.
        #
        # No numpy conversion inside every hook.
        # -------------------------------------------------

        self.layer_activity = {}
        self.layers = {}

        # -------------------------------------------------
        # structure
        # -------------------------------------------------

        self.structure = {}

        # -------------------------------------------------
        # load CLIP
        # -------------------------------------------------

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

        for key, value in state_dict.items():

            if key.startswith(
                "module.visual."
            ):

                name = key.replace(
                    "module.visual.",
                    ""
                )

                visual_state[name] = value

        model.visual.load_state_dict(
            visual_state,
            strict=False
        )

        self.model = model.visual

        self.model.eval()

        self.model.to(
            self.device
        )

        self.preprocess = preprocess

        # -------------------------------------------------
        # hooks
        # -------------------------------------------------

        self.handles = []

        self._register_hooks()

    # =====================================================
    # receive
    # =====================================================

    def receive(
        self,
        packet
    ):

        if packet is None:
            return

        if packet.source != "camera":
            return

        self.input_packet = packet

        #
        # New external observation.
        #

        self.dirty = True

    # =====================================================
    # compute allocation
    # =====================================================

    def apply_compute(
        self,
        amount
    ):

        amount = max(
            float(amount),
            0.0
        )

        self.compute_budget += amount

    # =====================================================
    # activity
    # =====================================================
    
    def activity(
        self
    ):

        if not self.dirty:
            return None

        return {
            "activity":
                float(self.input_activity),

            "signal":
                float(self.input_activity),

            "changed":
                True,

            "source":
                "clip",

            "request":
                "compute",
                
            "candidate":
                self.winner_layer,
            
            "candidate_value":
                float(self.winner_response)
                if self.winner_response is not None
                else 0.0,
            
            "layer":
                self.winner_layer
        }
        
        
    # =====================================================
    # step
    # =====================================================

    def step(
        self
    ):
        """
        One compute opportunity.

        The organ does exactly one forward when it has
        compute permission and new input.

        After forward:

            compute_budget -= 1

        No resource recovery happens here.

        No resource is requested here.

        If another computation is needed, the organ
        becomes dirty and waits for another allocation.
        """

        #
        # no compute
        #

        if self.compute_budget < 1.0:
            return

        #
        # no new input
        #

        if not self.dirty:
            return

        #
        # no input packet
        #

        if self.input_packet is None:
            return

        #
        # consume exactly one compute opportunity
        # for this attempt.
        #

        self.compute_budget -= 1.0

        #
        # decode
        #

        tensor = self._decode(
            self.input_packet
        )

        if tensor is None:
            return

        #
        # one forward
        #

        success = self._forward(
            tensor
        )

        if not success:
            return

        #
        # computation completed.
        #

        self.dirty = False

        self.need_initialization = False

        self.age += 1

    # =====================================================
    # decode
    # =====================================================

    def _decode(
        self,
        packet
    ):

        try:

            frame = np.frombuffer(
                packet.data,
                dtype=np.uint8
            )

            frame = frame.reshape(
                packet.shape
            )

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            frame = cv2.resize(
                frame,
                (224, 224)
            )

            tensor = torch.from_numpy(
                frame
            )

            tensor = tensor.permute(
                2,
                0,
                1
            )

            tensor = tensor.float() / 255.0

            tensor = (
                tensor - self.mean
            ) / self.std

            tensor = tensor.unsqueeze(
                0
            )

            tensor = tensor.to(
                self.device
            )

            return tensor

        except Exception as exc:

            print(
                "CLIP DECODE ERROR:",
                exc
            )

            return None

    # =====================================================
    # hooks
    # =====================================================

    def _register_hooks(
        self
    ):

        blocks = (
            self.model
            .transformer
            .resblocks
        )

        for index, block in enumerate(
            blocks
        ):

            handle = block.register_forward_hook(
                self._make_hook(index)
            )

            self.handles.append(
                handle
            )

    # =====================================================
    # hook
    # =====================================================

    def _make_hook(
        self,
        index
    ):

        def hook(
            module,
            inputs,
            output
        ):

            #
            # Keep tensor detached.
            #
            # Do not perform numpy conversion here.
            #

            self.layers[index] = (
                output.detach()
            )

        return hook

    # =====================================================
    # forward
    # =====================================================

    def _forward(
        self,
        tensor
    ):
        """
        Perform one complete CLIP visual forward.

        Lifecycle:

            compute opportunity
                    |
                    v
            complete CLIP forward
                    |
                    v
            12 layer states
                    |
                    v
            local response for each layer
                    |
                    v
            strongest response
                    |
                    v
            winner_layer
                    |
                    v
            complete cloud becomes current state

        Important:

            The complete cloud is always preserved.

            Winner is only the response coordinate.

            Winner is NOT the collision material.

            CloudCollision will later use the winner to discover
            the associated local cloud.
        """

        #
        # ---------------------------------------------------------
        # 1. clear previous forward capture
        # ---------------------------------------------------------
        #

        self.layers.clear()

        self.layer_activity.clear()


        #
        # ---------------------------------------------------------
        # 2. reset current response
        # ---------------------------------------------------------
        #

        self.winner_layer = None

        self.winner_response = 0.0


        #
        # ---------------------------------------------------------
        # 3. complete CLIP forward
        # ---------------------------------------------------------
        #

        try:

            with torch.no_grad():

                self.model(
                    tensor
                )

        except Exception as exc:

            print(
                "CLIP FORWARD ERROR:",
                exc
            )

            return False


        #
        # ---------------------------------------------------------
        # 4. verify complete transformer state
        # ---------------------------------------------------------
        #

        if len(
            self.layers
        ) != self.cloud_levels:

            print(
                "CLIP LAYER COUNT:",
                len(
                    self.layers
                )
            )

            return False


        #
        # ---------------------------------------------------------
        # 5. collect all layer states
        # ---------------------------------------------------------
        #
        # self.layers contains the complete state captured by hooks.
        # 
        # Do not select winner here.
        #
        # First preserve everything.
        #

        tensors = []


        for index in range(
            self.cloud_levels
        ):

            if index not in self.layers:

                print(
                    "CLIP MISSING LAYER:",
                    index
                )

                return False


            value = self.layers[
                index
            ]


            if not isinstance(
                value,
                torch.Tensor
            ):

                print(
                    "CLIP INVALID LAYER:",
                    index
                )

                return False


            tensors.append(
                value
            )


        #
        # ---------------------------------------------------------
        # 6. build complete cloud
        # ---------------------------------------------------------
        #

        try:

            stacked = torch.stack(
                tensors,
                dim=0
            )

        except Exception as exc:

            print(
                "CLIP CLOUD STACK ERROR:",
                exc
            )

            return False


        #
        # Expected:
        #
        #     (12, 1, 50, 768)
        #
        # or:
        #
        #     (12, 50, 768)
        #

        if stacked.ndim == 4:

            if stacked.shape[1] != 1:

                print(
                    "CLIP UNEXPECTED BATCH:",
                    tuple(
                        stacked.shape
                    )
                )

                return False


            stacked = stacked[
                :,
                0
            ]


        #
        # ---------------------------------------------------------
        # 7. verify complete cloud topology
        # ---------------------------------------------------------
        #

        if stacked.ndim != 3:

            print(
                "CLIP CLOUD SHAPE:",
                tuple(
                    stacked.shape
                )
            )

            return False


        expected_shape = (
            self.cloud_levels,
            self.cloud_tokens,
            self.cloud_dimension
        )


        if tuple(
            stacked.shape
        ) != expected_shape:

            print(
                "CLIP CLOUD UNEXPECTED SHAPE:",
                tuple(
                    stacked.shape
                ),
                "EXPECTED:",
                expected_shape
            )

            return False


        #
        # ---------------------------------------------------------
        # 8. materialize complete cloud
        # ---------------------------------------------------------
        #
        # One transfer only.
        #

        try:

            new_cloud = (
                stacked
                .detach()
                .cpu()
                .numpy()
                .astype(
                    np.float32,
                    copy=True
                )
            )

        except Exception as exc:

            print(
                "CLIP CLOUD BUILD ERROR:",
                exc
            )

            return False


        #
        # ---------------------------------------------------------
        # 9. calculate local response
        # ---------------------------------------------------------
        #
        # This operates on the complete cloud.
        #
        # It does NOT destroy the cloud.
        #

        response_ok = self._local_response(
            new_cloud
        )

        if not response_ok:

            return False


        #
        # ---------------------------------------------------------
        # 11. calculate complete-cloud change
        # ---------------------------------------------------------
        #

        if self.cloud is None:

            self.internal_activity = 1.0

        else:
            
            try:

                delta = np.mean(
                    np.abs(
                        new_cloud
                        -
                        self.cloud
                    )
                )

                self.internal_activity = float(
                    delta
                )

            except Exception as exc:

                print(
                    "CLIP CLOUD DELTA ERROR:",
                    exc
                )

                self.internal_activity = 0.0


        print(
            "CLIP CLOUD DELTA:",
            self.internal_activity
        )


        #
        # ---------------------------------------------------------
        # 12. preserve complete state
        # ---------------------------------------------------------
        #

        self.previous_cloud = self.cloud

        self.cloud = new_cloud


        #
        # ---------------------------------------------------------
        # 13. structure metadata
        # ---------------------------------------------------------
        #

        self.structure = {

            "representation":
                "multilevel_cloud",

            "levels":
                self.cloud_levels,

            "tokens":
                self.cloud_tokens,

            "dimension":
                self.cloud_dimension,

            "winner_layer":
                self.winner_layer,

            "winner_response":
                float(
                    self.winner_response
                )
        }


        #
        # ---------------------------------------------------------
        # 14. diagnostic output
        # ---------------------------------------------------------
        #

        print(
            "CLIP LOCAL RESPONSE:",
            self.layer_activity
        )


        print(
            "CLIP LOCAL WINNER:",
            self.winner_layer
        )


        print(
            "CLIP WINNER RESPONSE:",
            self.winner_response
        )


        print(
            "CLIP CLOUD:",
            self.cloud.shape
        )


        #
        # ---------------------------------------------------------
        # 15. complete
        # ---------------------------------------------------------
        #

        return True

    # =====================================================
    # local response
    # =====================================================

    def _local_response(
        self,
        new_cloud
    ):
        """
        Determine which of the 12 internal states has
        the strongest local response.

        No semantic interpretation is performed.

        For each layer:

            current layer
                    |
                    v
            previous same layer
                    |
                    v
            local difference
                    |
                    v
            mean absolute response

        On first computation:

            the layer's own magnitude becomes its response.

        On subsequent computations:

            response = mean(
                abs(
                    current_layer
                    -
                    previous_layer
                )
            )

        The complete layer responses are preserved.

        Winner is only the strongest response coordinate.
        """

        responses = {}
        
        print(
            "CLIP RESPONSE INPUT:",
            new_cloud.shape,
            None
            if self.cloud is None
            else self.cloud.shape
        )

        #
        # first cloud
        #

        if self.cloud is None:

            for index in range(
                new_cloud.shape[0]
            ):

                value = float(
                    np.mean(
                        np.abs(
                            new_cloud[index]
                        )
                    )
                )

                responses[index] = value

        #
        # subsequent clouds
        #

        else:

            previous = self.cloud

            levels = min(
                new_cloud.shape[0],
                previous.shape[0]
            )

            for index in range(
                levels
            ):

                value = float(
                    np.mean(
                        np.abs(
                            new_cloud[index]
                            -
                            previous[index]
                        )
                    )
                )

                responses[index] = value

        #
        # no response
        #

        if not responses:

            self.layer_activity = {}

            self.winner_layer = None

            self.winner_response = 0.0

            self.internal_activity = 0.0
            
            print(
                "CLIP LOCAL RESPONSE: EMPTY"
            )

            return False
            
        self.layer_activity = responses


        winner = max(
            self.layer_activity,
            key=self.layer_activity.get
        )


        self.winner_layer = int(
            winner
        )

        self.winner_response = float(
            self.layer_activity[
                winner
            ]
        )

        self.internal_activity = (
            self.winner_response
        )


        print(
            "CLIP LOCAL RESPONSE:",
            self.layer_activity
        )

        print(
            "CLIP LOCAL WINNER:",
            self.winner_layer
        )

        return True    
        

    # =====================================================
    # collision projection
    # =====================================================

    def collision_projection(
        self
    ):
        """
        Export the complete CLIP cloud.

        Collision layer is NOT selected here.

        The winner is metadata only.

        CloudCollision receives:

            complete cloud
            layer responses
            winner layer
            structure
        """

        if self.cloud is None:
            return None

        layers = {}

        for key, value in self.layers.items():

            if torch.is_tensor(value):

                layers[key] = (
                    value
                    .detach()
                    .cpu()
                    .numpy()
                    .copy()
                )

            elif isinstance(value, np.ndarray):

                layers[key] = value.copy()

            else:

                layers[key] = value


        return {

            "source":
                "clip",

            "representation":
                "clip_cloud",

            #
            # complete CLIP internal cloud
            #

            "cloud":
                self.cloud.copy(),

            #
            # layer states
            #

            "layers":
                layers,

            #
            # local response of all layers
            #

            "layer_activity":
                dict(
                    self.layer_activity
                ),

            #
            # strongest local response
            #

            "winner":
                self.winner_layer,

            "winner_response":
                float(
                    self.winner_response
                ),

            #
            # structure
            #

            "structure":
                dict(
                    self.structure
                ),

            "shape":
                tuple(
                    self.cloud.shape
                ),

            "dtype":
                str(
                    self.cloud.dtype
                )
        }

    # =====================================================
    # packet
    # =====================================================

    def packet(
        self
    ):

        if self.cloud is None:
            return None

        field = self.cloud.astype(
            np.float32,
            copy=False
        )

        return BitPacket(

            source="clip",

            tag="visual",

            data=field.tobytes(),

            shape=field.shape,

            dtype=str(
                field.dtype
            ),

            schema="continuous_field",

            meta={

                "representation":
                    "multilevel_cloud",

                "winner_layer":
                    self.winner_layer,

                "winner_response":
                    float(
                        self.winner_response
                    )
            }
        )

    # =====================================================
    # snapshot
    # =====================================================

    def snapshot(
        self
    ):

        return {

            "age":
                self.age,

            "cloud":
                None
                if self.cloud is None
                else self.cloud.copy(),

            "activity":
                dict(
                    self.layer_response
                ),

            "winner_layer":
                self.winner_layer,

            "winner_response":
                float(
                    self.winner_response
                ),

            "structure":
                dict(
                    self.structure
                )
        }

    # =====================================================
    # debug
    # =====================================================

    def debug_state(
        self
    ):

        return {

            "source":
                "clip",

            "cloud_shape":
                None
                if self.cloud is None
                else self.cloud.shape,

            "dirty":
                self.dirty,

            "compute_budget":
                self.compute_budget,

            "winner_layer":
                self.winner_layer,

            "winner_response":
                float(
                    self.winner_response
                ),

            "layer_response":
                dict(
                    self.layer_response
                ),

            "age":
                self.age
        }

    # =====================================================
    # close
    # =====================================================

    def close(
        self
    ):

        for handle in self.handles:

            handle.remove()

        self.handles.clear()