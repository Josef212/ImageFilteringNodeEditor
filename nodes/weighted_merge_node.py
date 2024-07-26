import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

class WeightedMergeNode(BaseNode):
    node = None
    input1_atr = None
    input2_atr = None
    output_atr = None
    # TODO: Alpha parameter field

    def __init__(self):
        pass

    def build_dpg(self, editor):
        def update_value(sender, app_data, user_data):
            user_data.value = app_data

        with dpg.node(label="Weighted merge", parent=editor) as node:
            with dpg.node_attribute(label="Input1Atr", attribute_type=dpg.mvNode_Attr_Input) as in1_atr:
                dpg.add_text(label="Input1")
            with dpg.node_attribute(label="Input2Atr", attribute_type=dpg.mvNode_Attr_Input) as in2_atr:
                dpg.add_text(label="Input2")
            with dpg.node_attribute(label="OutputAtr", attribute_type=dpg.mvNode_Attr_Output) as out_atr:
                dpg.add_text(label="Output")

        self.node = node
        self.input1_atr = in1_atr
        self.input2_atr = in2_atr
        self.output_atr = out_atr

    def get_all_attributes(self):
        return [self.input1_atr, self.input2_atr, self.output_atr]

    def get_debug_name(self):
        return "WheightedMergeNode"

    def get_input_attributes(self):
        return [self.input1_atr, self.input2_atr]

    def get_output(self, tree):
        input1_tree_node = tree.children[0]
        input1_node = input1_tree_node.value
        input2_tree_node = tree.children[1]
        input2_node = input2_tree_node.value

        img1 = input1_node.get_output(input1_tree_node)
        img2 = input2_node.get_output(input2_tree_node)

        print(f"Img1 shape: {img1.shape}")
        print(f"Img2 shape: {img2.shape}")

        ALPHA = 0.5
        merged = cv2.addWeighted(img1, ALPHA, img2, (1 - ALPHA), 0)

        return merged
