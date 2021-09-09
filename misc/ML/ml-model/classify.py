from PIL import Image,ImageFile
import numpy as np
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob
from tensorflow.keras.models import load_model

model = load_model('model.h5')

#dictionary to label all traffic signs class.
classes = {
    0:'cat',
    1:'dog',

}

def classify_with_filter(dir, attack_path):   
    w, h = (128, 128)
    image_attack = Image.open(attack_path)
    image_attack = image_attack.convert("RGBA")
    image_attack = image_attack.resize((w, h))

    cats = 0
    hacked = 0
    for file_path in glob.glob(f'{dir}/*.jpg'):
        try:
            image = Image.open(file_path)
            image = image.resize((w, h))
            pixel_count = 0
            for x in range(w):
                for y in range(h):
                    pixel = image_attack.getpixel((x, y))
                    if pixel[3] > 0 and pixel_count < 1900: # on the server you only have 1900 pixel i.e 1900 pixel might be not transparent
                        pixel_count += 1
                        image.putpixel((x, y), image_attack.getpixel((x, y)))
            image = image.convert("RGB")
            image = np.expand_dims(image, axis=0)
            image = np.array(image)
            
            image = image / 255
            res = classes[np.argmax(model.predict([image]), axis=-1)[0]]
            cats += 1
            if res == "dog":
                hacked += 1
        except:
            continue
    print(f"Checked: {cats} and hacked: {hacked}")

classify_with_filter("./Cat","./attack/attack.png")