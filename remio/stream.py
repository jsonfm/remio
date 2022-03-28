import numpy as np
import base64 as b64
import simplejpeg


class MJPEGEncoder:
    """MJPEG encoder based on simplejpeg library.

    Args:
        image: uncompressed image as uint8 array
        quality: JPEG quantization factor
        colorspace: source colorspace; one of
                        'RGB', 'BGR', 'RGBX', 'BGRX', 'XBGR', 'XRGB',
                        'GRAY', 'RGBA', 'BGRA', 'ABGR', 'ARGB', 'CMYK'.
        colorsubsampling: subsampling factor for color channels; one of
                                '444', '422', '420', '440', '411', 'Gray'.
        fastdct: If True, use fastest DCT method;
                        speeds up encoding by 4-5% for a minor loss in quality

    """
    def __init__(
        self, 
        quality: int = 85,
        colorspace: str = 'rgb',
        colorsubsampling: str = '444',
        fastdct: bool = True,
        *args, 
        **kwargs):
        self.quality = quality
        self.colorspace = colorspace
        self.colorsubsampling = colorsubsampling
        self.fastdct = fastdct
        print('quality: ', self.quality)

    def setParams(
        self,
        quality: int = 85,
        colorspace: str = 'rgb',
        colorsubsampling: str = '444',
        fastdct: bool = True
    ):
        self.quality = quality
        self.colorspace = colorspace
        self.colorsubsampling = colorsubsampling
        self.fastdct = fastdct

    def encode(self, frame: np.ndarray = None, base64: bool = True):
        """Encodes an array of images in JPEG format and, if possible, convert it to base64.

        Args:
            frame: image array
            base64: encode image in base64 format?

        Returns:
            jpeg: encoded image as JPEG (JFIF) data

        """
        if frame is not None:
            if self.colorspace == "GRAY":
                if frame.ndim == 2:
                    frame = frame[:, :, np.newaxis]

            jpeg = simplejpeg.encode_jpeg(
                frame,
                self.quality,
                self.colorspace,
                self.colorsubsampling,
                self.fastdct
            )

            if base64:
                jpeg = b64.b64encode(jpeg).decode()

            return jpeg
