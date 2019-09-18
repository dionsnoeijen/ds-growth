import bpy

from bpy.props import *
from bpy.types import ( Panel, Menu, Operator, PropertyGroup )

class DsGrowthProperties(PropertyGroup):

	growth_start: StringProperty(
		name='Start from'
	)
	particle_emitter: StringProperty(
		name='Particle emitter'
	)
	skin_size: FloatProperty(
		name='Vein thickness',
		default=.1,
		max=10,
		min=0,
		soft_max=2
	)
	frame_by_frame: BoolProperty(
		name='Make growth per frame'
	)
	stay_inside: BoolProperty(
		name='Stay inside object'
	)
	# It should display width_increase when turned on,
	# for now width_increase is visible by default
	uniform_width: BoolProperty(
		default=True,
		name='Uniform width'
	)
	# Why would you want this? For example: 
	# If the growth needs to stop halfway the object.
	autostop: BoolProperty(
		default=True,
		name='Stop when all veins are dead'
	)
	draw_veins_individually: BoolProperty(
		name='Draw veins individually'
	)
	iterations: IntProperty(
		name='Iterations',
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
	width_increase: FloatProperty(
		name='Width increase',
		default=0.0005,
		max=1
	)