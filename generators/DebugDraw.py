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

	def try_ray_cast():
		v_from = Vector((.9, -.2, .7))
		v_to = Vector((.2, -.2, .1))

		direction = v_to-v_from
		direction.normalize()

		bpy.ops.object.empty_add(location = v_from)
		bpy.ops.object.empty_add(location = v_to)

		cast_result = self.particle_emitter.ray_cast(
			v_from,
			direction
		)

		if cast_result[0]:
			print('FOUND')
			DebugDraw.draw_line_object([v_from, cast_result[1], v_to])
		else:
			print('NOT FOUND')
			DebugDraw.draw_line_object([v_from, v_to])

		print(cast_result)