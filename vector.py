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
	
i = Vector([1.0, 0.0, 0.0])
j = Vector([0.0, 1.0, 0.0])
k = Vector([0.0, 0.0, 1.0])

def v2(x):
	return (2*i+3*j+x*k)*x

def play1():
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    screen.fill((255, 0, 0))
    s = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    pygame.gfxdraw.aacircle(s, 250, 250, 200, (0, 0, 0))
    screen.blit(s, (0, 0))
    pygame.display.flip()
    try:
        while 1:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
            pygame.display.flip()
    finally:
        pygame.quit()

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
		self.s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
		#pygame.gfxdraw.aacircle(self.s, self.x_view_size/2, self.y_view_size/2, 4, (0, 255, 0))  
		self.screen.blit(self.s, (0, 0))
		pygame.display.flip()
	
	def DrawPoint(self, x, y, z):
		px = int((self.x_view_size/self.x_real_size)*x) + self.x_view_size/2
		py = int((self.y_view_size/self.y_real_size)*y) + self.y_view_size/2
		#print px, py
		pygame.gfxdraw.aacircle(self.s, px, py, 1, self.color)
		self.screen.blit(self.s, (0, 0))
		pygame.display.flip()
	def ClearPoint(self, x, y, z):
		pygame.gfxdraw.aacircle(self.s, int((self.x_view_size/self.x_real_size)*x) + self.x_view_size/2, int((self.y_view_size/self.y_real_size)*y) + self.y_view_size/2, 1, (0,0,0))
		self.screen.blit(self.s, (0, 0))
		pygame.display.flip()
	
	def DrawPoints(self,points):
		for p in points:
			self.DrawPoint(p[0], p[1], p[2])
	def Clear(self):
		self.screen.fill((0, 0, 0))	
		self.screen.blit(self.s, (0, 0))
		pygame.display.flip()


class MaterialPoint():
	def __init__(self, mass, position, velocity, acceleration):
		self.m = mass
		self.r = position
		self.v = velocity
		self.a = acceleration

def main():
	space = DisplaySpace(4*152098232000.0,4*152098232000.0,0)

	sun = MaterialPoint(1.98892e30, Vector([0.0, 0.0, 0.0]), Vector([0.0, 0.0, 0.0]), Vector([0.0, 0.0, 0.0]))
	earth = MaterialPoint(5.9742e24, Vector([152098232000.0, 0.0, 0.0]), Vector([0.0, -29000.78, 0.0]), Vector([0.0, 0.0, 0.0]))

	venus = MaterialPoint(4.8685e24, Vector([108942109000.0, 0.0, 0.0]), Vector([0.0, -35000.02, 0.0]), Vector([0.0, 0.0, 0.0]))

	mars = MaterialPoint(5.9742e24, Vector([152098232000.0, 2*152098232000.0, 0.0]), Vector([0.0, -29000.78, 0.0]), Vector([0.0, 0.0, 0.0]))

	bodies = [sun, earth, venus, mars ]
         	
        gamma = 6.67300e-11 # m3 kg-1 s-2
	
	t = 0.0
	dt = 360

	while(1):	
		for bodie in bodies:		
			space.DrawPoint(bodie.r[0],bodie.r[1],bodie.r[2])
			#print bodie.r[0],bodie.r[1],bodie.r[2]

		for bodie1 in bodies:
			bodie1.a = Vector([0.0, 0.0, 0.0])
                        for bodie2 in bodies:
				if bodie2 != bodie1:
					r = bodie2.r - bodie1.r
					#print bodie1.a
					bodie1.a = bodie1.a + gamma*bodie2.m*r/( r*r * sqrt(r*r) )

#		bodies[0].a = Vector([0.0, 0.0, 0.0])
#		bodies[1].a = Vector([0.0, 0.0, 0.0])
		
#		r = bodies[1].r - bodies[0].r
#		bodies[0].a = bodies[0].a + gamma*bodies[1].m*r/( r*r * sqrt(r*r) )
	
#		r = bodies[0].r - bodies[1].r
#		bodies[1].a = bodies[1].a + gamma*(bodies[0].m)*r/( r*r * sqrt(r*r) )
		#print bodies[1].a

		for bodie in bodies:
			bodie.r = bodie.r + bodie.v*t + (bodie.a*t*t)
			bodie.v = bodie.v + bodie.a*t

		t = t + dt
		#space.ClearPoint(r_tmp[0],r_tmp[1],r_tmp[2])
		print t
	    
	return 0

if __name__ == '__main__':
	main()
