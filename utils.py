import dearpygui.dearpygui as dpg
import cv2
import numpy as np

IMG_NAME = "test_image.jpg"
WHITE_TEXTURE = "white_texture"
BLACK_TEXTURE = "black_texture"

def convert_cv_to_dpg_image(cv_image):
    data = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2RGBA)
    data = np.ravel(data)
    data = np.asarray(data, dtype=np.float32)
    data = np.true_divide(data, 255.0)
    return data

def generate_plain_texture(shape, color):
    data = []
    for i in range(0, shape[0] * shape[1]):
        data.append(color[0])
        data.append(color[1])
        data.append(color[2])
        data.append(color[3])

    return data

def load_texture(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    height, width, _ = img.shape
    dpg_image = convert_cv_to_dpg_image(img)

    tag = None

    with dpg.texture_registry(show=False):
        tag = dpg.add_dynamic_texture(width=width, height=height, default_value=dpg_image, label=img_path)

    return img, tag
