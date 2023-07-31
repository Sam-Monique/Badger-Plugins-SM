#%%

import subprocess
import random
import os
import numpy as np
import matplotlib.pyplot as plt

#==============================================================================================================
#============================================ INPUT -- MODIFY HERE ============================================
#==============================================================================================================


# COSY parameters
xh = 0 # center of x distribution in mm
yh = 0 # center of x distribution in mm
widthX = 1.5/2 # half x- beam spot in mm
widthY = 1.5/2 # half y- beam spot in mm
dE = 0.0025 # half of total energy spread in fraction 1% = 0.01
#dE = 0.00 # half of total energy spread in fraction 1% = 0.01
aX = 10 # mrad
aY = 15 # mrad
anglesX = np.arange(5, 20, 3) # mrad
anglesY = np.arange(5, 20, 3) # mrad

numberMC = 400 # number of beam particles






#=============================================================================================================
# Function to replace of text in a file
def replace_line(file_nameOrig, file_nameTemp, line_num, text):
	lines = open(file_nameOrig, 'r').readlines()
	lines[line_num-1] = text
	out = open(file_nameTemp, 'w')
	out.writelines(lines)
	out.write('\n')
	out.close()


def replace_lines(file_nameOrig, file_nameTemp, line_nums, texts):
	lines = open(file_nameOrig, 'r').readlines()
	for i in range(len(line_nums)):
		lines[line_nums[i]-1] = texts[i]
	out = open(file_nameTemp, 'w')
	out.writelines(lines)
	out.write('\n')
	out.close()

# Function for adding a multiple lines of text in a file
def add_lines(file_nameOrig, file_nameTemp, line_num, text):
	lines = open(file_nameOrig, 'r').readlines()
	for i in range(numberMC):
		lines.append('\n')
	lines[(line_num+len(text)-1):] = lines[(line_num-1):]
	for i in range(len(text)):
		lines[line_num-1+i] = text[i]
	out = open(file_nameTemp, 'w')
	out.writelines(lines)
	out.write('\n')
	out.close()

def change_line(file_nameOrig,line_num, scale, types):
	lines = open(file_nameOrig, 'r').readlines()
	text = lines[line_num-1]
	split = text.split()
	new = ''
	if types in ['MQ','MH']:
		new += split[0] + ' ' +  split[1] + ' ' +  split[2] + '*' + str(scale) + \
			' ' + split[3] + '  			' + split[4] + '\n'
	elif types in ['M5']:
		new += split[0] +' ' + split[1] + ' ' + split[2] + '*' + str(scale) + ' ' + \
			split[3] + '*' + str(scale) + ' ' + split[4] + '*' + str(scale) + ' ' + \
				split[5] + '*' + str(scale) + ' ' + split[6] + '*' + str(scale) + ' ' +\
					split[7] + '  			' + split[8] + '\n'
	elif types in ['MC']:
		new += split[0] + ' ' + split[1] + "*" + str(scale)	+ ' ' + split[2] + ' ' + \
		split[3] + ' ' +split[4] + ' ' +split[5] + ' ' +split[6] + ' ' +split[7] + ' ' + \
		split[8] + '\n'



	return new
		
def targetPS(widthX, widthY, aX, aY):
	xT = [] # x-location of beam at target
	yT = [] # y-location of beam at target
	axT = [] # angleX-location of beam at target
	ayT = [] # angleY-location of beam at target

	for j in range(numberMC):
		# Sampling within ellipse of possible positions
		rng = np.random.RandomState(seed = j)
		rand_nums = rng.uniform(0,1, 5)
		# r = widthX * np.sqrt(random.uniform(0, 1))
		r = widthX * np.sqrt(rand_nums[0])
		# theta = random.uniform(0, 1) * 2 * np.pi
		theta = rand_nums[1] * 2 * np.pi
		x = xh + r * np.cos(theta)
		y = yh + widthY/widthX *  r * np.sin(theta)
		xT.append(x)
		yT.append(y)

		# Sampling within ellipse of possible angles
		# r = aX * np.sqrt(random.uniform(0, 1))
		r = aX * np.sqrt(rand_nums[2])

		# theta = random.uniform(0, 1) * 2 * np.pi
		theta = rand_nums[3] * 2 * np.pi

		angleX = r * np.cos(theta)
		if aX != 0:
			angleY = aY/aX *  r * np.sin(theta)
		else:
			# angleY = aY * np.sqrt(random.uniform(0, 1))
			angleY = aY * np.sqrt(rand_nums[4])

		axT.append(angleX)
		ayT.append(angleY)
	return (xT, yT, axT, ayT)


def set_vals(line_type,path,file):



	temp = file + 'TEMP' +  '.fox'

	line_num_list = []
	lines = []
	for mag in line_type:

		i = list(line_type.keys()).index(mag)
		line_num = line_type[mag][0]
		types = line_type[mag][1]
		scale = 1.0

		line = change_line(path+file + '.fox',line_num,scale,types)
		
		line_num_list.append(line_num)
		lines.append(line)

	replace_lines(path+file + '.fox', path +temp,line_num_list,lines)


def set_rays(path,file, dx = 0, dy = 0,  pencil = False):

	temp =  file + 'TEMP' +  '.fox'

	text = []
	xT, yT, axT, ayT = targetPS(widthX, widthY, aX, aY)
	for j in range(numberMC):
		ddE = np.round(random.uniform(-dE, dE),5)
		if pencil:
			text.append('SR '+ str(dx/1000) +' ' + str(0) +' ' \
			+ str(dy/1000) +' ' + str(0) + ' 0 ' + '0' + ' 0 0 1;\n')
		else:
			text.append('SR '+ str((xT[j]+dx)/1000) +' ' + str(axT[j]/1000) +' ' \
			+ str((yT[j]+dy)/1000) +' ' + str(ayT[j]/1000) + ' 0 ' + '0' + ' 0 0 1;\n')

	add_lines(path+file+'.fox',path+ temp, 736, text)


def run(path,file):
	subprocess.run(['powershell','-Command','cosy ' + path + file + 'TEMP'])
	#subprocess.run(['cosy '],[ path + file + 'TEMP'])



def get_obs(obs):
	text = open(os.getcwd()+'/output.txt','r').readlines()
	outputs = {}

	for lines in text:
		name = lines.split()[0]
		try: 
			num = float(lines.split()[1])
		except ValueError:
			num = 0
			print(f"ValueError for Obs {name}, set value to 0 and continuing..")
		outputs[name] = num
	try:
		val = outputs[obs]
	except KeyError:
		if obs == 'TRANSMISSION_DSSD':
			line = open(os.getcwd()+'/rays.txt','r').readlines()
			line = line[1:82]
			lines = []
			for i in line:
				i.split()
				for j in range(len(i.split())):
					lines.append(i.split()[j])
			out = []
			for val in lines:
				out.append(float(val))
			x = np.array(out)

			line = open(os.getcwd()+'/rays.txt','r').readlines()
			line = line[83:164]
			lines = []
			for i in line:
				i.split()
				for j in range(len(i.split())):
					lines.append(i.split()[j])
			out = []
			for val in lines:
				out.append(float(val))
			y = np.array(out)
			val = np.where((x > -0.016) & (y > -0.016) & (x<0.016) & (y<0.016))
			val = val[0]/numberMC
		
	return val

def get_var(var,settings,path, file):
	if settings[var][1] in ['M5','MQ','MH']:
		temp =  file + 'TEMP' +  '.fox'
		text = open(path+temp,'r').readlines()[settings[var][0]-1]
		split = text.split()
		vals = split[2].split('*')
		val = vals[-1]
		val = float(val)
	if settings[var][1] in ['MC']:
		temp =  file + 'TEMP' +  '.fox'
		text = open(path+temp,'r').readlines()[settings[var][0]-1]
		split = text.split()
		vals = split[1].split('*')
		val = vals[-1]
		val = float(val)
	return val

