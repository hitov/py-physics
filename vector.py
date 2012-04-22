#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2012 Angel Hitov <bango@bango-desktop>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from numpy import *

import pygame
import pygame.gfxdraw

class Vector:
  
  def __init__(self, data):
    self.data = data
    
  def __repr__(self):
    return repr(self.data)  
    
  def __getitem__(self, index):
    return self.data[index]
      
  def __add__(self, other):
	data = []
	for j in range(len(self.data)):
		data.append(self.data[j] + other.data[j])
	return Vector(data)
  
  def __radd__(self, other):
	return( self.__add__(other) )
	
  def __sub__(self, other):
	data = []
	for j in range(len(self.data)):
		data.append(self.data[j] - other.data[j])
	return Vector(data)
  
  def __rsub__(self, other):
	return( self.__sub__(other) )
	
  def __mul__(self, other):
	if isinstance(other,Vector):
		result = 0
		for j in range(len(self.data)):
			result += self.data[j]*other.data[j]
		return result
	else:
		data = []
		for j in range(len(self.data)):
			data.append(self.data[j]*other)
        return Vector(data)
        
  def __div__(self, other):
	data = []
	for j in range(len(self.data)):
		data.append(self.data[j]/other)
	return Vector(data)
    
  def __rmul__(self, other):
	return( self.__mul__(other) )
  
  def __xor__(self, other):
	data = []
	length = len(self.data)
	for i in range(length):
		idx_a = i + 1
		idx_b = i + 2
		idx_c = i - 1
		idx_d = i - 2
		if idx_a >= length:
			idx_a = idx_a - length
		if idx_b >= length:
			idx_b = idx_b - length

		if idx_c < 0:
			idx_c = length + idx_c
		if idx_d < 0:
			idx_d = length + idx_d

		data.append(self.data[idx_a] * other[idx_b] - self.data[idx_c] * other[idx_d])
	return Vector(data)

class DisplaySpace:
	def __init__(self, x_real_size, y_real_size, z_real_size, x_view_size = 1000, y_view_size = 800, z_view_size = 800, color = (0, 255, 0)):
		self.x_real_size = x_real_size
		self.y_real_size = y_real_size		
		self.z_real_size = z_real_size
		self.x_view_size = x_view_size
		self.y_view_size = y_view_size
		self.z_view_size = z_view_size
		self.color = color
		
		pygame.init()		
		self.screen = pygame.display.set_mode((self.x_view_size, self.y_view_size))
		self.screen.fill((0, 0, 0))
	
	def DrawPoint(self, x, y, z, color):
		px = int((self.x_view_size/self.x_real_size)*x) + self.x_view_size/2
		py = int((self.y_view_size/self.y_real_size)*y) + self.y_view_size/2
		pygame.draw.circle(self.screen, color, (px, py), 2, 2)
	
	def DrawPoints(self, points):
		for p in points:
			self.DrawPoint(p.r[0], p.r[1], p.r[2], p.color)
		pygame.display.flip()

	def Clear(self):
		self.screen.fill([0,0,0])

class MaterialPoint():
	def __init__(self, mass, position, velocity, acceleration, color = (0,255,0)):
		self.m = mass
		self.r = position
		self.v = velocity
		self.a = acceleration
		self.color = color

def main():

	red = (255,0,0)
	green = (0,255,0)
	blue = (0,0,255)
	yellow = (255,255,0)
	white = (255,255,255)

	space = DisplaySpace(3*152098232000.0,3*152098232000.0,0)

	sun = MaterialPoint(1.98892e30, Vector([0.0, 0.0, 0.0]), Vector([0.0, 0.0, 0.0]), Vector([0.0, 0.0, 0.0]), yellow)

	mercury = MaterialPoint(3.3022e23, Vector([69816900000.0, 0.0, 0.0]), Vector([0.0, -47870, 0.0]), Vector([0.0, 0.0, 0.0]), yellow)
	
	earth = MaterialPoint(5.9742e24, Vector([152098232000.0, 0.0, 0.0]), Vector([0.0, -29000.78, 0.0]), Vector([0.0, 0.0, 0.0]), blue)

	venus = MaterialPoint(4.8685e24, Vector([108942109000.0, 0.0, 0.0]), Vector([0.0, -35000.02, 0.0]), Vector([0.0, 0.0, 0.0]), green)

	mars = MaterialPoint(6.4185e23, Vector([206644545000.0, 0.0, 0.0]), Vector([0.0, -26499, 0.0]), Vector([0.0, 0.0, 0.0]),red)



	moon = MaterialPoint(7.3477e22, Vector([152098232000.0 + 362570000, 0.0, 0.0]), Vector([0.0, -29000.78 + 1022, 0.0]), Vector([0.0, 0.0, 0.0]),white)

	bodies = [sun, mercury, venus, earth, mars, moon]

	
        gamma = 6.67300e-11 # m3 kg-1 s-2
	
	t = 0.0
	dt = 2600
	i = 0	
	running = True
	
	while(running):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		if(i%(10) == 0):
			space.Clear()	
			space.DrawPoints(bodies)


		#print "Earth velocity = ", sqrt(earth.v*earth.v) / 1000, "km/s"
		#print "Time = ", t / 3600 / 24 / 365, "yrs"

		for bodie1 in bodies:
			bodie1.a = Vector([0.0, 0.0, 0.0])
                        for bodie2 in bodies:
				if bodie2 != bodie1:
					r = bodie2.r - bodie1.r
					bodie1.a = bodie1.a + gamma*bodie2.m*r/( r*r * sqrt(r*r) )

			bodie1.r = bodie1.r + bodie1.v*dt + (bodie1.a*dt*dt)
			bodie1.v = bodie1.v + bodie1.a*dt

		t += dt
                i += 1
	return 0

if __name__ == '__main__':
	main()
