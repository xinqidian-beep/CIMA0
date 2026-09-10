
import numpy as np


class DisplayIO:
    """
    CIMA0 Phase5_8

    Pure display port.

    The display port is the final convergence point.

    Internal information streams remain independent
    during evolution.

    At output:

        Planet field
            +
        preserved camera BGR
            |
            v
        final RGB framebuffer

    DisplayIO does NOT:

        - control Planet
        - modify Planet
        - modify camera packets
        - interpret semantic meaning
        - perform selection
        - perform computation
        - feed merged output back into the system

    It only decodes, completes, combines and renders
    already existing data at the final output boundary.
    """

    def __init__(
        self,
        height=240,
        width=320
    ):

        self.height = height
        self.width = width

        #
        # Previous complete field structure
        #

        self.previous = None

        #
        # Final framebuffer
        #

        self.frame = None

    #
    # ------------------------------------------------------------
    # public receive
    # ------------------------------------------------------------

    def receive(
        self,
        packet
    ):

        if packet is None:
            return None

        #
        # Normal packet path
        #

        frame = self.encode(
            packet
        )

        if frame is None:

            print(
                "DISPLAY ENCODE: None"
            )

            return None

        self.frame = frame

        return self.frame

    #
    # ------------------------------------------------------------
    # snapshot output path
    #
    # This is the final convergence point.
    #
    # No internal module is changed.
    #
    # ------------------------------------------------------------

    def receive_snapshot(
        self,
        snapshot
    ):

        if snapshot is None:
            return None

        planet = snapshot.get(
            "planet"
        )

        external = snapshot.get(
            "external"
        )

        #
        # preserved camera stream
        #

        camera_packet = None

        if isinstance(
            external,
            dict
        ):

            camera_packet = external.get(
                "camera_raw"
            )

        #
        # If both streams exist,
        # converge them only here.
        #

        if (
            planet is not None
            and
            camera_packet is not None
        ):

            frame = self._merge_planet_camera(
                planet,
                camera_packet
            )

            if frame is not None:

                frame = self._resize(
                    frame
                )

                self.frame = frame.astype(
                    np.uint8
                )

                return self.frame

        #
        # Fallback:
        # render Planet normally.
        #

        frame = self._planet_snapshot_to_rgb(
            planet
        )

        if frame is None:
            return None

        frame = self._resize(
            frame
        )

        self.frame = frame.astype(
            np.uint8
        )

        return self.frame

    #
    # ------------------------------------------------------------
    # normal packet encoding
    # ------------------------------------------------------------

    def encode(
        self,
        packet
    ):

        if packet is None:
            return None

        data = self._decode(
            packet
        )

        if data is None:
            return None

        #
        # physical camera stream
        #

        if packet.schema == "media.bgr":

            image = self._media_to_rgb(
                data
            )

        #
        # internal fields
        #

        elif packet.schema in (
            "continuous_field",
            "discrete_field"
        ):

            data = self._complete(
                data
            )

            image = self._field_to_rgb(
                data
            )

        else:

            return None

        if image is None:
            return None

        image = self._resize(
            image
        )

        return image.astype(
            np.uint8
        )

    #
    # ------------------------------------------------------------
    # camera BGR -> RGB
    # ------------------------------------------------------------

    def _media_to_rgb(
        self,
        data
    ):

        if data.ndim != 3:
            return None

        if data.shape[2] != 3:
            return None

        #
        # Camera packet is BGR.
        #
        # Framebuffer is RGB.
        #

        return data[:, :, ::-1].copy()

    #
    # ------------------------------------------------------------
    # decode byte packet
    # ------------------------------------------------------------

    def _decode(
        self,
        packet
    ):

        try:

            raw = np.frombuffer(
                packet.data,
                dtype=np.dtype(
                    packet.dtype
                )
            )

            data = raw.reshape(
                packet.shape
            )

        except Exception as e:

            print(
                "DISPLAY DECODE ERROR:",
                e
            )

            return None

        return data

    #
    # ------------------------------------------------------------
    # missing-position completion
    # ------------------------------------------------------------

    def _complete(
        self,
        data
    ):

        if self.previous is None:

            self.previous = data.copy()

            return data

        mask = np.isnan(
            data
        )

        if np.any(mask):

            data = data.copy()

            data[mask] = self.previous[mask]

        self.previous = data.copy()

        return data

    #
    # ------------------------------------------------------------
    # Planet snapshot -> display field
    # ------------------------------------------------------------

    def _planet_snapshot_to_rgb(
        self,
        planet
    ):

        data = self._extract_planet_field(
            planet
        )

        if data is None:
            return None

        data = self._complete(
            data
        )

        return self._field_to_rgb(
            data
        )

    #
    # ------------------------------------------------------------
    # extract actual field from Planet snapshot
    # ------------------------------------------------------------

    def _extract_planet_field(
        self,
        planet
    ):

        if planet is None:
            return None

        #
        # Direct ndarray
        #

        if isinstance(
            planet,
            np.ndarray
        ):

            return planet

        #
        # Common snapshot field names.
        #
        # We do not interpret their meaning.
        # We only locate an array already supplied
        # by the snapshot structure.
        #

        if isinstance(
            planet,
            dict
        ):

            for key in (
                "field",
                "state",
                "data",
                "value",
                "values"
            ):

                value = planet.get(
                    key
                )

                if isinstance(
                    value,
                    np.ndarray
                ):

                    return value

        return None

    #
    # ------------------------------------------------------------
    # final Planet + Camera convergence
    # ------------------------------------------------------------

    def _merge_planet_camera(
        self,
        planet,
        camera_packet
    ):

        #
        # Extract Planet field.
        #

        planet_data = self._extract_planet_field(
            planet
        )

        if planet_data is None:
            return None

        #
        # Decode preserved camera packet.
        #
        # The original packet remains untouched.
        #

        camera_data = self._decode(
            camera_packet
        )

        if camera_data is None:
            return None

        #
        # Camera must still be BGR media.
        #

        if camera_data.ndim != 3:
            return None

        if camera_data.shape[2] != 3:
            return None

        #
        # Planet must provide a spatial scalar field.
        #

        gray = self._to_scalar_field(
            planet_data
        )

        if gray is None:
            return None

        #
        # Establish spatial correspondence.
        #
        # This is only an output-side representation adapter.
        #
        # No data is written back to Planet or Camera.
        #

        gray = self._resize_field(
            gray,
            camera_data.shape[0],
            camera_data.shape[1]
        )

        #
        # Normalize Planet's current field.
        #
        # Planet determines intensity.
        #

        gray = gray.astype(
            np.float32
        )

        minimum = np.nanmin(
            gray
        )

        maximum = np.nanmax(
            gray
        )

        if maximum > minimum:

            gray = (
                gray - minimum
            ) / (
                maximum - minimum
            )

        else:

            gray = np.zeros_like(
                gray,
                dtype=np.float32
            )

        #
        # Camera provides color.
        #
        # Convert BGR -> RGB only for framebuffer output.
        #

        color = camera_data[
            :, :, ::-1
        ].astype(
            np.float32
        ) / 255.0

        #
        # --------------------------------------------------------
        # FINAL CONVERGENCE
        # --------------------------------------------------------
        #
        # Planet:
        #     determines current field intensity.
        #
        # Camera:
        #     supplies preserved color.
        #
        # The two streams meet only here.
        #

        output = (
            color
            * gray[:, :, None]
            * 255.0
        )

        output = np.clip(
            output,
            0,
            255
        )

        return output.astype(
            np.uint8
        )

    #
    # ------------------------------------------------------------
    # convert Planet field to scalar
    # ------------------------------------------------------------

    def _to_scalar_field(
        self,
        data
    ):

        if data is None:
            return None

        #
        # Scalar field
        #

        if data.ndim == 2:

            return data.astype(
                np.float32
            )

        #
        # Vector field
        #
        # Use the first existing component only
        # for visualization.
        #

        if data.ndim == 3:

            if data.shape[2] >= 1:

                return data[
                    :, :, 0
                ].astype(
                    np.float32
                )

        return None

    #
    # ------------------------------------------------------------
    # resize scalar field while preserving its structure
    # ------------------------------------------------------------

    def _resize_field(
        self,
        field,
        height,
        width
    ):

        h, w = field.shape

        ys = np.linspace(
            0,
            h - 1,
            height
        ).astype(
            np.int32
        )

        xs = np.linspace(
            0,
            w - 1,
            width
        ).astype(
            np.int32
        )

        return field[
            np.ix_(
                ys,
                xs
            )
        ]

    #
    # ------------------------------------------------------------
    # internal field visualization
    # ------------------------------------------------------------

    def _field_to_rgb(
        self,
        data
    ):

        if data.ndim == 2:

            #
            # scalar field
            #

            img = data[
                :, :, None
            ]

            img = np.repeat(
                img,
                3,
                axis=2
            )

        elif data.ndim == 3:

            #
            # already vector field
            #

            if data.shape[2] == 3:

                img = data

            else:

                img = np.repeat(
                    data[:, :, :1],
                    3,
                    axis=2
                )

        else:

            return None

        #
        # normalize framebuffer
        #

        img = img.astype(
            np.float32
        )

        minimum = np.nanmin(
            img
        )

        maximum = np.nanmax(
            img
        )

        if maximum > minimum:

            img = (
                img - minimum
            ) / (
                maximum - minimum
            )

        else:

            img = np.zeros_like(
                img
            )

        return (
            img * 255.0
        ).clip(
            0,
            255
        ).astype(
            np.uint8
        )

    #
    # ------------------------------------------------------------
    # display size adapter
    # ------------------------------------------------------------

    def _resize(
        self,
        img
    ):

        h, w, c = img.shape

        ys = np.linspace(
            0,
            h - 1,
            self.height
        ).astype(
            np.int32
        )

        xs = np.linspace(
            0,
            w - 1,
            self.width
        ).astype(
            np.int32
        )

        return img[
            np.ix_(
                ys,
                xs,
                np.arange(c)
            )
        ]

    #
    # ------------------------------------------------------------
    # framebuffer
    # ------------------------------------------------------------

    def render(
        self
    ):

        return self.frame

