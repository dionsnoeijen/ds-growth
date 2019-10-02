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

from . Sources import Sources
from . Vein import Vein
from . VeinClusterObject import VeinClusterObject
from . Material import Material
from .. DebugDraw import DebugDraw
from mathutils import Vector

class VeinGrowth(object):

	def __init__(
		self,
		growth_start,
		particle_emitter,
		properties,
		report,
		sources
	):
		self.growth_start = growth_start
		self.particle_emitter = particle_emitter
		self.properties = properties
		self.report = report
		self.sources = sources

		self.clusters = []
		self.veins = [ Vein(
			self.growth_start.location,
			self.sources,
			self.properties.growth_increase
		) ]
		self.material = Material()

		self.stop = False
		self._vein_cluster = VeinClusterObject(self.properties, self.material)
		self._vein_cluster.add_vertex(self.growth_start.location, 0)

		self.start()

	def start(self):
		self.iteration = 0
		if self.properties.autostop:
			while not self.stop:
				self.iteration+=1
				self.grow()
		else:
			for index in range(0, self.properties.iterations):
				self.iteration = index
				self.grow()

		if self.properties.draw_veins_individually:
			for vein in self.veins:
				self.draw_vein(vein)
		else:
			if not self.properties.frame_by_frame:
				self._vein_cluster.draw()

	def reset_vein_point_sources(self) -> None:
		for vein in self.veins:
			if not vein.dead:
				for point in vein.points:
					point.reset_found()

	def sources_find_closest_vein_point(self) -> None:
		for source_index,source in enumerate(self.sources.sources):
			if not source.dead:
				distance = 0
				closest_vein = {
					'vein_index': None,
					'point_index': None,
					'source_index': None 
				}
				for vein_index,vein in enumerate(self.veins):
					if not vein.dead:
						for point_index,point in enumerate(vein.points):
							vector_between_source_and_point = point.location-source.location
							direction = vector_between_source_and_point.normalized()
							found_distance = vector_between_source_and_point.magnitude

							if distance == 0:
								distance = found_distance

							ray_inside = True
							if self.properties.stay_inside and not point.dead:
								cast_result = self.particle_emitter.ray_cast(
									source.location,
									direction,
									distance=found_distance
								)
								if cast_result[0] == True:
									ray_inside = False

							if ray_inside and \
								(vein_index == 0 and \
								 point_index == 0 or \
								 found_distance < distance):
									distance = found_distance
									closest_vein['vein_index'] = vein_index
									closest_vein['point_index'] = point_index
									closest_vein['source_index'] = source_index

				if closest_vein['vein_index'] is not None:
					if distance < self.properties.growth_increase:
						source.dead = True
						DebugDraw.draw_death_block(source.location)
					self.veins[closest_vein['vein_index']] \
						.get_point(closest_vein['point_index']) \
						.add_found_source(closest_vein['source_index'])


	def try_create_new_vein(self, vein: Vein) -> None:
		tip_index = vein.get_tip_index()
		for point_index,point in enumerate(vein.points):
			found = point.found_sources
			if point_index != tip_index:
				if len(found) > 0:
					new_vein = Vein(
						point.location,
						self.sources,
						self.properties.growth_increase
					)
					# This happends when growth is from within
					# the emitter, make sure it will be before_last
					if point.cluster_vertex_index == None:
						# This fixes the first two branches stat will connect
						# wrong at the base. I don't know why this happends though
						if vein.before_last == 1 or vein.before_last == 2:
							new_vein.before_last = 0
						else:
							new_vein.before_last = vein.before_last
					else:
						new_vein.before_last = point.cluster_vertex_index

					new_point = new_vein.get_root()
					new_point.found_sources = found
					self.veins.append(new_vein)
			else:
				if len(found) == 0:
					vein.dead = True

	def add_to_cluster(self, vein: Vein) -> None:
		tip = vein.get_tip()
		if tip.cluster_vertex_index == None:
			line = [ vein.before_last ]
			self._vein_cluster.add_vertex(tip.location, self.iteration)
			last_index = self._vein_cluster.last_vertex_index()
			tip.cluster_vertex_index = last_index
			line.append(tip.cluster_vertex_index)
			vein.before_last = tip.cluster_vertex_index
			self._vein_cluster.add_line(tuple(line))

	def draw_vein(self, vein: Vein) -> None:
		'''This will draw the vein as an individual object'''
		vein.draw()

	def draw_for_animation(self) -> None:

		vein_cluster = self._vein_cluster.draw()

		vein_cluster.hide_render = True
		vein_cluster.hide_viewport = True
		vein_cluster.keyframe_insert(data_path="hide_render", frame=1)
		vein_cluster.keyframe_insert(data_path="hide_viewport", frame=1)
		vein_cluster.hide_render = False
		vein_cluster.hide_viewport = False
		vein_cluster.keyframe_insert(data_path="hide_render", frame=self.iteration)
		vein_cluster.keyframe_insert(data_path="hide_viewport", frame=self.iteration)

		for cluster in self.clusters:
			if cluster.hide_render != True and \
				cluster.hide_viewport != True:

				cluster.hide_render = True
				cluster.hide_viewport = True
				cluster.keyframe_insert(data_path="hide_render", frame=self.iteration)
				cluster.keyframe_insert(data_path="hide_viewport", frame=self.iteration)

		self.clusters.append(vein_cluster)

	def grow(self) -> None:
		self.reset_vein_point_sources()
		self.sources_find_closest_vein_point()

		all_dead = True
		for vein in self.veins:
			if not vein.dead:
				all_dead = False
				self.try_create_new_vein(vein)
				vein.grow()
				if not self.properties.draw_veins_individually:
					self.add_to_cluster(vein)

		if self.properties.frame_by_frame:
			self.draw_for_animation()

		if all_dead:
			print('All dead at iteration: ', self.iteration)
			self.report.report({'INFO'}, 'All dead at iteration: %s' % (self.iteration))
			if self.properties.autostop:
				self.stop = True

