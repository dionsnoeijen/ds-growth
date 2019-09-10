
class Source(object):

	def __init__(self, location):
		self._location = location
		self._dead = False

	@property
	def dead(self):
		return self._dead

	@property
	def location(self):
		return self._location

	@dead.setter
	def dead(self, dead):
		self._dead = dead
