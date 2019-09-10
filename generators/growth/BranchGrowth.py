from . Sources import Sources
from . Vein import Vein
from mathutils import Vector

class BranchGrowth(object):

	def __init__(self, growth_start, particle_emitter):
		self.growth_start = growth_start
		self.particle_emitter = particle_emitter
		self.sources = Sources(self.particle_emitter)
		self.growth_increase = 0.1
		self.veins = [ Vein(self.growth_start.location, self.sources, self.growth_increase) ]
		for index in range(0, 100):
			self.grow()
		self.draw_branch()

	def reset_veins(self) -> None:
		for vein in self.veins:
			for point in vein.points:
				point.reset_found()

	def sources_find_closest_vein(self) -> None:
		for source_index,source in enumerate(self.sources.sources):
			if not source.dead:
				distance = 0
				closest_vein = {
					'vein_index': None,
					'point_index': None,
					'source_index': None 
				}
				for vein_index,vein in enumerate(self.veins):
					for point_index,point in enumerate(vein.points):
						vector_between_source_and_point = source.location.xyz-point.location.xyz
						found_distance = vector_between_source_and_point.magnitude
						if vein_index == 0 and point_index == 0 \
							or found_distance < distance:
							distance = found_distance
							closest_vein['vein_index'] = vein_index
							closest_vein['point_index'] = point_index
							closest_vein['source_index'] = source_index

				if closest_vein['vein_index'] is not None:
					if distance < self.growth_increase:
						source.dead = True
					self.veins[closest_vein['vein_index']] \
						.get_point(closest_vein['point_index']) \
						.add_found_source(closest_vein['source_index'])


	def try_create_new_branch(self) -> None:
		for vein in self.veins:
			tip_index = vein.get_tip_index()
			for point_index,point in enumerate(vein.points):
				found = point.found_sources
				if point_index != tip_index:
					if len(found) > 0:
						newvein = Vein(point.location, self.sources, self.growth_increase)
						newpoint = newvein.get_point(0)
						newpoint.found_sources = found
						self.veins.append(newvein)
				else:
					if len(found) == 0:
						vein.dead = True

	def grow_branch(self):
		for vein in self.veins:
			if not vein.dead:
				vein.grow()

	def draw_branch(self):
		for index,vein in enumerate(self.veins):
			vein.draw(index)

	def grow(self) -> None:
		self.reset_veins()
		self.sources_find_closest_vein()
		self.try_create_new_branch()
		self.grow_branch()
