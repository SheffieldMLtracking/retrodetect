import numpy as np

from retrodetect.image_processing import getblockmaxedimage


class Retrodetect:
    """
    Retrodetect class is used to detect retro-reflectors in images.
    """

    def __init__(self, n_max_dilations: int = 5):
        self.max_dilated_img = None
        self.idx = 0
        self.n_max_dilations = n_max_dilations

    @staticmethod
    def find_tags(diff, img):
        """
        Finds potential tag locations in an image based on a difference image.

        This function iterates through a difference image (`diff`) and analyzes
        corresponding patches in the original image (`img`) to identify regions
        that might contain tags. It uses various criteria based on pixel intensities
        within the patch and surrounding areas.

        Args:
            diff (np.ndarray): A difference image, likely representing the result
                               of some image processing operation highlighting areas
                               of change. Expected to be a NumPy array.
            img (np.ndarray): The original image from which the difference image
                              was derived. Expected to be a NumPy array.

        Returns:
            list: A list of NumPy arrays, where each array represents a potential
                  tag location and contains the following information:
                    - Prediction score (float)
                    - X-coordinate (int)
                    - Y-coordinate (int)
                    - Maximum value in the difference patch (float)
                    - Maximum value in the center of the tag zone (float)
                    - Average value of the background in the patch (float)
                    - Maximum value in the outer surrounding pixels (float)
                    - Maximum value in the inner surrounding pixels (float)
                    - Maximum value in the center (unused?) (float)
                    - Difference patch as a NumPy array (float32)
                    - Original image patch as a NumPy array (float32)

        Notes:
            - The function assumes the difference image and original image have
              the same dimensions.
            - The specific logic for calculating the prediction score (`pred`) might
              require further explanation or reference to the underlying algorithm.
        """

        results = list()
        save_size = 20
        del_size = 15

        np.set_printoptions(precision=2, suppress=True)

        for n_patches in range(5):
            y, x = np.unravel_index(diff.argmax(), diff.shape)

            diff_max = diff[y, x]
            img_patch = img[y - save_size:y + save_size, x - save_size:x + save_size].astype(np.float32).copy()
            temp = img_patch.copy()
            diff_patch = diff[y - save_size:y + save_size, x - save_size:x + save_size].copy().astype(np.float32)
            diff[max(0, y - del_size):min(diff.shape[0], y + del_size),
            max(0, x - del_size):min(diff.shape[1], x + del_size)] = -5000

            if (x <= 20) or (x >= diff.shape[1] - 20) or (y <= 20) or (y >= diff.shape[0] - 20):
                res = np.array([-100, x, y, 0, 0, 0, 0, 0, 0, diff_patch, temp])
                results.append(res)
                continue

            centre_image = img_patch[17:24, 17:24].copy()
            img_patch[37:44, 37:44] = 0
            centre_max = np.max(centre_image.flatten())
            bg_mean = np.mean(img_patch.flatten())

            outer_surround_max = np.max(img_patch[[16, 20, 24, 20, 16, 16, 24, 24], [20, 16, 20, 24, 16, 24, 16, 24]])
            inner_surround_max = np.max(img_patch[[18, 20, 22, 20, 18, 18, 22, 22], [20, 18, 20, 22, 18, 22, 18, 22]])
            # not used?
            # centre_sum = np.sum(img_patch[[20,20,20,19,21],[20,21,19,20,20]])
            pred = 5
            # pred-= 250/(1+diff_max) #value at max in difference image
            pred += diff_max / 100  # ?
            pred -= 250 / (1 + centre_max)  # maximum in centre of tag zone in normal image
            pred -= 20 * inner_surround_max / centre_max  # ratio of the max value in the innersurrounding pixels and the maximum
            pred -= outer_surround_max / 100  # how bright the outer surrounding pixels are

            res = np.array(
                [pred, x, y, diff_max, centre_max, bg_mean, outer_surround_max, inner_surround_max, centre_max,
                 diff_patch, temp])
            results.append(res)
        return results

    def process_photo(self, photo_item: dict, idx=None):
        """
        Processes a photo object.
         - normalise
         - compute the dilated image
         - compute diff image from the max dilated image of last self.Nmaxdilations

        :param photo_item: The contents of a photo data file.
        :param idx: The photo index value
        """
        if idx is not None:
            self.idx = idx
        if self.max_dilated_img is None:
            try:
                imgshape = list(photo_item['img'].shape)
            except AttributeError:
                return []
            imgshape.append(self.n_max_dilations)
            self.max_dilated_img = np.full(imgshape, 5000)

        # convert to float
        try:
            img = photo_item['img'].astype(np.float32)
        except AttributeError:
            return list()

        # normalise photo
        img = 5 * img / np.mean(img)
        # compute the difference photo...
        diff_img = img - np.max(self.max_dilated_img, 2)

        dilated_img = getblockmaxedimage(img, 3, 3)
        self.max_dilated_img[:, :, self.idx % self.n_max_dilations] = dilated_img
        self.idx += 1  # this just is an index to access the max_dilate_img array

        return self.find_tags(diff_img, img)
