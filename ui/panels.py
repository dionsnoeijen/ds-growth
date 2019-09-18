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

		layout.prop(dsgrowth_properties, 'stay_inside')

		layout.prop(dsgrowth_properties, 'uniform_width')
		if not dsgrowth_properties.uniform_width:
			layout.prop(dsgrowth_properties, 'width_increase')
			layout.separator()

		layout.prop(dsgrowth_properties, 'autostop')
		if not dsgrowth_properties.autostop:
			layout.prop(dsgrowth_properties, 'iterations')
			layout.separator()

		layout.prop(dsgrowth_properties, 'vertex_only')
		if not dsgrowth_properties.vertex_only:
			layout.prop(dsgrowth_properties, 'skin_size')
			layout.separator()

		layout.prop(dsgrowth_properties, 'frame_by_frame')
		layout.prop(dsgrowth_properties, 'growth_increase')

		layout.separator()
		layout.operator("object.dsgrowth_generate")

		# Maybe, sometime
		# layout.prop(dsgrowth_properties, 'draw_veins_individually')


