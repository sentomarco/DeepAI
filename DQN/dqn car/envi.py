import numpy as np
from random import random, randint
import random
import matplotlib.pyplot as plt
import time
import math

from  map_reader import convert, update_plot

# map parameters
IN_D=30
OUT_D = 90
START_X = 10 #modified in update states
START_Y = 10 #modified in update states
START_ANGLE = 90
VELOCITY=5
VIEW_OUTLINE=10
VIEW_ANGLE=5
DANGER_OUTLINE=10
ROBOT_DIM=5


room=convert(IN_D, OUT_D, "./env/room1.png")

# actions mapping
action2rotation = [0,30,-30]    #Robot directions: forward, 30° left or right

counter=0

class robot():

	def __init__(self):

		self.angle = START_ANGLE #refers to the direction of the robot, of the head
		self.rotation = 0
		self.pos_x, self.pos_y = START_X, START_Y 
		self.sensor1_x, self.sensor1_y = 0, 0
		self.sensor2_x, self.sensor2_y = 0, 0
		self.sensor3_x, self.sensor3_y = 0, 0
		self.signal1, self.signal2, self.signal3 = 0, 0, 0
		
	def reset(self):
		self.angle = START_ANGLE #refers to the direction of the robot, of the head
		self.rotation = 0
		self.pos_x, self.pos_y = START_X, START_Y 
		self.sensor1_x, self.sensor1_y = 0, 0
		self.sensor2_x, self.sensor2_y = 0, 0
		self.sensor3_x, self.sensor3_y = 0, 0
		self.signal1, self.signal2, self.signal3 = 0, 0, 0
		

	def move(self, rotation, pos_goal):
		
		global room, counter
		
		print("Vado a ", rotation, "gradi")
		self.rotation = rotation
		self.angle = self.angle + self.rotation
		
		#velocity is the variation of dx dy between 2 steps
	
		self.pos_x = self.pos_x + VELOCITY*math.cos(math.radians(self.angle))
		self.pos_y = self.pos_y + VELOCITY*math.sin(math.radians(self.angle))

		#The sensor are placed at a distance from the center of 2 unit (the robot is 5x5 squares)
		self.sensor1_x = self.pos_x + 2*math.cos(math.radians(self.angle))
		self.sensor1_y = self.pos_y + 2*math.sin(math.radians(self.angle))
		self.sensor2_x = self.pos_x + 2*math.cos(math.radians(self.angle + 30 ))
		self.sensor2_y = self.pos_y + 2*math.sin(math.radians(self.angle + 30))
		self.sensor3_x = self.pos_x + 2*math.cos(math.radians(self.angle - 30 ))
		self.sensor3_y = self.pos_y + 2*math.sin(math.radians(self.angle - 30))

		#signal defined both by seeing an obstacole or beeing too near to the outline

		#if near an obstacle
		self.signal1 = int(np.sum( room[ int(self.sensor1_x)-VIEW_ANGLE:int(self.sensor1_x)+VIEW_ANGLE, int(self.sensor1_y)-VIEW_ANGLE:int(self.sensor1_y)+VIEW_ANGLE ])/(VIEW_ANGLE^2))
		
		self.signal2 = int(np.sum( room[int(self.sensor2_x)-VIEW_ANGLE:int(self.sensor2_x)+VIEW_ANGLE, int(self.sensor2_y)-VIEW_ANGLE:int(self.sensor2_y)+VIEW_ANGLE])/(VIEW_ANGLE^2))
		
		self.signal3 = int(np.sum( room[int(self.sensor3_x)-VIEW_ANGLE:int(self.sensor3_x)+VIEW_ANGLE, int(self.sensor3_y)-VIEW_ANGLE:int(self.sensor3_y)+VIEW_ANGLE])/(VIEW_ANGLE^2))

		#if near the outline
		if self.sensor1_x>OUT_D-VIEW_OUTLINE or self.sensor1_x<VIEW_OUTLINE or self.sensor1_y>OUT_D-VIEW_OUTLINE or self.sensor1_y<VIEW_OUTLINE:
			self.signal1 = 1
		if self.sensor2_x>OUT_D-VIEW_OUTLINE or self.sensor2_x<VIEW_OUTLINE or self.sensor2_y>OUT_D-VIEW_OUTLINE or self.sensor2_y<VIEW_OUTLINE:
			self.signal2 = 1
		if self.sensor3_x>OUT_D-VIEW_OUTLINE or self.sensor3_x<VIEW_OUTLINE or self.sensor3_y>OUT_D-VIEW_OUTLINE or self.sensor3_y<VIEW_OUTLINE:
			self.signal3 = 1

		pos_r=(self.pos_x,self.pos_y)
		
		# update the plot of the movement 
		#if counter%5==0: update_plot(room, pos_r, self.angle, ROBOT_DIM, pos_goal)
		counter+=1

class Enviroment():

	def  __init__(self, num_actions, num_rewards):
	
		self.robot=robot()
		
		self.goal = (OUT_D -10,OUT_D-10)
		self.steps = 0
		self.last_steps = 0
		self.last_reward=0
		self.last_reward = 0
		self.last_distance = 0

			
	def reset(self):
		self.robot.reset()
		return [self.robot.signal1, self.robot.signal2, self.robot.signal3, self.robot.angle]
	
	def update_state(self, action):	
	
		global room, START_X, START_Y

		#xx = self.goal_x - self.robot.pos_x
		#yy = self.goal_y - self.robot.pos_y
		orientation =self.robot.angle
		last_signal = [self.robot.signal1, self.robot.signal2, self.robot.signal3, orientation]

		#update the DQN AI
		#action = brain.update(self.last_reward, last_signal)
		#results of the learning process
		#scores.append(brain.score())


		#next move
		rotation = action2rotation[action]
		self.robot.move(rotation, self.goal)
		distance = np.sqrt((self.robot.pos_x - self.goal[0])**2 + (self.robot.pos_y - self.goal[1])**2)

		self.steps += 1

		#rewards 

		# Going into a wall
		
		#self.robot.angle=
		
		if room[int(self.robot.pos_x), int(self.robot.pos_y)] > 0:

			#self.robot.velocity = Vector(1, 0).rotate(self.robot.angle)	??
			self.last_reward = -5

		else: 

			# driving away from objective reward
			#self.robot.velocity = Vector(6, 0).rotate(self.robot.angle) #??
			self.last_reward = -0.1 
			# driving towards objective reward
			if distance < self.last_distance:
				self.last_reward = 0.1

		# too close to edges of the wall on the "right"
		if self.robot.pos_x < DANGER_OUTLINE:
			self.robot.pos_x = DANGER_OUTLINE
			self.last_reward = -1 
		# too close to edges of the wall on the "left"
		if self.robot.pos_x > OUT_D - DANGER_OUTLINE:
			self.robot.pos_x = OUT_D - DANGER_OUTLINE
			self.last_reward = -1 
		# too close to edges of the "bottom" wall
		if self.robot.pos_y < DANGER_OUTLINE:
			self.robot.pos_y = DANGER_OUTLINE
			self.last_reward = -1 
		# too close to edges of the "upper" wall
		if self.robot.pos_y > OUT_D - DANGER_OUTLINE:
			self.robot.pos_y = OUT_D - DANGER_OUTLINE
			self.last_reward = -1 

		if distance < 20:

			#switch the position of the goal to make it start again to seek the goal
			#START_X, START_Y = self.goal_x, self.goal_y
			
			#self.goal_x = OUT_D-self.goal_x
			#self.goal_y = OUT_D-self.goal_y
			# reward for reaching the objective faster than last round (may want to scale this)
			self.last_reward = self.last_steps - self.steps 
			
			#reset the data
			self.last_steps = self.steps 
			self.steps = 0

		self.last_distance = distance
		
		done = (distance < 20)
		
		return last_signal, self.last_reward, done
		
