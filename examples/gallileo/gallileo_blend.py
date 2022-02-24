import numpy as np
import pandas as pd       
from scipy.spatial.transform import Rotation as R
import bpy

from bpsci import core as bpsci_core

euler_pa = [.1, 0, 0] # this offsets the inertial principle axes according to the euler angle sequence below
euler_type = 'xyz' # principal axes offset euler angle sequence
              
file_path = './examples/gallileo/gallileo.csv' # file path of data

# read data and separate into correct variables
data = pd.read_csv(file_path)
t = data['t'].to_numpy() # time

phi = data['phi'].to_numpy() # first angle in 'zxz' euler angle sequence
theta = data['theta'].to_numpy() # second angle in 'zxz' euler angle sequence
psi = data['psi'].to_numpy() # third angle in 'zxz' euler angle sequence

x = data['x'].to_numpy() # positional data, x
y = data['y'].to_numpy() # positional data, y
z = data['z'].to_numpy() # positional data, z

# convert euler angles to quaternion (apply_animation method accepts a quaternion generated from scipy's Rotation library) 
# if you are interested in why this transformation is necessary, look up gimbal lock and its effects on animation
euler_angle = np.vstack([psi, theta, phi]).transpose()
angles = R.from_euler('zxz', euler_angle).as_quat()
             
speed_up = 3 # the simulation will be this many times faster than real time
scaler = 1 # if you have a very large bounding box for your movement, it may make sense to scale it down to a reasonable size to be easily viewable in Blender
anim = bpsci_core.init_anim(t, speed_up, scaler) # the anim object initializes Blender and calculates properties that the animation will require (like frames)

craft = bpsci_core.dyn_obj(bpy.data.objects['gallileo'], euler_pa, euler_type, None, anim)  #the dynamic object that represents the Gallileo spacecraft
craft.apply_animation(x, y, z, angles) # apply the animation to the spacecraft
