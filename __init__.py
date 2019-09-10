
bl_info = {
    "name": "DS - Growth",
    "author": "Dion Snoeijen <hallo@dionsnoeijen.nl>",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Growing algorithm for particle systems",
    "warning": "",
    "wiki_url": "#",
    "tracker_url": "#",
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
