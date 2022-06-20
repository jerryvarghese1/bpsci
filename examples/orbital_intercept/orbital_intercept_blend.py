import bpy
import bpsci.core as bpsc
import numpy as np
import pandas as pd

from scipy.spatial.transform import Rotation as R 

file_loc = "./examples/orbital_intercept/orb_int_data.csv" # read data
data = pd.read_csv(file_loc)

euler_pa = (0, 0, 0) # offset of principal axes (from the inertia tensor). In this case, all the objects are strictly translating, so this will be passed to all the dynamics objects indicating that there is no offset of the principal axes
euler_type = 'xyz' # same as previous
cog_offset = (0, 0, 0) # offset of center of gravity

anim = bpsc.init_anim(data['t'].to_numpy(), 4000, 1/1000) #initialize animation using the time vector, speeding up the simulation 4000x and scaling it to 1/1000 of the original size

asteroid = bpsc.dyn_obj(bpy.data.objects['asteroid'], euler_pa, cog_offset, euler_type, None, anim) # the asteroid's dynamic object
asteroid.apply_animation(data['t_x'].to_numpy(), data['t_y'].to_numpy(), data['t_z'].to_numpy(), None) # apply the animation, using None for the angles (since there are no rotational dynamics). 't' stands for target
asteroid.apply_streamline('dynamic', data['t_x'].to_numpy(), data['t_y'].to_numpy(), data['t_z'].to_numpy(), .1) # create the dynamic streamline based on the same data, with a thickness of .1

orig_orbit = bpsc.dyn_obj(bpy.data.objects['orig_orbit'], euler_pa, cog_offset, euler_type, None, anim) # the initial orbit's dynamic object
orig_orbit.apply_animation(data['i_x'].to_numpy(), data['i_y'].to_numpy(), data['i_z'].to_numpy(), None) # apply the animation, using None for the angles (since there are no rotational dynamics). 't' stands for target
orig_orbit.apply_streamline('dynamic', data['i_x'].to_numpy(), data['i_y'].to_numpy(), data['i_z'].to_numpy(), .1) # create the dynamic streamline based on the same data, with a thickness of .1

transf_orbit = bpsc.dyn_obj(bpy.data.objects['ship'], euler_pa, cog_offset, euler_type, None, anim) # the ship's dynamic object (the ship is making the low-thrust transfer)
transf_orbit.apply_animation(data['r1'].to_numpy(), data['r2'].to_numpy(), data['r3'].to_numpy(), None) # apply the animation, using None for the angles (since there are no rotational dynamics). 't' stands for target
transf_orbit.apply_streamline('dynamic', data['r1'].to_numpy(), data['r2'].to_numpy(), data['r3'].to_numpy(), .1) # create the dynamic streamline based on the same data, with a thickness of .1
