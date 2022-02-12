import numpy as np
from scipy.spatial.transform import Rotation as R
import bpy
import pandas as pd

def erase_others(obj_name):
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
    return bpy.data.objects[obj_name]