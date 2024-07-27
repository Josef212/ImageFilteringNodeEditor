import dearpygui.dearpygui as dpg
import cv2
import numpy as np

from nodes.base_node import BaseNode
from utils import *

class EmbossedEdgesNode(BaseNode):
    node = None
    input_atr = None
    output_atr = None
    kernel = np.array([[0, -3, -3],
                       [3, 0, -3],
                       [3, 3, 0]])

    def __init__(self):
        pass

    def build_dpg(self, editor):
        with dpg.node(label="EmbossedEdges", parent=editor) as node:
            with dpg.node_attribute(label="InputAtr", attribute_type=dpg.mvNode_Attr_Input) as in_atr:
                dpg.add_text("Input")

            with dpg.node_attribute(label="OutputAtr", attribute_type=dpg.mvNode_Attr_Output) as out_atr:
                dpg.add_text("Output")

        self.node = node
        self.input_atr = in_atr
        self.output_atr = out_atr

    def get_all_attributes(self):
        return [self.input_atr, self.output_atr]

    def get_debug_name(self):
        return "EmbossedEdgesNode"

    def get_input_attributes(self):
        return [self.input_atr]

    def get_output(self, tree):
        input_tree_node = tree.children[0]
        input_node = input_tree_node.value
        img = input_node.get_output(input_tree_node)
        ret = cv2.filter2D(img, -1, kernel=self.kernel)

        return ret
