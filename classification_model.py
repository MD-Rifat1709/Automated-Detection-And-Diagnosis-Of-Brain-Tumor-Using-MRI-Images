import numpy as np
import cv2
from PIL import Image
from keras.models import load_model

def classification_model (image_path):
    model = load_model('Classification/EfficientNetB2-raw(1).h5')
    img = Image.open(image_path)
    opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = cv2.resize(opencvImage,(150,150))
    img = img.reshape(1,150,150,3)
    p = model.predict(img)
    p = np.argmax(p,axis=1)[0]

    if p==0:
        x = 'Meningioma Tumor'
        y = 'D32. 9'
    elif p==1:
        x = 'Glioma Tumor'
        y = 'C71. 9'
    elif p==2:
        x = 'Pituitary Tumor'
        y = 'E23.7'
    else:
        x = 'No Tumor'
        y = 'NA'

    return x,y
        


