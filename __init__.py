# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "DS - Growth",
    "author": "Dion Snoeijen <hallo@dionsnoeijen.nl>",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Growing algorithm for particle systems",
    "warning": "This addon is in alpha",
    "wiki_url": "#",
    "tracker_url": "https://github.com/dionsnoeijen/ds-growth/issues",
    "category": "Mesh"
}

if "bpy" in locals():
    import importlib
    importlib.reload(DsGrowthProperties)
    importlib.reload(OBJECT_PT_DsGrowthGenerate)
    importlib.reload(DsGrowth_OT_Generate)

else:
    from . ui.properties import DsGrowthProperties
    from . ui.panels import OBJECT_PT_DsGrowthGenerate
    from . operators.generate import DsGrowth_OT_Generate

classes = (
    DsGrowthProperties,
    OBJECT_PT_DsGrowthGenerate,
    DsGrowth_OT_Generate
)

import bpy

from bpy.props import PointerProperty

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.dsgrowth_properties = PointerProperty(type=DsGrowthProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    del bpy.types.Scene.dsgrowth_properties

if __name__ == "__main__":
    register()
