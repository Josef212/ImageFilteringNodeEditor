import dearpygui.dearpygui as dpg
import cv2
import numpy as np
from anytree import Node, RenderTree

from utils import *
from nodes.base_node import BaseNode
from nodes.source_node import *
from nodes.dst_node import *
from nodes.test_node import *
from nodes.const_node import *
from nodes.gaussian_blur_node import *
from nodes.invert_node import *
from nodes.canny_node import *
from nodes.weighted_merge_node import *
from nodes.one_to_n_channels_node import *

OUTPUT_IMAGE_ITEM_TAG = "img_item"
OUTPUT_WINDOW_TAG = "output_window"

atr_to_node = {}
def node_added(node):
    attributes = node.get_all_attributes()
    for atr in attributes:
        atr_to_node[atr] = node

input_output_links = {} # link_id : (input_atr, output_atr)
def get_output_atr_from_input_atr(input_atr):
    for _, pair in input_output_links.items():
        if pair[0] == input_atr:
            return pair[1]

    return None

def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    # TODO: Before linking we should validate it
    #   Input and output types should match
    #   No recursion ???
    # print(f"Linking. 0: {app_data[0]} 1: {app_data[1]} S: {sender}")

    link = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    input_output_links[link] = (app_data[1], app_data[0])

def delink_callback(sender, app_data):
    # app_data -> link_id

    del input_output_links[app_data]
    dpg.delete_item(app_data)

def update_image_texture(sender, app_data, user_data):
    # user_data is the image item tag/id to target the image change

    cv_image, dpg_tag = load_texture(IMG_NAME)
    dpg.configure_item(user_data, texture_tag=dpg_tag)

def rec_build_node_tree(tree_parent_node, input_nodes):
    for node in input_nodes:
        tree_node = Node(node.get_debug_name(), parent=tree_parent_node)
        tree_node.value = node
        rec_input_nodes = [atr_to_node[get_output_atr_from_input_atr(atr)] for atr in node.get_input_attributes()]
        if len(rec_input_nodes) > 0:
            rec_build_node_tree(tree_node, rec_input_nodes)

def build_node_tree(dst_node):
    # TODO: This breaks if any link is missing

    input_nodes = [atr_to_node[get_output_atr_from_input_atr(atr)] for atr in dst_node.get_input_attributes()]
    tree_root_node = Node(dst_node.get_debug_name())
    tree_root_node.value = dst_node
    rec_build_node_tree(tree_root_node, input_nodes)

    for pre, fill, node in RenderTree(tree_root_node):
        print("%s%s" % (pre, node.name))

    return tree_root_node

def apply_output(sender, app_data, user_data):
    # user_data is the destination node
    tree = build_node_tree(user_data)
    output = tree.value.get_output(tree)
    # print(output)

    if output is not None:
        height, width, channels = output.shape
        dpg_output = convert_cv_to_dpg_image(output)
        output_texture_tag = register_dpg_texture(dpg_output, "Output image", width, height, False)
        dpg.configure_item(OUTPUT_IMAGE_ITEM_TAG, texture_tag=output_texture_tag)

        # with dpg.window(label="Aaaa"):
        #     dpg.add_image(output_texture_tag, width=300, height=250)

def create_source_node(sender, app_data, user_data):
    # user_data is the editor id
    node = SourceNode()
    node.build_dpg(user_data)
    node_added(node)

    return node

def create_dst_node(sender, app_data, user_data):
    # user_data is the editor id
    node = DstNode()
    node.build_dpg(user_data, apply_output)
    node_added(node)

    return node

def create_test_node(sender, app_data, user_data):
    # user_data is the editor id
    node = TestNode()
    node.build_dpg(user_data)
    node_added(node)

    return node

def create_const_node(sender, app_data, user_data):
    # user_data is the editor id
    node = ConstNode()
    node.build_dpg(user_data)
    node_added(node)

    return node

def create_gaussian_blur_node(sender, app_data, user_data):
    # user_data is the editor id
    node = GaussianBlurNode()
    node.build_dpg(user_data)
    node_added(node)

    return node

def create_invert_node(sender, app_data, user_data):
    # user_data is the editor id
    node = InvertNode()
    node.build_dpg(user_data)
    node_added(node)

    return node

def create_canny_node(sender, app_data, user_data):
    # user_data is the editor id
    node = CannyNode()
    node.build_dpg(user_data)
    node_added(node)

    return node

def create_weighted_merge_node(sender, app_data, user_data):
    # user_data is the editor id
    node = WeightedMergeNode()
    node.build_dpg(user_data)
    node_added(node)

    return node

def create_one_to_n_channels_node(sender, app_data, user_data):
    # user_data is the editor id
    node = OneToNChannels()
    node.build_dpg(user_data)
    node_added(node)

    return node

def on_viewport_updated():
    (window_pos, _, __) = calculate_output_image_window()
    dpg.set_item_pos(OUTPUT_WINDOW_TAG, window_pos)

def app():
    load_default_textures()

    with dpg.window(label="Node editor", tag="PrimaryWindow"):
        with dpg.node_editor(callback=link_callback, delink_callback=delink_callback) as editor:
            def_src = create_source_node(None, None, editor)
            def_dst = create_dst_node(None, None, editor)
            # create_test_node(None, None, editor)
            # create_const_node(None,None, editor)
            link_callback(editor, (def_src.output_atr, def_dst.input_atr))

    (window_pos, window_size, image_size) = calculate_output_image_window()
    with dpg.window(label="Output image", tag=OUTPUT_WINDOW_TAG, no_close=True, no_collapse=True, no_resize=True, pos=window_pos, width=window_size[0], height=window_size[1]) as prev_window:
        image_item = dpg.add_image(BLACK_TEXTURE, width=image_size[0], height=image_size[1], tag=OUTPUT_IMAGE_ITEM_TAG)
        dpg.add_button(label="Save image", callback=update_image_texture, tag="btn", user_data=image_item)

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save", callback=lambda: print("Save"))
            dpg.add_menu_item(label="Save as", callback=lambda: print("Save as"))

        dpg.add_menu_item(label="Help", callback=lambda: print("Helping"))

        with dpg.menu(label="Nodes"):
            dpg.add_menu_item(label="Source", callback=create_source_node, user_data=editor)
            dpg.add_menu_item(label="Dst", callback=create_dst_node, user_data=editor)
            dpg.add_menu_item(label="Test", callback=create_test_node, user_data=editor)
            dpg.add_menu_item(label="Const", callback=create_const_node, user_data=editor)
            dpg.add_menu_item(label="GaussianBlur", callback=create_gaussian_blur_node, user_data=editor)
            dpg.add_menu_item(label="Invert", callback=create_invert_node, user_data=editor)
            dpg.add_menu_item(label="Canny", callback=create_canny_node, user_data=editor)
            dpg.add_menu_item(label="Weighted merge", callback=create_weighted_merge_node, user_data=editor)
            dpg.add_menu_item(label="One to n channels", callback=create_one_to_n_channels_node, user_data=editor)

        with dpg.menu(label="Tools"):
            dpg.add_menu_item(label="Item registry", callback=lambda: dpg.show_tool(dpg.mvTool_ItemRegistry))
            dpg.add_menu_item(label="Debug tool", callback=lambda: dpg.show_tool(dpg.mvTool_Debug))

    dpg.set_primary_window("PrimaryWindow", True)

def main():
    dpg.create_context()
    dpg.create_viewport(title="Editor", width=1200, height=720)
    dpg.set_viewport_vsync(True)
    dpg.set_viewport_resize_callback(on_viewport_updated)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    app()

    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
