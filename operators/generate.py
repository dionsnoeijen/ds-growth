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

from .. generators.growth.VeinGrowth import VeinGrowth

class DsGrowth_OT_Generate(bpy.types.Operator):
	
	bl_idname = "object.dsgrowth_generate"
	bl_label = "Start Growth"
	bl_description = "Start the growth process"
	bl_options = {'REGISTER', 'UNDO'}

	def execute (self, context):
		scene = context.scene
		dsgrowth_properties = scene.dsgrowth_properties
		if dsgrowth_properties.growth_start in scene.objects and \
			dsgrowth_properties.particle_emitter in scene.objects:
			start_object = scene.objects[dsgrowth_properties.growth_start]
			emitter_object = scene.objects[dsgrowth_properties.particle_emitter]
			# Add new VeinGrowth instance for every start_object
			VeinGrowth(start_object, emitter_object, dsgrowth_properties)
		else:
			self.report({'ERROR'}, 'Select start and emitter')

		return {'FINISHED'}