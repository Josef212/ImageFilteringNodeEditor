import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

class SourceNode(BaseNode):
    src_image_path = ""

    node = None
    output_atr = None

    path_text_item = None
    image_item = None

    image_texture_tag = None
    cv_image = None

    def __init__(self):
        pass

    def build_dpg(self, editor):
        def dialog_cbk(sender, app_data, user_data):
            print(app_data)
            self.load_image(app_data["file_path_name"])
            pass

        with dpg.file_dialog(
            label="Select image",
            directory_selector=False, 
            show=False, 
            callback=dialog_cbk, tag="file_dialog_id", 
            width=700, height=400):
            dpg.add_file_extension(".jpg")

        with dpg.node(label="Src image", parent=editor) as node:
            with dpg.node_attribute(label="Atr", attribute_type=dpg.mvNode_Attr_Output) as atr:
                self.image_item = dpg.add_image(BLACK_TEXTURE, width=100, height=100)
                self.path_text_item = dpg.add_text("")
                dpg.add_button(label="Load image", width=150, callback=lambda: dpg.show_item("file_dialog_id"))

        self.node = node
        self.output_atr = atr

    def load_image(self, img_path):
        if self.image_texture_tag is not None:
            dpg.delete_item(self.image_texture_tag)
            self.image_texture_tag = None

        if self.cv_image is not None:
            self.cv_image = None

        self.src_image_path = img_path
        cv_image, dpg_tag = load_texture(self.src_image_path)

        self.cv_image = cv_image
        self.image_texture_tag = dpg_tag

        self.update_ui()
        
    def update_ui(self):
        dpg.configure_item(self.image_item, texture_tag=self.image_texture_tag)
        dpg.set_value(self.path_text_item, self.src_image_path)

    def get_debug_name(self):
        return "SrcNode"

    def get_all_attributes(self):
        return [self.output_atr]

    def get_input_attributes(self):
        return []

    def get_output(self, tree):
        return self.cv_image
