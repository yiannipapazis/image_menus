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
    "name" : "Image Menus",
    "author" : "Yianni Papazis",
    "description" : "Some menus for making working with images easier.",
    "blender" : (2, 90, 0),
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
        # TODO make recent images reload
        # layout.label(text="Recent")
        # layout.label(text="Images")
        image_list = get_images_from_objects()
        
        if image_list:
            image_data = [img.image.name for img in image_list]
            o = layout.operator(reload_image_by_name.bl_idname, text="Reload All", icon="FILE_REFRESH")
            o.reload_list = True
            o.image_name = str(image_data)

            layout.separator()

            for image_node in image_list:
                image = image_node.image
                o = layout.operator(reload_image_by_name.bl_idname, text=image.name, icon='IMAGE_DATA')
                o.reload_list = False
                o.image_name = image.name
        else:
            layout.label("No images")

class reload_image_by_name(bpy.types.Operator):
    bl_idname = "object.reload_image_by_name"
    bl_label = "Reload Image by Name"
    image_name = bpy.props.StringProperty()
    reload_list = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        if self.image_name:
            if not self.reload_list:
                bpy.data.images[self.image_name].reload()
            else:
                # converting string list to list
                # probably doing this in a stupid
                image_list = self.image_name[1:-1].split(',')
                image_list = [img.strip(' ')[1:-1] for img in image_list]

                for image in image_list:
                    bpy.data.images[image].reload()
        return {'FINISHED'}

class load_from_selected_menu(bpy.types.Menu):
    bl_idname = "load_from_selected_menu"
    bl_label = "Load from Selected"
    bl_space_type = "IMAGE_EDITOR"

    class operator(bpy.types.Operator):
        bl_idname = "load_from_selected.my_class_name"
        bl_label = "Load From Selected"
        image_name = bpy.props.StringProperty()
    
        @classmethod
        def poll(cls, context):
            return True
    
        def execute(self, context):
            image = bpy.data.images[self.image_name]
            bpy.context.area.spaces.active.image = image
            return {"FINISHED"}
    

    def draw(self, context):
        layout = self.layout

        material_list = get_materials_from_selected()
        if material_list:
            for mat in material_list:
                layout.label(text=mat, icon='MATERIAL')
                layout.separator()
                mat_image_nodes = look_for_images_from_mat(
                    bpy.data.materials[mat])

                # build menu for each material
                if mat_image_nodes:
                    for image_node in mat_image_nodes:
                        o = layout.operator(
                            self.operator.bl_idname, text=image_node.image.name, icon='IMAGE_DATA')
                        o.image_name = image_node.image.name
                    layout.separator()
                else:
                    layout.label(text="No images")
        else:
            layout.label(text='No materials')

class make_active_from_selected_menu(bpy.types.Menu):
    bl_idname = "object.make_active_from_selected_menu"
    bl_label = "Make Image Active"
    image_name = ""

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
                layout.label(text=mat, icon='MATERIAL')
                layout.separator()
                mat_image_nodes = look_for_images_from_mat(
                    bpy.data.materials[mat])

                # build menu for each material
                if mat_image_nodes:
                    for image_node in mat_image_nodes:
                        o = layout.operator(
                            self.operator.bl_idname, text=image_node.image.name, icon='IMAGE_DATA')
                        o.mat_name = mat
                        o.node_name = str(image_node)
                    layout.separator()
                else:
                    layout.label(text="No images")
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
    load_from_selected_menu.operator,
    reload_image_by_name,
    make_active_from_selected_menu.operator,
    make_active_from_selected_menu
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
