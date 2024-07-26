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

def register_dpg_texture(data, label, width, height, show_registry=False):
    tag = None
    with dpg.texture_registry(show=show_registry):
        tag = dpg.add_dynamic_texture(width=width, height=height, default_value=data, label=label)

    return tag

def load_texture(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    height, width, _ = img.shape
    dpg_image = convert_cv_to_dpg_image(img)
    tag = register_dpg_texture(dpg_image, img_path, width, height)

    return img, tag

def calculate_output_image_window():
    window_width = 350
    window_height = 320
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    extra_margin_x = 25
    extra_margin_y = 48
    image_width = window_width * 0.95
    image_height = (window_height - 60)

    window_pos = (viewport_width - window_width - extra_margin_x, viewport_height - window_height - extra_margin_y)
    window_size = (window_width, window_height)
    image_size = (image_width, image_height)


    return (window_pos, window_size, image_size)

def load_default_textures():
    with dpg.texture_registry(show=False):
        black_tex = generate_plain_texture((100, 100), (0 / 255, 0 / 255, 0 / 255, 255 / 255))
        dpg.add_dynamic_texture(width=100, height=100, default_value=black_tex, tag=BLACK_TEXTURE, label="BLACK_TEX")#, format=dpg.mvFormat_Float_rgba)

        white_tex = generate_plain_texture((100, 100), (255 / 255, 255 / 255, 255 / 255, 255 / 255))
        dpg.add_dynamic_texture(width=100, height=100, default_value=white_tex, tag=WHITE_TEXTURE, label="WHITE_TEX")#, format=dpg.mvFormat_Float_rgba)
