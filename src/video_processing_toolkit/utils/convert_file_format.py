import numpy as np
import torch


class ConvertFileFormat:

    def __init__(self):
        print(" I am inside init function of test file ")

    @staticmethod
    def to_numpy(tensor):
        if torch.is_tensor(tensor):
            return tensor.cpu().numpy()
        elif type(tensor).__module__ != 'numpy':
            raise ValueError("Cannot convert {} to numpy array"
                             .format(type(tensor)))
        return tensor

    @staticmethod
    def torch_var_to_numpy(tensor_var):
        """ Converts Tensor from a Pytorch tensor to a numpy array.

        Args:
            tensor_var: (torch.Tensor) A Pytorch tensor. Normally a batch of 3D (Ch x Height x Width) images

        Returns:
            np_tensor: (numpy.ndarray) The same tensor as a numpy array.
        """
        if torch.is_tensor(tensor_var):
            np_tensor = tensor_var.detach().cpu().numpy()
            np_tensor = np.transpose(np_tensor, (0, 2, 3, 1))
            np_tensor = np_tensor.squeeze()
            return np_tensor
        elif type(tensor_var).__module__ != 'numpy':
            raise ValueError("Cannot convert {} to numpy array"
                             .format(type(tensor_var)))
        return tensor_var

    @staticmethod
    def numpy_to_torch_var(np_tensor, device):
        """ Converts Tensor from a numpy array to a Pytorch tensor.

        Args:
            np_tensor: (numpy.ndarray) The same tensor as a numpy array.

        Returns:
            var: (torch.Tensor) A Pytorch tensor.
        """
        if len(np_tensor.shape) == 3:
            np_tensor = np.expand_dims(np_tensor, axis=0)
        var = np.transpose(np_tensor, (0, 3, 1, 2))
        var = torch.from_numpy(var).float()
        var = var.to(device)
        return var

    @staticmethod
    def permute_tensor_dims(input_var):
        """ This function implements the ToTensor class, without scaling the pixel values to the [0,1] range.
            H x W x C -> C x H x W

        Args:
            input_var: (numpy.ndarray) The same tensor as a numpy array.

        Returns:
            var: (torch.Tensor) A Pytorch tensor.
        """
        var = torch.FloatTensor(np.array(input_var)).permute(2, 0, 1)
        return var

    @staticmethod
    def to_torch(ndarray):
        if type(ndarray).__module__ == 'numpy':
            return torch.from_numpy(ndarray)
        elif not torch.is_tensor(ndarray):
            raise ValueError("Cannot convert {} to torch tensor"
                             .format(type(ndarray)))
        return ndarray

    @staticmethod
    def im_to_numpy(img):
        img = ConvertFileFormat.to_numpy(img)
        img = np.transpose(img, (1, 2, 0))  # H*W*C
        return img

    @staticmethod
    def im_to_torch(img):
        """
        cv img [h, w, c]
        torch  [c, h, w]
        """
        img = np.transpose(img, (2, 0, 1))  # C*H*W
        img = ConvertFileFormat.to_torch(img).float()
        return img

    @staticmethod
    def torch_to_img(img):
        img = ConvertFileFormat.to_numpy(torch.squeeze(img, 0))
        img = np.transpose(img, (1, 2, 0))  # H*W*C
        return img
