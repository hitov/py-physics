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

def main():

	x_size = 1000
	y_size = 800
	
	pygame.init()
	screen = pygame.display.set_mode((x_size,y_size))
	screen.fill((0, 0, 0))
	s = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
	pygame.gfxdraw.aacircle(s, 250, 250, 200, (0, 0, 0))
	pygame.gfxdraw.aacircle(s, x_size/2, y_size/2, 4, (0, 255, 0))	
	screen.blit(s, (0, 0))
	pygame.display.flip()


	r0 = Vector([5.0, 0.0, 10.0])
	v0 = Vector([0.0, -0.028, 0.0])
	a  = Vector([0.0, 0.0, 0.0])
	
	gama = 0.0000234
	M = 1000
	m = 2
	
	t = 0.0
	dt = 0.01
	
	r = r0
	v = v0

	while(1):	
		x = int(10*r[0])+x_size/2
		y = int(10*r[1])+y_size/2
		pygame.gfxdraw.aacircle(s, x, y, 1, (0, 255, 0))
		screen.blit(s, (0, 0))
		pygame.display.flip()
		
		a = - gama*M*r/( r*r * sqrt(r*r) )
		r0 = r
		v0 = v
		r = r0 + v0*t + (a*t*t)
		v = v0 + a*t
		t = t + dt
		
		pygame.gfxdraw.aacircle(s, x, y, 1, (0, 0, 0))
		screen.blit(s, (0, 0))
		pygame.display.flip()
	    
	return 0

if __name__ == '__main__':
	main()
