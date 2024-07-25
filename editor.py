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
    print(f"Linking. 0: {app_data[0]} 1: {app_data[1]} S: {sender}")
    link = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    input_output_links[link] = (app_data[1], app_data[0])

def delink_callback(sender, app_data):
    # app_data -> link_id
    del input_output_links[app_data]
    dpg.delete_item(app_data)

def convert_cv_to_dpg_image(cv_image):
    data = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2RGBA)
    data = np.ravel(data)
    data = np.asarray(data, dtype=np.float32)
    data = np.true_divide(data, 255.0)
    return data

def generate_plain_texture(shape, color):
    data = []
    for i in range(0, shape[0] * shape[1]):
        data.append(color[0])
        data.append(color[1])
        data.append(color[2])
        data.append(color[3])

    return data

def load_texture(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    height, width, _ = img.shape
    dpg_image = convert_cv_to_dpg_image(img)

    tag = None

    with dpg.texture_registry(show=False):
        tag = dpg.add_dynamic_texture(width=width, height=height, default_value=dpg_image, label=img_path)

    return img, tag

def update_image_texture(sender, app_data, user_data):
    # user_data is the image item tag/id to target the image change
    cv_image, dpg_tag = load_texture(IMG_NAME)
    dpg.configure_item(user_data, texture_tag=dpg_tag)

def build_node_tree(dst_node):
    # TODO: This breaks if any link is missing

    input_nodes = [atr_to_node[get_output_atr_from_input_atr(atr)] for atr in dst_node.get_input_attributes()]
    tree_root_node = Node(dst_node.get_debug_name())
    rec_build_node_tree(tree_root_node, input_nodes)

    for pre, fill, node in RenderTree(tree_root_node):
        print("%s%s" % (pre, node.name))

def rec_build_node_tree(tree_parent_node, input_nodes):
    print(f"Parent: {tree_parent_node}")
    for node in input_nodes:
        print(f"  {node.get_debug_name()}")
        tree_node = Node(node.get_debug_name(), parent=tree_parent_node)
        print(f"  {tree_node}")
        rec_input_nodes = [atr_to_node[get_output_atr_from_input_atr(atr)] for atr in node.get_input_attributes()]
        if len(rec_input_nodes) > 0:
            rec_build_node_tree(tree_node, rec_input_nodes)

def apply_output(sender, app_data, user_data):
    # user_data is the destination node
    build_node_tree(user_data)

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


def calculate_output_image_window():
    window_width = 350
    window_height = 320
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    extra_margin_x = 25
    extra_margin_y = 48
    image_width = window_width * 0.95
    image_height = (window_height - 60)

    window_pos = (viewport_width - window_width - extra_margin_x, viewport_height - window_height - extra_margin_y)
    window_size = (window_width, window_height)
    image_size = (image_width, image_height)


    return (window_pos, window_size, image_size)

def on_viewport_updated():
    (window_pos, window_size, image_size) = calculate_output_image_window()
    dpg.set_item_pos("output_window", window_pos)
    # dpg.set_item_width("output_window", window_size[0])
    # dpg.set_item_height("output_window", window_size[1])
    # dpg.set_item_width("img_item", image_size[0])
    # dpg.set_item_height("img_item", image_size[1])

def app():
    with dpg.texture_registry(show=False):
        black_tex = generate_plain_texture((100, 100), (0 / 255, 0 / 255, 0 / 255, 255 / 255))
        dpg.add_dynamic_texture(width=100, height=100, default_value=black_tex, tag=BLACK_TEXTURE, label="BLACK_TEX")#, format=dpg.mvFormat_Float_rgba)

        white_tex = generate_plain_texture((100, 100), (255 / 255, 255 / 255, 255 / 255, 255 / 255))
        dpg.add_dynamic_texture(width=100, height=100, default_value=white_tex, tag=WHITE_TEXTURE, label="WHITE_TEX")#, format=dpg.mvFormat_Float_rgba)

    with dpg.window(label="Node editor", tag="PrimaryWindow"):
        with dpg.node_editor(callback=link_callback, delink_callback=delink_callback) as editor:
            def_src = create_source_node(None, None, editor)
            def_dst = create_dst_node(None, None, editor)
            create_test_node(None, None, editor)
            create_const_node(None,None, editor)
            # link_callback(editor, (def_src.output_atr, def_dst.input_atr))

    (window_pos, window_size, image_size) = calculate_output_image_window()
    with dpg.window(label="Output image", tag="output_window", no_close=True, no_collapse=True, no_resize=True, pos=window_pos, width=window_size[0], height=window_size[1]) as prev_window:
        image_item = dpg.add_image(BLACK_TEXTURE, width=image_size[0], height=image_size[1], tag="img_item")
        dpg.add_button(label="Save image", callback=update_image_texture, tag="btn", user_data=image_item)
        # dpg.add_button(label="Apply", callback=apply_output, tag="apply_btn", user_data=def_dst)

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

        with dpg.menu(label="Tools"):
            dpg.add_menu_item(label="Item registry", callback=lambda: dpg.show_tool(dpg.mvTool_ItemRegistry))

    dpg.set_primary_window("PrimaryWindow", True)

    for (atr, node) in atr_to_node.items():
        print(atr)


def frame():
    pass

def main():
    dpg.create_context()
    dpg.create_viewport(title="Editor", width=1200, height=720)
    dpg.set_viewport_vsync(True)
    dpg.set_viewport_resize_callback(on_viewport_updated)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    app()

    # while dpg.is_dearpygui_running():
    #     frame()
    #     dpg.render_dearpygui_frame()
    dpg.start_dearpygui()

    dpg.destroy_context()

if __name__ == "__main__":
    main()
