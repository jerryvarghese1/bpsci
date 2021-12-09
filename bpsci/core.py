import numpy as np
from scipy.spatial.transform import Rotation as R
import bpy
import pandas as pd

class init_anim:
    def __init__(self, t, speed_up):
        self.frame_rate = bpy.context.scene.render.fps
        
        self.t = t
        
        self.speed_up = speed_up
        
        self.frames = np.linspace(1, int(t[-1]*self.frame_rate/speed_up), len(t)).astype(int)
        
        self.frame_duration = self.frames[-1]
        
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = self.frame_duration+1

class ref_frame:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        
        # Blender portion
        self.ob = bpy.data.objects.new(name, None)
        bpy.context.scene.collection.objects.link(self.ob)
        
        self.ob.parent = parent
        self.ob.empty_display_type = 'ARROWS'
        self.ob.rotation_mode = 'QUATERNION'
        
    def static_6DOF(self, quat, x, y, z):
        if not(quat is None):
            self.ob.rotation_quaternion[1] = quat[0]
            self.ob.rotation_quaternion[2] = quat[1]
            self.ob.rotation_quaternion[3] = quat[2]
            self.ob.rotation_quaternion[0] = quat[3]
        
        if not((x is None or y is None) or z is None):
            self.ob.location = (x, y, z)
        
    def dynamic_6DOF(self, quat, x_list, y_list, z_list, frames):
        if not(quat is None):
            for i in range(len(frames)):
                cur_frame = frames[i]
                
                cur_quat = quat[i]
            
                self.ob.rotation_quaternion[1] = cur_quat[0]
                self.ob.rotation_quaternion[2] = cur_quat[1]
                self.ob.rotation_quaternion[3] = cur_quat[2]
                self.ob.rotation_quaternion[0] = cur_quat[3]
            
                self.ob.keyframe_insert(data_path='rotation_quaternion', frame=cur_frame)
                
        if not(x_list is None):
            for i in range(len(frames)):
                cur_frame = frames[i]
                cur_x = x_list[i]
                cur_y = y_list[i]
                cur_z = z_list[i]
            
                self.ob.location = (cur_x, cur_y, cur_z)
            
                self.ob.keyframe_insert(data_path='location', frame=cur_frame)
        

class dyn_obj:
    def __init__(self, obj, pa, euler_type, parent):
        
        self.euler_pa = pa
        
        self.quat = R.from_euler(euler_type, pa).as_quat()
        
        self.non_rot = ref_frame(obj.name+'_non_rot', parent)
        
        self.pa_axes = ref_frame(obj.name+'_pa', self.non_rot.ob)
        self.pa_axes.static_6DOF(self.quat, None, None, None)
        
        self.body = ref_frame(obj.name+'_body', self.pa_axes.ob)
        
        obj.parent = self.body.ob
        self.body.static_6DOF(-self.quat, None, None, None)
        
    def apply_animation(self, x_list, y_list, z_list, quat_list, frames):
        
        self.pa_axes.dynamic_6DOF(quat_list, None, None, None, frames)
        self.non_rot.dynamic_6DOF(None, x_list, y_list, z_list, frames)