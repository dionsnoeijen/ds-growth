import bpy
from .. generators.growth.BranchGrowth import BranchGrowth

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
			BranchGrowth(start_object, emitter_object)
		else:
			self.report({'ERROR'}, 'Select start and emitter')

		return {'FINISHED'}