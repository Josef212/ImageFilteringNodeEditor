import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

class OilNode(BaseNode):
    node = None
    input_atr = None
    output_atr = None
    size = 3
    dyn_ratio = 1

    def __init__(self):
        pass

    def build_dpg(self, editor):
        def update_value(sender, app_data, user_data):
            if user_data[1] == 1:
                user_data[0].size = app_data
            elif user_data[1] == 2:
                user_data[0].dyn_ratio = app_data

        with dpg.node(label="Oil painting", parent=editor) as node:
            with dpg.node_attribute(label="InputAtr", attribute_type=dpg.mvNode_Attr_Input) as in_atr:
                dpg.add_input_int(label="Size", width=150, callback=update_value, user_data=(self, 1), default_value=self.size)
                dpg.add_input_int(label="Dyn ratio", width=150, callback=update_value, user_data=(self, 2), default_value=self.dyn_ratio)

            with dpg.node_attribute(label="OutputAtr", attribute_type=dpg.mvNode_Attr_Output) as out_atr:
                dpg.add_text("Output")

        self.node = node
        self.input_atr = in_atr
        self.output_atr = out_atr

    def get_all_attributes(self):
        return [self.input_atr, self.output_atr]

    def get_debug_name(self):
        return "OilNode"

    def get_input_attributes(self):
        return [self.input_atr]

    def get_output(self, tree):
        input_tree_node = tree.children[0]
        input_node = input_tree_node.value
        img = input_node.get_output(input_tree_node)
        ret = cv2.xphoto.oilPainting(img, self.size, self.dyn_ratio)

        return ret
