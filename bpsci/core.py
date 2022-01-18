import numpy as np
from scipy.spatial.transform import Rotation as R
import bpy
import pandas as pd

class init_anim:
    def __init__(self, t, speed_up, scale):
        self.frame_rate = bpy.context.scene.render.fps
        
        self.t = t
        
        self.speed_up = speed_up
        
        self.frames = np.linspace(1, int(t[-1]*self.frame_rate/speed_up), len(t)).astype(int)
        
        self.frame_duration = self.frames[-1]

        self.scale = scale
        
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = self.frame_duration+1

class ref_frame:
    def __init__(self, name, parent, anim):
        self.name = name
        self.parent = parent
        
        # Blender portion
        self.ob = bpy.data.objects.new(name, None)
        bpy.context.scene.collection.objects.link(self.ob)
        
        self.ob.parent = parent
        self.ob.empty_display_type = 'ARROWS'
        self.ob.rotation_mode = 'QUATERNION'

        self.frames = anim.frames
        self.scale = anim.scale

        
    def static_6DOF(self, quat, x, y, z):
        if not(quat is None):
            self.ob.rotation_quaternion[1] = quat[0]
            self.ob.rotation_quaternion[2] = quat[1]
            self.ob.rotation_quaternion[3] = quat[2]
            self.ob.rotation_quaternion[0] = quat[3]

        
        if not((x is None or y is None) or z is None):
            self.ob.location = (x, y, z)
        
    def dynamic_6DOF(self, quat, x_list, y_list, z_list):
        frames = self.frames
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
                cur_x = x_list[i]*self.scale
                cur_y = y_list[i]*self.scale
                cur_z = z_list[i]*self.scale
            
                self.ob.location = (cur_x, cur_y, cur_z)
            
                self.ob.keyframe_insert(data_path='location', frame=cur_frame)
        

class dyn_obj:
    def __init__(self, obj, pa, euler_type, parent, anim):

        self.frames = anim.frames
        self.scale = anim.scale
        
        self.euler_pa = pa
        
        self.quat = R.from_euler(euler_type, pa).as_quat()
        
        self.non_rot = ref_frame(obj.name+'_non_rot', parent, anim)
        
        self.pa_axes = ref_frame(obj.name+'_pa', self.non_rot.ob, anim)
        self.pa_axes.static_6DOF(self.quat, None, None, None)
        
        self.body = ref_frame(obj.name+'_body', self.pa_axes.ob, anim)
        
        obj.parent = self.body.ob
        obj.scale = (self.scale, self.scale, self.scale)

        self.body.static_6DOF(-self.quat, None, None, None)

        self.name = obj.name
        
    def apply_animation(self, x_list, y_list, z_list, quat_list):
        

        self.pa_axes.dynamic_6DOF(quat_list, None, None, None)
        self.non_rot.dynamic_6DOF(None, x_list, y_list, z_list)

    def apply_streamline(self, staticity, int_x, int_y, int_z, thickness):
        name = self.name+'_streamline'
        frames = self.frames
        
        int_size = len(int_x)
        int_coords = np.zeros((int_size, 3))
        int_coords[:, 0] = int_x*self.scale
        int_coords[:, 1] = int_y*self.scale
        int_coords[:, 2] = int_z*self.scale

        int_curve = bpy.data.curves.new(name, type='CURVE')
        int_curve.dimensions = '3D'
        int_curve.resolution_u = 2

        # map coords to spline
        int_line = int_curve.splines.new('NURBS')
        int_line.points.add(len(int_coords))
        for i, coord in enumerate(int_coords):
            x,y,z = coord
            int_line.points[i].co = (x, y, z, 1)

        # create Object
        int_curveOB = bpy.data.objects.new(name, int_curve)

        # attach to scene and validate context
        bpy.context.collection.objects.link(int_curveOB)
        
        int_curveOB.data.bevel_depth = thickness
        
        if staticity == 'dynamic':
            for i in range(len(frames)):
                cur_frame = frames[i]
                
                bpy.data.objects[name].data.bevel_factor_end = 1/(frames[-1]) * cur_frame
                bpy.data.objects[name].data.keyframe_insert(data_path='bevel_factor_end', frame=cur_frame)

class dyn_vec:
    def __init__(self, obj, name, scale_mag, scale_off, offset, anim):
        self.parent = obj
        self.name = name+"_vector"
        
        self.parent_rf = ref_frame(self.name+"_empty", self.parent, anim)

        self.filepath = self.filepath = __file__.replace("__init__.py", "").replace("\\core.py", "")+'\\assets\\objects\\arrow.obj' #"C:/Users/vargh/Documents/GitHub/bpsci/bpsci/assets/objects/arrow.obj" #bpsci.__file__.replace("__init__.py", "")+'\\assets\\objects\\arrow.obj'

        vec = bpy.ops.import_scene.obj(filepath=self.filepath)
        vec = bpy.context.selected_objects[0]
        self.vec = vec
        
        self.parent_rf.ob.location = offset
        vec.parent = self.parent_rf.ob
        vec.name = self.name
        
        self.scale = scale_mag
        vec.scale = (scale_mag, scale_off, scale_off)
        
        self.frames = anim.frames
    def animate(self, x, y, z):
        frames = self.frames

        max_x = 1
        max_y = 1
        max_z = 1
        
        if max(x) != 0:
            max_x = max(x)
        if max(y) != 0:
            max_y = max(y)
        if max(z) != 0:
            max_z = max(z)
        
        norm_x = x/max_x *self.scale
        norm_y = y/max_y *self.scale
        norm_z = z/max_z *self.scale
        
        self.point_rf = ref_frame(self.name+"_pointing_empty", self.parent, anim)
        
        tracking_constraint = self.parent_rf.ob.constraints.new('DAMPED_TRACK')
        tracking_constraint.target = self.point_rf.ob
        tracking_constraint.track_axis = 'TRACK_X'
        
        for i in range(len(frames)):
            cur_frame = frames[i]
            cur_x = norm_x[i]
            cur_y = norm_y[i]
            cur_z = norm_z[i]
                
            mag_arrow = np.sqrt(cur_x**2 + cur_y**2 + cur_z**2)*self.scale
            
            self.parent_rf.ob.scale = (mag_arrow, 1, 1)
                
            self.point_rf.ob.location = (cur_x, cur_y, cur_z)
            
            self.point_rf.ob.keyframe_insert(data_path='location', frame=cur_frame)
            self.parent_rf.ob.keyframe_insert(data_path='scale', frame=cur_frame)

