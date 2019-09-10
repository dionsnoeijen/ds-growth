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

	@dead.setter
	def dead(self, dead):
		self._dead = dead

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
				growth_vector = direction.xyz-tip.location.xyz
				growth_vector.normalize()
				growth_vector.xyz *= self.growth_increase
				growth_vector.xyz += tip.location.xyz
				self._points.append(VeinPoint(growth_vector, self.sources, self._name))
			

