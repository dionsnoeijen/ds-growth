import bpy

from . Sources import Sources
from . Vein import Vein
from . VeinClusterObject import VeinClusterObject
from .. DebugDraw import DebugDraw
from mathutils import Vector

class VeinGrowth(object):

	def __init__(self, growth_start, particle_emitter, properties):
		self.growth_start = growth_start
		self.particle_emitter = particle_emitter
		self.properties = properties
		self.sources = Sources(self.particle_emitter)
		self.veins = [ Vein(self.growth_start.location, self.sources, self.properties.growth_increase) ]

		self._vein_cluster = VeinClusterObject(self.properties)
		self._vein_cluster.add_vertex(self.growth_start.location)

		# DebugDraw.try_ray_cast()
		self.iteration = 0
		for index in range(0, self.properties.iterations):
			self.iteration = index
			self.grow()

		if self.properties.draw_veins_individually:
			for vein in self.veins:
				self.draw_vein(vein)
		else:
			self._vein_cluster.draw()

	def reset_vein_point_sources(self) -> None:
		for vein in self.veins:
			if not vein.dead:
				for point in vein.points:
					point.reset_found()

	def sources_find_closest_vein_point(self) -> None:
		# if self.iteration == 25:
		# 	print('WTF')
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
					self.veins[closest_vein['vein_index']] \
						.get_point(closest_vein['point_index']) \
						.add_found_source(closest_vein['source_index'])


	def try_create_new_vein(self, vein: Vein) -> None:
		tip_index = vein.get_tip_index()
		for point_index,point in enumerate(vein.points):
			found = point.found_sources
			if point_index != tip_index:
				if len(found) > 0:
					new_vein = Vein(point.location, self.sources, self.properties.growth_increase)
					# This happends when growth is from within
					# the emitter, make sure it will be before_last
					if point.cluster_vertex_index == None:
						new_vein.before_last = vein.before_last
					else:
						new_vein.before_last = point.cluster_vertex_index
					new_point = new_vein.get_root()
					new_point.found_sources = found
					self.veins.append(new_vein)
			else:
				if len(found) == 0:
					# DebugDraw.draw_death_block(vein.get_tip().location)
					vein.dead = True

	def add_to_cluster(self, vein: Vein) -> None:
		tip = vein.get_tip()
		if tip.cluster_vertex_index == None:
			line = [ vein.before_last ]
			self._vein_cluster.add_vertex(tip.location)
			last_index = self._vein_cluster.last_vertex_index()
			tip.cluster_vertex_index = last_index
			line.append(tip.cluster_vertex_index)
			vein.before_last = tip.cluster_vertex_index
			self._vein_cluster.add_line(tuple(line))

	def draw_vein(self, vein: Vein) -> None:
		'''This will draw the vein as an indivudual object'''
		vein.draw(0)

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

		if all_dead:
			print('All dead at iteration: ', self.iteration)

