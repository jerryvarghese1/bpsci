import numpy as np
import pandas as pd       
from scipy.spatial.transform import Rotation as R
import bpy

from bpsci import core as bpsci_core
        
#ref_frame('bruh2', None)
euler_pa = [.1, 0, 0]
euler_type = 'xyz'
              
file_path = './examples/data/gallileo.csv'

data = pd.read_csv(file_path)
t = data['t'].to_numpy()

phi = data['phi'].to_numpy()
theta = data['theta'].to_numpy()
psi = data['psi'].to_numpy()

x = data['x'].to_numpy()
y = data['y'].to_numpy()
z = data['z'].to_numpy()

euler_angle = np.vstack([psi, theta, phi]).transpose()
angles = R.from_euler('zxz', euler_angle).as_quat()
             
speed_up = 3 
scaler = 1
anim = bpsci_core.init_anim(t, speed_up, scaler)


craft = bpsci_core.dyn_obj(bpy.data.objects['gallileo'], euler_pa, euler_type, None, anim)   

craft.apply_animation(x, y, z, angles)
