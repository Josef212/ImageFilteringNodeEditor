import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

class OneToNChannels(BaseNode):
    node = None
    input_atr = None
    output_atr = None
    channel_count = 4
    # TODO: Add channel count input field

    def __init__(self):
        pass

    def build_dpg(self, editor):
        def update_value(sender, app_data, user_data):
            user_data.value = app_data

        with dpg.node(label="One to n channels", parent=editor) as node:
            with dpg.node_attribute(label="InputAtr", attribute_type=dpg.mvNode_Attr_Input) as in_atr:
                dpg.add_text(label="Input")
            with dpg.node_attribute(label="OutputAtr", attribute_type=dpg.mvNode_Attr_Output) as out_atr:
                dpg.add_text(label="Output")

        self.node = node
        self.input_atr = in_atr
        self.output_atr = out_atr

    def get_all_attributes(self):
        return [self.input_atr, self.output_atr]

    def get_debug_name(self):
        return "OneToNChannelsNode"

    def get_input_attributes(self):
        return [self.input_atr]

    def get_output(self, tree):
        input_tree_node = tree.children[0]
        input_node = input_tree_node.value
        img = input_node.get_output(input_tree_node)

        output = ()
        for _ in range(0, self.channel_count):
            output = output + (img,)

        output = cv2.merge(output)

        return output
