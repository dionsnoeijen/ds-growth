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
from . VeinPoint import VeinPoint
import math
import random
import string

class Vein(object):

	def __init__(self, start_location, sources, growth_increase):
		self._dead = False
		self._name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		self._points = [ VeinPoint(start_location, sources, self._name) ]
		self._before_last = 0
		self._directions = []
		self.sources = sources
		self.growth_increase = growth_increase

	@property
	def points(self) -> list:
		return self._points

	@property
	def dead(self):
		return self._dead

	@property
	def name(self):
		return self._name

	@property
	def before_last(self) -> int:
		return self._before_last
	
	@before_last.setter
	def before_last(self, before_last):
		self._before_last = before_last

	@dead.setter
	def dead(self, dead):
		for point in self._points:
			point.dead = True
		self._dead = dead

	def get_root(self):
		return self._points[0]

	def get_tip(self):
		return self._points[-1]

	def get_tip_index(self):
		return len(self._points) - 1

	def get_point(self, point_index) -> VeinPoint:
		return self._points[point_index]

	def draw(self, index: int):
		name = 'vein-' + str(index)
		growth_line = bpy.data.meshes.new(name)
		growth_line_object = bpy.data.objects.new(name, growth_line)
		bpy.context.collection.objects.link(growth_line_object)
		verts = []
		for point in self._points:
			verts.append(point.location)
		lines = []
		for index,vert in enumerate(verts):
			lines.append((index, index+1))
		del lines[-1]
		growth_line.from_pydata(verts, lines, [])

	def grow(self):
		if not self.dead:
			tip = self.get_tip()
			direction = tip.average_direction()
			if direction is not None:
				# Fix the growth of straight lines towards single
				# left out sources on the other side of the object
				if direction in self._directions:
					if len(tip.found_sources) == 1:
						source_index = tip.last_found_source_index()
						self.sources.sources[source_index].dead = True
				else:
					self._directions.append(direction)
				
				growth_vector = direction-tip.location
				growth_vector.normalize()
				growth_vector *= self.growth_increase
				growth_vector += tip.location
				self._points.append(VeinPoint(growth_vector, self.sources, self._name))
			

