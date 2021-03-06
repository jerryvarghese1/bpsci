Quickstart Guide
================

Objectives of bpsci
-------------------

:mod:`bpsci` aims to provide a six degree of freedom simulation backbone to visualize an object's displacement in three dimensions, as well as the three orientation angles, given that the time series data for each degree of freedom has already been simulated. Future functionality with additional scientifically useful visualizations will most likely be added as well.

Why do I need this library?
---------------------------
Graphs are nice, but can often not provide the same level of intuition as a full visualization in 3D space. For example, it is much easier to understand Euler Angles/orientation in 3D space in an interactive 3D space, rather than a technical drawing projected on to a 2D paper. Technical visualizations build intution in a more physical understanding of an object's dynamics. 

As an example, visualizing an orbit in three dimensions with respect to time inherently bestows intution about the velocity magnitude of a spacecraft as a function of its true anomaly, in a way that a graph of the path of the orbits cannot.


Quick Installation
------------------

:mod:`bpsci` is installabe via PyPi, however, it needs to be installed from Blender's version of Python and run from within Blender.

1. Install Blender from `https://www.blender.org/ <https://www.blender.org/>`_. Any version above 2.8 should be compatible
2. Open a python enabled command prompt. 
3. Locate Blender's installation's python path. For Windows users, this is usually found in :file:`"C:/Program Files/Blender Foundation/Blender X.X/X.X/python"` where X.X is your version of Blender. 
4. Locate the :file:`python.exe` associated with your version of Blender, found in :file:`./bin/python.exe`
5. Locate the :file:`site-packages` directory, found in :file:`./lib/site-packages`
6. Run the following command in the command prompt

.. code-block:: shell

   "your/path/to/python.exe" -m pip install bpsci --target="your/path/to/site-packages"

This should fully install bpsci for Blender, along with its dependencies.

.. note::
   If you get an error in installation, try the same steps above but run the command prompt as an administrator.

Quick Tutorial
--------------

Let's animate a cube to follow a simple quadratic path in three dimensions, and rotate linearly in the z-axis (yaw), using the Euler angle approach to rotation:

.. math::
   x = t^2
.. math::
   y = t^2
.. math::
   z = t^2
.. math::
   yaw = t

Thankfully, there is a default cube present, but for the sake of learning how to use the Blender GUI, let's delete it and add another. In the following steps, curly brackets {} represent keys and square brackets [] represent GUI items.

1. Click on the cube to select it, and press {X} to delete it. 

2. Click on [Add] in the top right corner (next to [View] and [Select]). A drop down menu will then show you what types of  objects you can add. A cube and most other solid geometries are referred to as a "mesh" in Blender, so select [Mesh]. The [Cube] option should be in the resulting drop-down. Select it. The Cube will be placed at the world origin.

3. Now move to the [Scripting] tab. There are multiple "Tabs" at the top of the Blender GUI, including [Layout] which you are currently on, [Modelling], [Sculpting], etc. If you do not see it, press the [+] at the end of the tabs and select it from the resulting dropdown.

4. Now we can finally write our program. Click [+ New] in the text editor. This will open a text editor with Blender that can execute scripts, with full syntax highlighting. The text editor can be temperamental, so you can also write your script elsewhere, but it must eventually be pasted into Blender's text editor and run from there.

5. Import libraries

.. code-block:: python

   import bpy # Blender Python, nothing will run without this
   import bpsci.core as bpcore # the core bpsci library
   from bpsci.utils import bpy_obj, euler2quat # tools that simply conversions and referencing Blender objects

   import numpy as np
   import scipy as sp

6. Set up dynamics information

.. code-block:: python

   disc = 50 # number of discrete time points
   start = 0 # start (in seconds)
   stop = 10 # stop (in seconds)
   t = np.linspace(start, stop, disc) # the time vector

   x = t**2
   y = t**2
   z = t**2 # the x, y, z positions of the cube

   yaw = t # the yaw angle (in radians) of the cube
   zero_list = np.zeros([1, disc]) # having just a yaw angle means that the other angles are zero

   euler_type = 'xyz' # the Euler angle sequence (1,2,3)
   quat_out = euler2quat(zero_list, zero_list, yaw, euler_type) # convert the Euler angles to quaternions

7. Initialize the animation

.. code-block:: python

    scale = 1 # scale factor of 1, will not change global scale
    speed_up = 1 # speed up factor of 1, will not change global speed up
    anim = bpcore.init_anim(t, speed_up, scale) # initialize the animation

8. Animate the object

.. code-block:: python

    cube = bpy_obj('Cube') # This selectes the cube object
    pa_offset = (0, 0, 0) # the principal axes offset of the cube as Euler angles
    cog_offset = (0, 0, 0) # the offset of the 3D model's origin to the object's center of mass
    parent = None # parent of the cube
    dyn_cube = bpcore.dyn_obj(cube, pa_offset, cog_offset, euler_type, parent, anim) # initializes the bpsci dynamic object class
    dyn_cube.apply_animation(x, y, z, quat_out) # animates object

9. View your results. Navigate back to the [Layout] tab, press the [|<] button at the bottom of the Blender GUI to jump to the first frame. Press {Space} to play the animation.










