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
from nodes.oil_node import *
from nodes.stylization_node import *
from nodes.hdr_node import *
from nodes.embossed_edges import *
from nodes.resize_node import *

OUTPUT_IMAGE_ITEM_TAG = "img_item"
OUTPUT_WINDOW_TAG = "output_window"

atr_to_node = {}
def node_added(node):
    global atr_to_node
    attributes = node.get_all_attributes()
    for atr in attributes:
        atr_to_node[atr] = node

input_output_links = {} # link_id : (input_atr, output_atr)
def get_output_atr_from_input_atr(input_atr):
    global input_output_links
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

    global input_output_links
    link = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    input_output_links[link] = (app_data[1], app_data[0])

def delink_callback(sender, app_data):
    # app_data -> link_id

    global input_output_links
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

output_image_texture_tag = None
def apply_output(sender, app_data, user_data):
    # user_data is the destination node
    tree = build_node_tree(user_data)
    output = tree.value.get_output(tree)

    global output_image_texture_tag
    if output_image_texture_tag is not None:
        dpg.delete_item(output_image_texture_tag)
        output_image_texture_tag = None

    if output is not None:
        height, width, channels = output.shape
        dpg_output = convert_cv_to_dpg_image(output)
        output_image_texture_tag = register_dpg_texture(dpg_output, "Output image", width, height, False)


    output_texture_tag = BLACK_TEXTURE if output_image_texture_tag is None else output_image_texture_tag
    dpg.configure_item(OUTPUT_IMAGE_ITEM_TAG, texture_tag=output_texture_tag)
        # with dpg.window(label="Aaaa"):
        #     dpg.add_image(output_texture_tag, width=300, height=250)

def create_dst_node(sender, app_data, user_data):
    # user_data is the editor id
    node = DstNode()
    node.build_dpg(user_data, apply_output)
    node_added(node)

    return node

def create_node(builder_cbk, editor):
    node = builder_cbk()
    node.build_dpg(editor)
    node_added(node)

    return node

def on_viewport_updated():
    (window_pos, _, __) = calculate_output_image_window()
    dpg.set_item_pos(OUTPUT_WINDOW_TAG, window_pos)

def app():
    load_default_textures()

    with dpg.window(label="Node editor", tag="PrimaryWindow"):
        with dpg.node_editor(callback=link_callback, delink_callback=delink_callback) as editor:
            def_src = create_node(SourceNode, editor)
            def_dst = create_dst_node(None, None, editor)
            # create_test_node(None, None, editor)
            # create_const_node(None,None, editor)
            # link_callback(editor, (def_src.output_atr, def_dst.input_atr))

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
            with dpg.menu(label="Data"):
                data_nodes = [
                    ("Source", lambda: create_node(SourceNode, editor)),
                    ("Dst", create_dst_node),
                    ("Const", lambda: create_node(ConstNode, editor))
                ]
                for label, cbk in data_nodes:
                    dpg.add_menu_item(label=label, callback=cbk, user_data=editor)

            with dpg.menu(label="Utils"):
                utils_nodes = [
                    ("Weighted merge", lambda: create_node(WeightedMergeNode, editor)),
                    ("One to n channels", lambda: create_node(OneToNChannels, editor))
                    ("Resize", lambda: create_node(ResizeNode, editor)),
                ]
                for label, cbk in utils_nodes:
                    dpg.add_menu_item(label=label, callback=cbk, user_data=editor)

            with dpg.menu(label="Effects"):
                effect_nodes = [
                    ("GaussianBlur", lambda: create_node(GaussianBlurNode, editor)),
                    ("Invert", lambda: create_node(InvertNode, editor)),
                    ("Canny", lambda: create_node(CannyNode, editor)),
                    ("Oil", lambda: create_node(OilNode, editor)),
                    ("Stylization", lambda: create_node(StylizationNode, editor)),
                    ("Hdr", lambda: create_node(HdrNode, editor)),
                    ("EmbossedEdgesNode", lambda: create_node(EmbossedEdgesNode, editor))
                ]
                for label, cbk in effect_nodes:
                    dpg.add_menu_item(label=label, callback=cbk, user_data=editor)

            dpg.add_menu_item(label="Test", callback=lambda: create_node(TestNode, editor), user_data=editor)

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
