import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

class CannyNode(BaseNode):
    node = None
    input_atr = None
    output_atr = None
    threshold1 = 100
    threshold2 = 200

    def __init__(self):
        pass

    def build_dpg(self, editor):
        def update_threshold(sender, app_data, user_data):
            if user_data[1] == 1:
                user_data.threshold1 = app_data
            elif user_data[1] == 2:
                user_data.threshold2 = app_data

        with dpg.node(label="Canny edges", parent=editor) as node:
            with dpg.node_attribute(label="InputAtr", attribute_type=dpg.mvNode_Attr_Input) as in_atr:
                dpg.add_input_int(label="Threshold 1", width=150, callback=update_threshold, user_data=(self, 1), default_value=self.threshold1)
                dpg.add_input_int(label="Threshold 2", width=150, callback=update_threshold, user_data=(self, 2), default_value=self.threshold2)

            with dpg.node_attribute(label="OutputAtr", attribute_type=dpg.mvNode_Attr_Output) as out_atr:
                dpg.add_text("Output")

        self.node = node
        self.input_atr = in_atr
        self.output_atr = out_atr

    def get_all_attributes(self):
        return [self.input_atr, self.output_atr]

    def get_debug_name(self):
        return "CannyNode"

    def get_input_attributes(self):
        return [self.input_atr]

    def get_output(self, tree):
        input_tree_node = tree.children[0]
        input_node = input_tree_node.value
        img = input_node.get_output(input_tree_node)
        canny_edges = cv2.Canny(img, threshold1=self.threshold1, threshold2=self.threshold2)

        return canny_edges
