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


class reload_images_menu(bpy.types.Menu):
    bl_idname = "reload_images_menu"
    bl_label = "Reload Image"
    bl_space_type = "3D_VIEW"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Recent")
        layout.label(text="Images")
        layout.label(text="Reload All", icon="FILE_REFRESH")
        image_list = get_images_from_objects()
        for image in image_list:
            o = layout.operator(reload_image_by_name.bl_idname, text=image.name, icon='IMAGE_DATA')
            o.image_name = image.name

class reload_image_by_name(bpy.types.Operator):
    bl_idname = "object.reload_image_by_name"
    bl_label = "reload_image_by_name"
    image_name = bpy.props.StringProperty()

    def execute(self, context):
        if self.image_name:
            
            bpy.data.images[self.image_name].reload()
            print("hello")
        return {'FINISHED'}

class load_from_selected_menu(bpy.types.Menu):
    bl_idname = "load_from_selected_menu"
    bl_label = "Load from Selected"
    bl_space_type = "IMAGE_EDITOR"

    def draw(self, context):
        layout = self.layout

        test_list = ['image1', 'image2', 'image3']

        for image in test_list:
            layout.label(text=image, icon='IMAGE_DATA')

def get_images_from_objects():
    images = []
    checked_mats = []
    active_object = bpy.context.active_object
    materials = active_object.material_slots
    for mat in materials:
        mat = mat.material
        if mat not in checked_mats:
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image not in images:
                    images.append(node.image)
    return images

classes = (
    reload_images_menu,
    load_from_selected_menu,
    reload_image_by_name
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

    km = kc.keymaps.new(name="Image", space_type="IMAGE_EDITOR")
    kmi = km.keymap_items.new(
        "wm.call_menu",
        type="L",
        value="PRESS",
        shift=True
        )
    kmi.properties.name = load_from_selected_menu.bl_idname
def unregister():
    bpy.utils.unregister_class(reload_images_menu)

    # TODO unregister keymaps
