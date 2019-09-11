import bpy

class VeinClusterObject(object):
	'''This draws the cluster as a whole'''

	def __init__(self):
		self._verts = []
		self._lines = []

	@property
	def verts(self):
		return self._verts

	@property
	def lines(self):
		return self._lines

	def add_vertex(self, vert) -> None:
		self._verts.append(vert)

	def last_vertex_index(self) -> int:
		return len(self._verts) - 1

	def add_line(self, line) -> None:
		self._lines.append(line)

	def draw(self):
		name = 'vein-cluster'
		vein_cluster = bpy.data.meshes.new(name)
		vein_cluster_object = bpy.data.objects.new(name, vein_cluster)
		bpy.context.collection.objects.link(vein_cluster_object)
		vein_cluster.from_pydata(self._verts, self._lines, [])
		vein_cluster.validate()

		# vein_cluster_object.modifier_add(type='SKIN')
		# vein_cluster_object.editmode_toggle()
		# bpy.ops.mesh.select_all(action='SELECT')
		# bpy.ops.transform.skin_resize(value=(0.1, 0.1, 0.1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		# vein_cluster_object.editmode_toggle()