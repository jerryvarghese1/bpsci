import numpy as np
from scipy.spatial.transform import Rotation as R
import bpy
import pandas as pd

def erase_others(obj_name):
    """
        Erase all objects associated with the passed object name. 

        .. warning::
            this function will delete any object that has the passed object name as a substring
        .. versionadded:: 0.2.30

        :param str obj_name: the object name

        """
    actual_obj = bpy.data.objects[obj_name]
    name = actual_obj.name
    
    all_objs = list(bpy.data.objects)
    all_objs_names = np.array([obj.name for obj in all_objs])
    
    inds = [all_obj_name.find(name) for all_obj_name in all_objs_names]
    
    family = []
    relatives = []
    
    for i in range(len(inds)):
        if inds[i] >= 0:
            family.append(all_objs_names[i])
    
    for member in family:
        if member != name:
            relatives.append(member)
            
    [bpy.data.objects.remove(bpy.data.objects[obj_name]) for obj_name in relatives]

def bpy_obj(obj_name):
    """
        Returns the Blender object associated with the passed name

        :param str obj_name: the object name

        """
    return bpy.data.objects[obj_name]

def euler2quat(angles1, angles2, angles3, euler_type):
    """
        Takes a set of Euler angles over time and returns the equivalent quaternion representation

        :param np.ndarray angles1: first set of angles over time
        :param np.ndarray angles2: second set of angles over time
        :param np.ndarray angles3: third set of angles over time
        :param str euler_type: the Euler angle order (i.e. 'xyz' for 1,2,3 or 'zxz' for 3,1,3)

        Returns:
            :returns (nd.array): a numpy array of quaternions over time

        """

    all_angles = np.vstack([angles1, angles2, angles3]).transpose()
    quat_out = R.from_euler(euler_type, all_angles).as_quat()
    return quat_out