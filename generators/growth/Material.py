import bpy

class Material(object):

	def __init__(self):
		self._material = bpy.data.materials.new('Vein')

	@property
	def material(self):
		return self._material
