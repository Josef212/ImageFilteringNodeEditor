import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

# TODO: Should add resize modes
class ResizeNode(BaseNode):
    node = None
    input_atr = None
    output_atr = None
    percentage = 50

    def __init__(self):
        pass

    def build_dpg(self, editor):
        def update_value(sender, app_data, user_data):
            if user_data == 1:
                user_data.percentage = app_data

        with dpg.node(label="Resize", parent=editor) as node:
            with dpg.node_attribute(label="InputAtr", attribute_type=dpg.mvNode_Attr_Input) as in_atr:
                dpg.add_input_int(label="Resize percentage", width=150, callback=update_value, user_data=self, default_value=self.percentage)

            with dpg.node_attribute(label="OutputAtr", attribute_type=dpg.mvNode_Attr_Output) as out_atr:
                dpg.add_text("Output")

        self.node = node
        self.input_atr = in_atr
        self.output_atr = out_atr

    def get_all_attributes(self):
        return [self.input_atr, self.output_atr]

    def get_debug_name(self):
        return "ResizeNode"

    def get_input_attributes(self):
        return [self.input_atr]

    def get_output(self, tree):
        input_tree_node = tree.children[0]
        input_node = input_tree_node.value
        img = input_node.get_output(input_tree_node)
        height, width, _ = img.shape
        target_width = width * (self.percentage / 100.0)
        target_height = height * (self.percentage / 100.0)

        # TODO: Expose the interpolation as field
        ret = cv2.resize(img, (int(target_width), int(target_height)), interpolation = cv2.INTER_AREA)

        return ret
