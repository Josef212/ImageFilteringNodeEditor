import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

class TestNode(BaseNode):
    node = None
    input1_atr = None
    input2_atr = None
    output_atr = None

    def __init__(self):
        pass

    def build_dpg(self, editor):
        with dpg.node(label="Test", parent=editor) as node:
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
        return "TestNode"

    def get_input_attributes(self):
        return [self.input1_atr, self.input2_atr]

    def get_output(self):
        pass
