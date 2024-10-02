import sys
import warnings
warnings.filterwarnings('ignore')
import torch
import os
import torchvision.transforms as transforms
import torchvision.transforms.functional as TF
import numpy as np
from PIL import Image

# Append the Segmentation directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Segmentation'))
import bts.model as model
import bts.classifier as classifier

def segmentation(image_path):
    # Set the device to CUDA if available, otherwise CPU
    device = torch.device('cpu')
    FILTER_LIST = [16, 32, 64, 128, 256]
    LOAD_MODEL = True

    # Define the transformation to apply to the input image
    default_transformation = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((512, 512))
    ])

    # Load the image and apply transformations
    image_name = image_path
    image_x = Image.open(image_name)
    image = default_transformation(image_x)
    image_tensor = TF.to_tensor(image).unsqueeze(0)  # Add batch dimension

    # Initialize the UNet model and classifier
    unet_model = model.DynamicUNet(FILTER_LIST).to(device)
    unet_classifier = classifier.BrainTumorClassifier(unet_model, device)

    if LOAD_MODEL:
        # Load the model weights, mapping to CPU if necessary
        unet_classifier.restore_model('Segmentation/saved_models/UNet-[16, 32, 64, 128, 256].pt')

    # Set the model to evaluation mode
    unet_model.eval()

    # Move the input tensor to the correct device
    image_tensor = image_tensor.to(device)

    # Perform inference
    with torch.no_grad():  # Disable gradient calculation
        output = unet_model(image_tensor)

    # Threshold the output and convert to numpy array
    output = (output > 0.5).cpu().numpy()  # Move output back to CPU
    image = TF.to_tensor(image_x).numpy()  # Convert image back to numpy

    # Resize output and image
    image_resized = np.resize((image * 255), (512, 512))
    output_resized = np.resize((output * 255), (512, 512))

    # Save the output mask
    basename = os.path.basename(image_path)
    path1 = 'constructed_mask/'
    os.makedirs(path1, exist_ok=True)  # Create directory if it doesn't exist
    output_path = os.path.join(path1, basename)
    output_image = Image.fromarray(np.uint8(output_resized), 'L')
    output_image.save(output_path)

    return image_resized, output_resized, output_path, basename
