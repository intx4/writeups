import tensorflow as tf
from tensorflow import keras
from PIL import Image,ImageFile
import numpy as np
from tensorflow.keras.losses import CategoricalCrossentropy as BCE

ImageFile.LOAD_TRUNCATED_IMAGES = True
w = 128
h = 128

m = w // 2
start_x = m - 21
start_y = m - 22
extra_x = start_x + 43

#dictionary to label.
classes = {
    0:'cat',
    1:'dog',
}
y_true = [[0, 1]] #dog

try:
    model = keras.models.load_model('model.h5')
    print("*** Loaded ***")

    model.summary()
    layer = model.get_layer("dense_1") #relu
    layer = model.get_layer("dense_2") #softmax

except:
    print("*** Fail ***")

def pre_process():
    #from chall
    image = Image.open("gurke.jpg")
    image = image.resize((w,h))
    image = image.convert("RGB")
    image = np.expand_dims(image, axis=0)
    image = np.array(image) #it's a tensor of 128x128x1, with elements living in R^3 (RGB) -> 1,128,128,3
    image = image / 255 #normalize
    return image

'''
alpha=False
Basically creates a mask of 1900 pixelsat the centre of the image by setting all other pixels to 0
alpha=True
Creates a mask to make the alpha channel 1 just for the pixel in the patch
'''
def put_patch(x, alpha=False):
    if not alpha:
        mask = np.zeros_like(x)
        #create a patch at center of image of pixel 43x44
        mask[:,start_x:start_x+43,start_y:start_y+44,:] = 1

        #reach 1900 pixels
        mask[:,extra_x:extra_x+8,m,:] = 1
        patched = mask * x
    else:
        mask = np.zeros((128,128,1))
        mask[start_x:start_x+43, start_y:start_y+44,:] = 1
        mask[extra_x:extra_x+8,m,:] = 1
        patched = np.dstack((x, mask))

    return patched

def get_gradient(x):
    with tf.GradientTape() as tape:
        x = tf.convert_to_tensor(x, dtype=tf.float32)
        tape.watch(x)

        label = tf.Variable(y_true,shape=(1,2))

        loss_func = BCE()

        pred = model(x)
        
        loss = loss_func(label, pred)
        return tape.gradient(loss,x).numpy()
        
def get_active_pixels(file_path):
    image = Image.open(file_path)
    image = image.convert("RGBA")
    image = image.resize((w, h))
    pixel_count = 0
    for x in range(w):
        for y in range(h):
            pixel = image.getpixel((x, y))
            if pixel[3] > 0: # on the server you only have 1900 pixel i.e 1900 pixel might be not transparent
                pixel_count += 1
    return pixel_count

def attack():
    x = pre_process()
    
    EPS = 20000
    lambda_ = 0.2

    for _ in range(0,EPS):
        x = put_patch(x)
        g = get_gradient(x)
        x = x - lambda_*g
    
    x = x * 255
    x = put_patch(x.squeeze(), True)

    # save img
    img = Image.fromarray(x.astype('uint8'), 'RGBA')
    
    img.save("./attack.png")

    assert(get_active_pixels("attack.png") <= 1900)

attack()