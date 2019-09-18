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

class VeinClusterObject(object):
	'''This draws the cluster as a whole'''

	def __init__(self, properties):
		self._verts = []
		self._lines = []
		self._iterations = {}
		self.properties = properties

	@property
	def verts(self) -> list:
		return self._verts

	@property
	def lines(self) -> list:
		return self._lines

	def add_vertex(self, vert, iteration: int) -> None:
		self._verts.append(vert)
		if iteration not in self._iterations:
			self._iterations.update({iteration: []})
		self._iterations[iteration].append(len(self._verts)-1)

	def last_vertex_index(self) -> int:
		return len(self._verts) - 1

	def add_line(self, line) -> None:
		self._lines.append(line)

	def make_uniform_width(self) -> None:
		bpy.ops.object.editmode_toggle()
		bpy.ops.mesh.select_all(action='SELECT')
		bpy.ops.transform.skin_resize(
			value=( self.properties.skin_size, self.properties.skin_size, self.properties.skin_size )
		)
		bpy.ops.object.editmode_toggle()

	def make_increase_width(self) -> None:
		size = self.properties.skin_size
		obj = bpy.context.active_object
		for iteration in self._iterations:
			size += self.properties.width_increase
		for iteration in self._iterations:
			for vert_index in self._iterations[iteration]:
				obj.data.skin_vertices[''].data[vert_index].radius = (size, size)
			size -= self.properties.width_increase

	def draw(self) -> None:
		name = 'vein-cluster'
		vein_cluster = bpy.data.meshes.new(name)
		vein_cluster_object = bpy.data.objects.new(name, vein_cluster)
		bpy.context.collection.objects.link(vein_cluster_object)
		vein_cluster.from_pydata(self._verts, self._lines, [])

		if not self.properties.vertex_only:
			bpy.context.view_layer.objects.active = vein_cluster_object
			bpy.ops.object.modifier_add(type='SKIN')
			if self.properties.uniform_width:
				self.make_uniform_width()
			else:
				self.make_increase_width()
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Skin')
			bpy.ops.object.modifier_add(type='SUBSURF')
			bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Subdivision')

		return vein_cluster_object
