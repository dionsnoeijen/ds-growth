import bpy

from bpy.props import *
from bpy.types import (Panel,Menu,Operator,PropertyGroup)

class OBJECT_PT_DsGrowthGenerate(Panel):
	
	bl_idname = "OBJECT_PT_DsGrowthGenerate"
	bl_label = "DS-Growth - Generation"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "DS-Growth"
	
	def draw(self, context):
		layout = self.layout
		scene = context.scene
		dsgrowth_properties = scene.dsgrowth_properties

		layout.prop_search(dsgrowth_properties, "growth_start", scene, "objects")
		layout.prop_search(dsgrowth_properties, "particle_emitter", scene, "objects")

		layout.separator()
		layout.operator("object.dsgrowth_generate")


