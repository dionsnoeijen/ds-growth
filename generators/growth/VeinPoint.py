import bpy
import math
from mathutils import Vector

class VeinPoint(object):

	def __init__(self, location, sources, for_vein):
		self._location = location
		self.sources = sources
		self._found_sources = []
		self._dead = False
		self.for_vein = for_vein
		self._cluster_vertex_index = None

	@property
	def location(self):
		return self._location

	@property
	def dead(self):
		return self._dead

	@dead.setter
	def dead(self, dead):
		self._dead = dead

	@property
	def found_sources(self) -> list:
		return self._found_sources

	@found_sources.setter
	def found_sources(self, found_sources):
		self._found_sources = found_sources

	def add_found_source(self, source_index: int) -> None:
		self._found_sources.append(source_index)

	def reset_found(self) -> None:
		self._found_sources = []

	@property
	def cluster_vertex_index(self):
		return self._cluster_vertex_index

	@cluster_vertex_index.setter
	def cluster_vertex_index(self, vertex_index: int) -> None:
		self._cluster_vertex_index = vertex_index

	def average_direction(self) -> Vector:
		found_sources_count = len(self._found_sources);
		if found_sources_count == 0:
			return None
		average_location = Vector((.0,.0,.0))
		for source_index in self._found_sources:
			source = self.sources.sources[source_index]
			average_location.xyz += source.location.xyz
		average_location.xyz /= found_sources_count;
		return average_location
