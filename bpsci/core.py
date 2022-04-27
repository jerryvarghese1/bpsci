"""
Building Blocks of a Dynamic Visualization - :mod:`bpsci.core`
==============================================================
The bpsci core is a collection of classes and methods used to create dynamic visualizations.

"""

import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.interpolate import interp1d
import bpy
import pandas as pd

class init_anim:
    """
    Sets up the global animation information such speed up and global scale

    :param np.ndarray t: contains the time information that corresponds with the six degrees of freedom data 
    :param float speed_up: the 'real time speed up' or the ratio of the duration of the data to the duration of the animation 
    :param float scale: global physical scale factor of the animation, i.e., .1 will reduce everything to be 1/10th its original size
    """
    def __init__(self, t, speed_up, scale):

        self.frame_rate = bpy.context.scene.render.fps
        """:type: `float`: frame rate of animation"""
        
        self.t = t
        """:type: `np.ndarray`: contains the time information that corresponds with the six degrees of freedom data"""
        
        self.speed_up = speed_up
        """:type: `float`: the "real time speed up" or the ratio of the duration of the data to the duration of the animation"""
        
        self.frames = np.linspace(1, int(t[-1]*self.frame_rate/speed_up+1), len(t)).astype(int)
        """:type: `np.ndarray`: the frames that Blender will animate and have corresponding data for"""
        
        self.frame_duration = self.frames[-1]
        """:type: `int`: number of total frames in animation"""

        self.scale = scale
        """:type: `float`: global physical scale factor of the animation, i.e., .1 will reduce everything to be 1/10th its original size"""
        
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = self.frame_duration+1

class ref_frame:
    """
    Initializes a reference frame that other objects and animations can be the child of. 

    In blender, this takes the form of an Empty object.


    :param str name: the Blender object name of the reference frame
    :param bpy.data.object parent: the Blender object parent of this reference frame 
    :param anim: class object that was used to initialize the animation
    :type anim: :class:`bpsci.core.anim`
    

    """
    def __init__(self, name, parent, anim):

        
        
        self.name = name
        """:type: `str`: the Blender object name of the reference frame"""
        self.parent = parent
        """:type: `bpy.data.object`: the Blender object parent of this reference frame"""
        
        # Blender portion
        self.ob = bpy.data.objects.new(name, None)
        """:type: `bpy.data.object`: the Blender object that represents this reference frame"""
        
        bpy.context.scene.collection.objects.link(self.ob)
        
        self.ob.parent = parent
        self.ob.empty_display_type = 'ARROWS'
        self.ob.rotation_mode = 'QUATERNION'

        self.frames = anim.frames
        """:type: `np.ndarray`: the frames that Blender will animate and have corresponding data for"""

        self.scale = anim.scale
        """:type: `float`: global physical scale factor of the animation"""

        
    def static_6DOF(self, quat, x, y, z):
        """
        Places the reference frame in one specified static location.

        .. warning::
            This is currently an internal method. This method will be exposed properly in future updates
        .. versionadded:: 0.2.30

        May be useful for offsetting the reference frame from the parent object (i.e. for center of mass of principal axes offset)


        :param np.ndarray quat: an numpy array of one quaternion
        :param float x: the x position 
        :param float y: the y position 
        :param float z: the z position 

        """
        if not(quat is None):
            self.ob.rotation_quaternion[1] = quat[0]
            self.ob.rotation_quaternion[2] = quat[1]
            self.ob.rotation_quaternion[3] = quat[2]
            self.ob.rotation_quaternion[0] = quat[3]

        
        if not((x is None or y is None) or z is None):
            self.ob.location = (x, y, z)
        
    def dynamic_6DOF(self, quat, x_list, y_list, z_list):
        """
        Animates the reference frame over time.

        .. warning::
            This is currently an internal method. This method will be exposed properly in future updates
        .. versionadded:: 0.2.30

        May be useful for continually offsetting the reference frame from the parent object (i.e. for center of mass of principal axes offset for changing mass/distribution)

        :param np.ndarray quat: an numpy array of quaternions over time
        :param np.ndarray x: the x position over time
        :param np.ndarray y: the y position over time
        :param np.ndarray z: the z position over time

        """

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
    """
    The main building block of all dynamic visualizations 


    :param bpy.data.object obj: the Blender object that will be animated
    :param np.ndarray pa: the offset of the principal axes specified by the :param: ` euler_type:
    :param str euler_type: the Euler angle order (i.e. 'xyz' for 1,2,3 or 'zxz' for 3,1,3)
    :param bpy.data.object parent: the Blender object parent of the original object 
    :param anim: class object that was used to initialize the animation
    :type anim: :class:`bpsci.core.init_anim`
        
    """
    def __init__(self, obj, pa, euler_type, parent, anim):
        

        self.parent = parent
        """:type: `bpy.data.object`: the Blender object parent of this reference frame"""

        self.frames = anim.frames
        """:type: `np.ndarray`: the frames that Blender will animate and have corresponding data for"""
        self.scale = anim.scale
        """:type: `float`: global physical scale factor of the animation"""

        self.ob = obj
        """:type: `bpy.data.object`: the Blender object that will be animated"""
        
        self.euler_pa = pa
        """:type: `np.ndarray`: the offset of the principal axes specified by the :param: ` euler_type:"""
        
        self.quat = R.from_euler(euler_type, pa).as_quat()
        """:type: `np.ndarray`: a numpy array of one quaternion that represents the principal axes offset"""
        
        self.non_rot = ref_frame(obj.name+'_non_rot', parent, anim)
        """:class:`~bpsci.core.ref_frame`: the non-rotational reference frame (owner of translational movement only)"""
        
        self.pa_axes = ref_frame(obj.name+'_pa', self.non_rot.ob, anim)
        """:class:`~bpsci.core.ref_frame`: the principal axes rotational reference frame (owner of rotational movement, inherits translational movement from parent)"""

        self.pa_axes.static_6DOF(self.quat, None, None, None)
        
        self.body = ref_frame(obj.name+'_body', self.pa_axes.ob, anim)
        """:class:`~bpsci.core.ref_frame`: the body reference frame (untransformed principal axes)"""
        
        obj.parent = self.body.ob
        obj.scale = (self.scale, self.scale, self.scale)

        self.body.static_6DOF(-self.quat, None, None, None)

        self.name = obj.name
        """:type: `str`: the Blender object name of the original object"""

    def apply_animation(self, x_list, y_list, z_list, quat_list):

        """
        Animates a :class:`~bpsci.core.dyn_obj` in the full six degrees of freedom

        :param np.ndarray x_list: a numpy array of the x position over time
        :param np.ndarray y_list: a numpy array of the y position over time
        :param np.ndarray z_list: a numpy array of the z position over time
        :param np.ndarray quat_list: a numpy array of the quaternion over time. Can be passed None if rotation is ignored.
        """

        self.pa_axes.dynamic_6DOF(quat_list, None, None, None)
        self.non_rot.dynamic_6DOF(None, x_list, y_list, z_list)

    def apply_streamline(self, staticity, int_x, int_y, int_z, thickness):
        """
        Creates a static or dynamic positional streamline for a :class:`~bpsci.core.dyn_obj`

        :param str staticity: a string (either 'static' or 'dynamic') that specifies whether the the streamline is animated over time
        :param np.ndarray int_x: a numpy array of the x position over time
        :param np.ndarray int_y: a numpy array of the y position over time
        :param np.ndarray int_z: a numpy array of the z position over time
        
        """


        name = self.name+'_streamline'
        """:type: `str`, the Blender object name of the streamline"""
        frames = self.frames
        """:type: `np.ndarray`: the frames that Blender will animate and have corresponding data for"""
        
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
        int_curveOB.data.use_fill_caps = True


        int_curveOB.data.bevel_factor_start = 0

        curve_to_mesh(int_curveOB)

        if staticity == 'dynamic':
            bpy.ops.object.modifier_add(type='BUILD')
            bpy.context.object.modifiers["Build"].frame_start = 0
            bpy.context.object.modifiers["Build"].frame_duration = self.frames[-1]+1


class dyn_vec:
    """
    Initializes a dynamic vector`


    :param bpy.data.object parent: the Blender object the vector is associated with
    :param str name: the Blender object name of the vector ('_vector' will be appended to this name)
    :param float scale_mag: the scaling factor of the vector's magnitude axis (purely aesthetic)
    :param float scale_off: the scaling factor of the vector's off-axes (purely aesthetic)
    :param tuple[float] offset: offset of vector from the parent object (purely aesthetic)
    :param anim: class object that was used to initialize the animation
    :type anim: :class:`bpsci.core.anim`

    """
    def __init__(self, parent, name, scale_mag, scale_off, offset, anim):

        

        self.parent = parent
        """:type: `bpy.data.object`: the Blender object parent of this reference frame"""

        self.name = name+"_vector"
        """str: the Blender object name of the vector"""
        
        self.parent_rf = ref_frame(self.name+"_empty", self.parent, anim)
        """:type: `bpy.data.object`: holds the vector"""

        self.filepath = self.filepath = __file__.replace("__init__.py", "").replace("\\core.py", "")+'\\assets\\objects\\arrow.obj' #"C:/Users/vargh/Documents/GitHub/bpsci/bpsci/assets/objects/arrow.obj" #bpsci.__file__.replace("__init__.py", "")+'\\assets\\objects\\arrow.obj'
        """:type: `str`: file path to arrow asset"""


        vec = bpy.ops.import_scene.obj(filepath=self.filepath)
        vec = bpy.context.selected_objects[0]
        self.vec = vec
        """:type: `bpy.data.object`: the actual arrow asset"""
        
        self.parent_rf.ob.location = offset
        vec.parent = self.parent_rf.ob
        vec.name = self.name
        
        self.scale = scale_mag
        vec.scale = (scale_mag, scale_off, scale_off)
        self.anim = anim
        """:class:`bpsci.core.init_anim`: class object that was used to initialize the animation"""
        
        self.frames = anim.frames
        """:type: `np.ndarray`: the frames that Blender will animate and have corresponding data for"""
    def animate(self, x, y, z):
        """
        Animates a dynamic vector

        :param np.ndarray x: a numpy array of the x component over time
        :param np.ndarray y: a numpy array of the y component over time
        :param np.ndarray z: a numpy array of the z component over time

        """

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
        
        self.point_rf = ref_frame(self.name+"_pointing_empty", self.parent, self.anim)
        """:type: `bpy.data.object`: an empty that provides calculates the directionality of the vector"""
        
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

class anim_text:
    """
    Creates animated text


    :param str name: the Blender object name of the text ('_text' will be appended to this name)
    :param bpy.data.object parent: the Blender object parent of this text 
    :param anim: class object that was used to initialize the animation
    :type anim: :class:`bpsci.core.anim`
    :param np.ndarray data: the data to be displayed (same length as the number of animated frames)
    :param str label: a label to append to the text (if no label is desired, pass '')
    :param int fix_place: the number of decimal places to fix the text to
    :param bool if_str: whether or not the data is a numerical or string vector. Currently only numerical vectors are supported.

    """
    def __init__(self, name, parent, anim, data, label, fix_place, if_str):

        

        self.anim = anim

        bpy.ops.object.text_add()
        ob=bpy.context.object
        ob.data.body = "INIT"

        self.obj = ob

        ob.name = name + '_text'

        self.obj.parent = parent
        self.name = name

        all_frames = np.arange(1, anim.frames[-1])
        frame_interper = interp1d(anim.frames, data, fill_value = 'extrapolate')

        fixed_data = frame_interper(all_frames)

        if not(if_str):
            def recalculate_text(scene):
                text = ob
                cur_frame = bpy.context.scene.frame_current
                
                text.data.body = ('{0:.'+str(fix_place)+'f}').format(fixed_data[cur_frame-1]) + ' ' + label
                    

            bpy.app.handlers.frame_change_pre.append(recalculate_text)

def curve_to_mesh(curve):
    context = bpy.context
    deg = context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(curve.evaluated_get(deg), depsgraph=deg)
    
    curve_name = curve.name

    new_obj = bpy.data.objects.new(curve.name + "_mesh", me)
    context.collection.objects.link(new_obj)

    for o in context.selected_objects:
        o.select_set(False)

    new_obj.matrix_world = curve.matrix_world
    new_obj.select_set(True)
    context.view_layer.objects.active = new_obj
    
    bpy.data.objects.remove(curve, do_unlink=True)
    new_obj.name = curve_name

