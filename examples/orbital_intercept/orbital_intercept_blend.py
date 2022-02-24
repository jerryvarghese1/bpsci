import bpy
from bpsci import core as bpsc
import numpy as np
import pandas as pd

from scipy.spatial.transform import Rotation as R 

file_loc = "./examples/orbital_intercept/orb_int_data.csv" # read data
data = pd.read_csv(file_loc)

euler_pa = [0, 0, 0] # offset of principal axes (from the inertia tensor). In this case, all the objects are strictly translating, so this will be passed to all the dynamics objects indicating that there is no offset of the principal axes
euler_type = 'xyz' # same as previous

anim = bpsc.init_anim(data['t'].to_numpy(), 4000, 1/1000) #initialize animation using the time vector, speeding up the simulation 4000x and scaling it to 1/1000 of the original size

asteroid = bpsc.dyn_obj(bpy.data.objects['asteroid'], euler_pa, euler_type, None, anim) # the asteroid's dynamic object
asteroid.apply_animation(data['t_x'].to_numpy(), data['t_y'].to_numpy(), data['t_z'].to_numpy(), None)
asteroid.apply_streamline('dynamic', data['t_x'].to_numpy(), data['t_y'].to_numpy(), data['t_z'].to_numpy(), .1)

orig_orbit = bpsc.dyn_obj(bpy.data.objects['orig_orbit'], euler_pa, euler_type, None, anim)
orig_orbit.apply_animation(data['i_x'].to_numpy(), data['i_y'].to_numpy(), data['i_z'].to_numpy(), None)
orig_orbit.apply_streamline('dynamic', data['i_x'].to_numpy(), data['i_y'].to_numpy(), data['i_z'].to_numpy(), .1)

transf_orbit = bpsc.dyn_obj(bpy.data.objects['ship'], euler_pa, euler_type, None, anim)
transf_orbit.apply_animation(data['r1'].to_numpy(), data['r2'].to_numpy(), data['r3'].to_numpy(), None)
transf_orbit.apply_streamline('dynamic', data['r1'].to_numpy(), data['r2'].to_numpy(), data['r3'].to_numpy(), .1)
