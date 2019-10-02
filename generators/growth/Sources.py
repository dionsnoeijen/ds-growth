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
from . Source import Source

class Sources(object):

	def __init__(
		self,
		particle_emitter,
		growth_increase: int,
		report
	):
		self.particle_emitter = particle_emitter
		self._growth_increase = growth_increase
		self._report = report
		self._sources = []
		self.determine_sources()

	@property
	def sources(self) -> list:
		return self._sources

	def determine_sources(self) -> None:
		depsgraph = bpy.context.evaluated_depsgraph_get()
		eval_ob = self.particle_emitter.evaluated_get(depsgraph)
		if eval_ob.particle_systems and eval_ob.particle_systems[0]:
			particle_system = eval_ob.particle_systems[0]
			for particle in particle_system.particles:
				self._sources.append(Source(particle.location))
		else:
			raise ValueError('There is no particle system found on the object')

		before = self.how_many_sources_alive()
		self.kill_too_close()
		message = 'Reduced sources from %d to %d' % (before, self.how_many_sources_alive())
		self._report.report({'INFO'}, message)

	def how_many_sources_alive(self) -> int:
		counter = 0
		for source in self._sources:
			if not source.dead:
				counter+=1
		return counter

	def kill_too_close(self):
		'''Prevent particles from being too close to eachother'''
		for search in self._sources:
			for source in self._sources:
				if source is not search and source is not source.dead:
					vector_between_search_and_source = source.location-search.location
					found_distance = vector_between_search_and_source.magnitude
					if found_distance <= self._growth_increase:
						source.dead = True

