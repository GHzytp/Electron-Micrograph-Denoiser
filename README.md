# TEM Denoiser

This repository is for a deep convolutional neural network trained to remove Poisson noise from transmission electron micrographs (TEMs) that outperforms existing methods by 24.6%. It contains a checkpoint for the fully trained network, a training script `denoiser-multi-gpu.py` and an inference script 'denoiser.py'. The training script is written for multi-GPU training in a distributed setting and the inference script loads the neural network once for repeated inference.

## Download

To get the neural network and its training and inference scripts, simply copy the files from or clone this repository:

```
git clone https://github.com/Jeffrey-Ede/Electron-Micrograph-Denoiser.git
cd Electron-Micrograph-Denoiser
```

## Dependencies

This neural network was trained using TensorFlow and requires it and other common python libraries. Most of these libraries come with modern python distributions by default. If you don't some of these libraries, they can be installed using pip or another package manager. 

Libraries you need for both training and inference:

* tensorFlow
* numpy
* cv2
* functools
* itertools
* collections
* six
* os

for training you also need:

* argparse
* random
* scipy
* Image

## Example Usage

Example inference:

```python
import numpy as np
from denoiser import Denoiser, disp

#Create a 1000x1000 image from randon numbers for demonstration
#Tra=y replacing this with your own image!
img = np.random.rand(1000, 1000)

#Initialize the denoising neural network
noise_remover = Denoiser()

#Denoise a 512x512 crop from the image
crop = img[:512,:512]
denoised_crop = noise_remover.denoise_crop(crop)

#Denoise the entire image
denoised_img = noise_remover.denoise(img)

#Use the disp function to display the results
disp(crop) #Crop before denoising
disp(denoised_crop) #Crop after denoising
disp(img) #Image before denoising
disp(denoised_img) #Image after denoising
```

##Incomplete! 

This repository is still in the works! I'm in the process of writing up a paper, publishing the training, validation and test data and neatening up my source code. Nevertheless, the neural network published here is now in a working state.

[Trained neural network](<add link>)
