import bpy

from mathutils import Vector

class DebugDraw:

	def draw_line_object(verts):
		name = 'debug-line-object'
		debug_line = bpy.data.meshes.new(name)
		debug_line_object = bpy.data.objects.new(name, debug_line)
		bpy.context.collection.objects.link(debug_line_object)

		lines = []
		for index,vert in enumerate(verts):
			lines.append((index, index+1))
		del lines[-1]

		debug_line.from_pydata(verts, lines, [])
		debug_line.validate()

	def draw_death_block(location: Vector):
		bpy.ops.mesh.primitive_cube_add(
			size=0.05,
			calc_uvs=True,
			enter_editmode=False,
			align='WORLD',
			location=location,
			rotation=(0.0, 0.0, 0.0)
		)
