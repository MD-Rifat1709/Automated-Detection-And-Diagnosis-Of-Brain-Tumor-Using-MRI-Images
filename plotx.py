import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


def result(image, output, title, transparency=0.38, save_path=None):
    seg_output = output*transparency
    seg_image = np.add(image, seg_output)/2
    return seg_image

