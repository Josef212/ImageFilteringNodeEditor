import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

dpg.create_context()

def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)

def delink_callback(sender, app_data):
    # app_data -> link_id
    dpg.delete_item(app_data)

def create_empty_node(sender, app_data, user_data):
    node = dpg.add_node(label="New node", parent=user_data)
    input_atr = dpg.add_node_attribute(label="Input", parent=node)
    dpg.add_text(default_value="Src", parent=input_atr)

    atr = dpg.add_node_attribute(label="Preview", parent=node, attribute_type=dpg.mvNode_Attr_Static)
    dpg.add_text(default_value="Prev", parent=atr)

    out_atr = dpg.add_node_attribute(label="Output", parent=node, attribute_type=dpg.mvNode_Attr_Output)
    dpg.add_text(default_value="Out", parent=out_atr)

    return node

W = 100
H = 100
def load_plain_texture(width, height, r, g, b, a):
    buffer = []
    for i in range(0, width * height):
        buffer.append(r)
        buffer.append(g)
        buffer.append(b)
        buffer.append(a)
    return buffer

def update_texture(sender, app_data, user_data):
    tex = load_plain_texture(W, H, 1.0, 1.0, 1.0, 1.0)
    dpg.set_value("texture_tag", tex)

def load_test_image(sender, app_data, user_data):
    tex = []
    # TODO: Load img
    dpg.set_value("texture_tag", tex)

def create_source_image_node(sender, app_data, user_data):
    with dpg.node(label="Src image"):
        with dpg.node_attribute(label="Atr", attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_image("texture_tag", width=100, height=100)
            dpg.add_button(label="White", width=150, callback=update_texture)
            dpg.add_button(label="Test", width=150, callback=load_test_image)

with dpg.texture_registry(show=False):
    tex = load_plain_texture(W, H, 0.0, 0.0, 0.0, 1.0)
    dpg.add_dynamic_texture(width=W, height=H, default_value=tex, tag="texture_tag")

with dpg.window(label="Tutorial node editor", tag="PrimaryWindow"):
    EDITOR_TAG = "editor_id"

    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save", callback=lambda: print("Save"))
            dpg.add_menu_item(label="Save as", callback=lambda: print("Save as"))

        dpg.add_menu_item(label="Help", callback=lambda: print("Helping"))

        with dpg.menu(label="Nodes"):
            dpg.add_menu_item(label="Add node", tag="Im tagging", callback=create_empty_node, user_data=EDITOR_TAG)

    with dpg.node_editor(tag=EDITOR_TAG, callback=link_callback, delink_callback=delink_callback) as editor:
        create_source_image_node(None, None, EDITOR_TAG)
        create_empty_node(None, None, EDITOR_TAG)
        pass
        # with dpg.node(label="Node 1"):
        #     with dpg.node_attribute(label="Node A1"):
        #         dpg.add_input_float(label="F1", width=150)
        #
        #     with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
        #         dpg.add_input_float(label="F2", width=150)
        #
        # with dpg.node(label="Node 2"):
        #     with dpg.node_attribute(label="Node A3"):
        #         dpg.add_input_float(label="F3", width=200)
        #
        #     with dpg.node_attribute(label="Node A4", attribute_type=dpg.mvNode_Attr_Output):
        #         dpg.add_input_float(label="F4", width=200)

dpg.create_viewport(title="Testing", width=800, height=600)
dpg.set_viewport_vsync(True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("PrimaryWindow", True)

dpg.start_dearpygui()
dpg.destroy_context()
