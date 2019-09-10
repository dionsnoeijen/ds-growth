import bpy
from . Source import Source

class Sources(object):

	def __init__(self, particle_emitter):
		self.particle_emitter = particle_emitter
		self._sources = []
		self.determine_sources()

	@property
	def sources(self):
		return self._sources

	def determine_sources(self):
		depsgraph = bpy.context.evaluated_depsgraph_get()
		eval_ob = self.particle_emitter.evaluated_get(depsgraph)
		particle_system = eval_ob.particle_systems[0]
		for particle in particle_system.particles:
			self._sources.append(Source(particle.location))
