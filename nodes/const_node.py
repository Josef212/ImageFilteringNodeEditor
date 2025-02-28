import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

class ConstNode(BaseNode):
    node = None
    output_atr = None
    value = 0.0

    def __init__(self):
        pass

    def build_dpg(self, editor):
        def update_value(sender, app_data, user_data):
            user_data.value = app_data

        with dpg.node(label="Cosnt", parent=editor) as node:
            with dpg.node_attribute(label="OutputAtr", attribute_type=dpg.mvNode_Attr_Output) as out_atr:
                dpg.add_input_float(label="Value", width=150, callback=update_value, user_data=self, default_value=self.value)

        self.node = node
        self.output_atr = out_atr

    def get_all_attributes(self):
        return [self.output_atr]

    def get_debug_name(self):
        return "ConstNode"

    def get_input_attributes(self):
        return []

    def get_output(self, tree):
        return self.value
