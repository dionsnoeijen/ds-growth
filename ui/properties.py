import bpy

from bpy.props import *
from bpy.types import (Panel,Menu,Operator,PropertyGroup)

class DsGrowthProperties(PropertyGroup):

	growth_start: StringProperty(
		name='Start from'
	)
	particle_emitter: StringProperty(
		name='Particle emitter'
	)