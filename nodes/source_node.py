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
        with dpg.node(label="Src image", parent=editor) as node:
            with dpg.node_attribute(label="Atr", attribute_type=dpg.mvNode_Attr_Output) as atr:
                self.image_item = dpg.add_image(BLACK_TEXTURE, width=100, height=100)
                self.path_text_item = dpg.add_text("")
                dpg.add_button(label="Load image", width=150, callback=lambda _, __, obj: obj.load_image(IMG_NAME), user_data=self)

        self.node = node
        self.output_atr = atr

    def load_image(self, img_path):
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

    def get_output(self):
        pass
