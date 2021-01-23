# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

bl_info = {
    "name" : "Image Operators",
    "author" : "Yianni Papazis",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

addon_keymaps = []

class reload_images_menu(bpy.types.Menu):
    bl_idname = "reload_images_menu"
    bl_label = "Reload Images"
    bl_space_type = "3D_VIEW"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Recent")
        layout.label(text="Images")
        layout.label(text="Reload All", icon="FILE_REFRESH")
        image_list = get_images_from_objects()
        for image_node in image_list:
            image = image_node.image
            o = layout.operator(reload_image_by_name.bl_idname, text=image.name, icon='IMAGE_DATA')
            o.image_name = image.name

class reload_image_by_name(bpy.types.Operator):
    bl_idname = "object.reload_image_by_name"
    bl_label = "Reload Image by Name"
    image_name = bpy.props.StringProperty()

    def execute(self, context):
        if self.image_name:
            
            bpy.data.images[self.image_name].reload()
        return {'FINISHED'}

class load_from_selected_menu(bpy.types.Menu):
    bl_idname = "load_from_selected_menu"
    bl_label = "Load from Selected"
    bl_space_type = "IMAGE_EDITOR"

    def draw(self, context):
        layout = self.layout

        image_list = get_images_from_objects()

        for image in image_list:
            layout.label(text=image, icon='IMAGE_DATA')

class make_active_from_selected_menu(bpy.types.Menu):
    bl_idname = "object.make_active_from_selected_menu"
    bl_label = "Make Image Active"
    image_name = ""

    class menu(bpy.types.Menu):
        bl_idname = "object.make_active_from_image_menu"
        bl_label = "Material"
        mat_name = bpy.props.StringProperty()

        def draw(self, context):
            layout = self.layout
            mat_image_nodes = look_for_images_from_mat(bpy.data.materials[self.mat_name])
            operators = []
            if mat_image_nodes:
                for image_node in mat_image_nodes:
                    o = layout.operator(self.operator.bl_idname, text=image_node.image.name, icon='IMAGE_DATA')
                    o.mat_name = self.mat_name
                    o.node_name = str(image_node)
            else:
                layout.label(text="No images")

        class operator(bpy.types.Operator):
            bl_idname = "object.make_active_from_selected"
            bl_label = "Make Image Active"
            mat_name = bpy.props.StringProperty()
            node_name = bpy.props.StringProperty()

            def execute(self, context):

                node_tree = bpy.data.materials[self.mat_name].node_tree
                # TODO find a cleaner way of getting out node
                for each in node_tree.nodes:
                    if str(each) == self.node_name:
                        node = each
                node.select = True
                node_tree.nodes.active = node
                return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        material_list = get_materials_from_selected()
        if material_list:
            for mat in material_list:
                m = self.menu
                m.mat_name = mat
                layout.menu(m.bl_idname, text=mat, icon="MATERIAL")
        else:
            layout.label(text='No materials')

def get_images_from_objects():
    checked_mats = []
    images = []
    active_object = bpy.context.active_object
    materials = active_object.material_slots
    for mat in materials:
        mat = mat.material
        if mat not in checked_mats:
            checked_mats.append(mat)
            found_images = look_for_images_from_mat(mat)
            for img in found_images:
                if img not in images:
                    images.append(img)
    return images

def look_for_images_from_mat(mat = bpy.types.Material):
    image_list = []
    for node in mat.node_tree.nodes:
        if node.type == 'TEX_IMAGE' and node.image not in image_list:
            image_list.append(node)
    return image_list

def get_materials_from_selected():
    object_materials = []
    checked_mats = []
    active_object = bpy.context.active_object
    if active_object:
        materials = active_object.material_slots
        for mat in materials:
            mat = mat.name
            if mat not in checked_mats:
                checked_mats.append(mat)
                object_materials.append(mat)
    return object_materials

classes = (
    reload_images_menu,
    load_from_selected_menu,
    reload_image_by_name,
    make_active_from_selected_menu.menu.operator,
    make_active_from_selected_menu,
    make_active_from_selected_menu.menu
)

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    # register keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(
        "wm.call_menu",
        type="R",
        value="PRESS",
        shift=True
        )
    kmi.properties.name = reload_images_menu.bl_idname
    addon_keymaps.append((km,kmi))

    km = kc.keymaps.new(name="Image", space_type="IMAGE_EDITOR")
    kmi = km.keymap_items.new(
        "wm.call_menu",
        type="I",
        value="PRESS",
        shift=True
        )
    kmi.properties.name = load_from_selected_menu.bl_idname
    addon_keymaps.append((km,kmi))

    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(
        "wm.call_menu",
        type="I",
        value="PRESS",
        shift=True
    )
    kmi.properties.name = make_active_from_selected_menu.bl_idname
    addon_keymaps.append((km,kmi))

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Unregister keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    
    addon_keymaps.clear()
