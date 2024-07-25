import dearpygui.dearpygui as dpg
import cv2
import numpy as np

dpg.create_context()

img_name = "test_image.jpg"
img_name = "kholin.jpg"

img = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
height, width, _ = img.shape

data = img
data = cv2.cvtColor(data, cv2.COLOR_BGRA2RGBA)
# data = np.flip(data, 1)
data = np.ravel(data)
data = np.asarray(data, dtype=np.float32)
data = np.true_divide(data, 255.0)

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(width=width, height=height, default_value=data, tag="texture_tag", format=dpg.mvFormat_Float_rgba, label=img_name)

with dpg.window(label="Example window"):
    dpg.add_text("Hello world")
    dpg.add_image("texture_tag", width=300, height=250)



dpg.create_viewport(title="Testing", width=800, height=600)
dpg.set_viewport_vsync(True)

dpg.setup_dearpygui()
dpg.show_viewport()

dpg.start_dearpygui()
dpg.destroy_context()
