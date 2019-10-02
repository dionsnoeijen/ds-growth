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

	vertex_only: BoolProperty(
		name='Vertex only',
		default=False
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
	apply_modifiers: BoolProperty(
		default=False,
		name='Apply modifiers'
	)