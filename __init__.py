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
    bl_idname = "OBJECT_MT_reload_images_menu"
    bl_label = "Reload Images Menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Recent")
        layout.label(text="Images")

        image_list = ['image1', 'image_200.jpg', 'image_300.jpg']
        get_images_from_objects()

        for image in image_list:
            layout.label(text=image, icon='IMAGE_DATA')

def get_images_from_objects():
    active_object = bpy.context.active_object
    materials = active_object.material_slots
    for slot in materials:
        print(slot.material)
"""
classes = (
    reload_images_menu
)
"""

def register():
    bpy.utils.register_class(reload_images_menu)
    """
    for cls in classes:
        bpy.utils.register_class(cls)
    """
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

def unregister():
    bpy.utils.unregister_class(reload_images_menu)
