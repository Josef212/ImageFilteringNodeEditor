import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

class DstNode(BaseNode):
    node = None
    input_atr = None

    image_item = None

    image_texture_tag = None
    cv_image = None

    def __init__(self):
        pass

    def build_dpg(self, editor, apply_cbk):
        with dpg.node(label="Dst", parent=editor) as node:
            with dpg.node_attribute(label="DstAtr", attribute_type=dpg.mvNode_Attr_Input) as atr:
                dpg.add_button(label="Apply", width=150, callback=apply_cbk, user_data=self)

        self.node = node
        self.input_atr = atr

    def get_all_attributes(self):
        return [self.input_atr]

    def get_debug_name(self):
        return "DstNode"

    def get_input_attributes(self):
        return [self.input_atr]

    def get_output(self, tree):
        input_tree_node = tree.children[0]
        input_node = input_tree_node.value
        return input_node.get_output(input_tree_node)
