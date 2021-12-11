## bpsci Documentation

This page is under construction; please check again soon!

### Site Navigation
#### [Core Module Documentation](https://jerryvarghese1.github.io/bpsci/core)

### Objectives of bpsci
```bpsci``` aims to provide a six degree of freedom simulation backbone to visualize an objects displacement in three dimensions, as well as the three orientation angles, given that the time series data for each degree of freedom has already been simulated. Future functionality with additional scientifically useful visualizations will most likely be added as well.

### Why do I need this library?
Graphs are nice, but can often not provide the same level of intuition as a full visualization in 3D space. For example, it is much easier to understand Euler Angles/Orientation in 3D space in an interactive 3D space, rather than a technical drawing projected on to a 2D paper. Technical visualizations build intution in a more physical understanding of an object's dynamics. 

As an example, visualizing an orbit in three dimensions with respect to time inherently bestows intution about the velocity magnitude of a spacecraft as a function of its true anomaly, in a way that a graph of the path of the orbits cannot.

### Getting Started
This addon is specifically made for use in the Blender Python Scripting API. Using it outside of Blender will not work. Additionally, this is not a true Blender add-on. Some scripting is required to initialize and apply all animations properly. This library seeks to provide a high-level abstraction that takes care of all Blender API calls to allow the user to focus on creating the visualization, rather than searching Blender documentation.

#### Dependencies
This tool requires ```scipy```, ```numpy```, and ```pandas``` as external packages to work, along with ```bpy```, which is already built in to Blender. This means that ```scipy```, ```numpy```, and ```pandas``` will need to be ``pip`` installed for this library to work. 

To do so, locate your Blender installation's ```python.exe``` file. 

Then run
```bash
python -m "your/path/to/Blender's/python.exe" --target="your/path/to/Blender's/site-packages" pip install numpy scipy pandas bpsci
```

This should install the packages in the correct directory. If this fails, try using the ``--user`` option or running the command as administrator in your command prompt.

#### Use

The ```bpsci``` library allows one to animate an existing object in the Blender viewport. We will be animating the default cube in this tutorial.

Imports:
```python
import numpy as np
import pandas as pd       
from scipy.spatial.transform import Rotation as R
import bpy

from bpsci import core as bpsci_core
```

Initialize Offset of Principal Axes:
```python
euler_pa = [.1, 0, 0] # offset of principal axes from the body fixed imported axes as an Euler angle triple
euler_type = 'xyz' # Specify Euler angle sequence
````

Read data:
```python
file_path = '[fill this in]' # data source

data = pd.read_csv(file_path) # read data from pandas
t = data['t'].to_numpy() # isolate time variable

# isolate euler angles
phi = data['phi'].to_numpy()
theta = data['theta'].to_numpy()
psi = data['psi'].to_numpy()

# isolate diplacement data
x = data['x'].to_numpy()
y = data['y'].to_numpy()
z = data['z'].to_numpy()

euler_angle = np.vstack([psi, theta, phi]).transpose() # stack euler angle columns into column of euler angle triples
angles = R.from_euler('zxz', euler_angle).as_quat() # convert euler angle triples into quaternions
```

Initialize animation:
```python
anim = bpsci_core.init_anim(t, 3)
frames = anim.frames
```

Actuate animation:
```python
cube = bpsci_core.dyn_obj(bpy.data.objects['cube'], euler_pa, euler_type, None)   
cube.apply_animation(x, y, z, angles, frames)
```


