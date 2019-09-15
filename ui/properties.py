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
	skin_size: FloatProperty(
		name='Skin size',
		default=.1,
		max=10,
		min=0,
		soft_max=2
	)
	stay_inside: BoolProperty(
		name='Stay inside object'
	)
	draw_veins_individually: BoolProperty(
		name='Draw veins individually'
	)
	iterations: IntProperty(
		name='Iterations (temp)',
		default=100,
		max=200,
		min=1
	)
	growth_increase: FloatProperty(
		name='Growth increase',
		default=0.1,
		max=1,
		min=0.01
	)