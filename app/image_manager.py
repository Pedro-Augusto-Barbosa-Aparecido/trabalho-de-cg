import os
import cv2
import pathlib
import numpy as np

from abc import abstractmethod, ABC

from app.settings import TEMP_FOLDER


class ImageManager(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def _convert_image_to_grayscale_with_np(np_image: np.ndarray) -> np.ndarray:
        image_in_gray_scale = np.average(np_image[:, :, :3], axis=2)
        return image_in_gray_scale

    @staticmethod
    def _convert_image_to_grayscale_with_opencv(image):
        """convert image to grayscale with OpenCV
        :param image: cv2.MatLike
        :rtype: cv2.MatLike
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def _get_mask_with_opencv(image_in_gray_scale):
        """make mask of an image with opencv
        :param: image_in_gray_scale: cv2.MatLike
        :rtype: NDArray[uint8]
        """
        threshold = cv2.threshold(image_in_gray_scale, 250, 255, cv2.THRESH_BINARY)[1]
        threshold = 255 - threshold

        kernel = np.ones((3, 3), np.uint8)

        mask_of_image = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
        mask_of_image = cv2.morphologyEx(mask_of_image, cv2.MORPH_CLOSE, kernel)

        mask_of_image = cv2.GaussianBlur(mask_of_image, (0, 0), sigmaX=2, sigmaY=2, borderType=cv2.BORDER_DEFAULT)
        mask_of_image = (2 * (mask_of_image.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)

        return mask_of_image

    @staticmethod
    def remove_bg(image_path) -> str:
        """remove background of image with opencv
        :param image_path: pathlib.PathLike | str
        :rtype: cv2.MatLike
        """
        image_to_remove_bg = cv2.imread(image_path)
        image_to_remove_bg_np = np.array(image_to_remove_bg)
        image_to_remove_bg_grayscale = ImageManager._convert_image_to_grayscale_with_opencv(image_to_remove_bg_np)
        mask = ImageManager._get_mask_with_opencv(image_to_remove_bg_grayscale)

        image = cv2.cvtColor(image_to_remove_bg.copy(), cv2.COLOR_BGR2BGRA)
        image[:, :, 3] = mask

        filename = os.path.basename(image_path)
        filepath = os.path.join(TEMP_FOLDER, filename)

        _filepath = pathlib.Path(filepath)

        filepath = filepath.replace(
            _filepath.suffix,
            ".png"
        )

        cv2.imwrite(
            filepath,
            image
        )

        return filepath
