<h1><img src="https://user-images.githubusercontent.com/63359305/153303226-3c4b89a6-4d05-4850-a832-0dafebd3454d.png">  bpsci documentation</h1>

This page is under construction; it may be incomplete.

### Site Navigation
#### [core Module Documentation](https://jerryvarghese1.github.io/bpsci/core)
#### [utils Module Documentation](https://jerryvarghese1.github.io/bpsci/utils)

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

Then run:
```bash
"your/path/to/Blender's/python.exe" -m pip install numpy scipy pandas bpsci --target="your/path/to/Blender's/site-packages"
```

This should install the packages in the correct directory. If this fails, try running the command as administrator in your python enabled command prompt.

To update:
```bash
"your/path/to/Blender's/python.exe" -m pip install bpsci --update --target="your/path/to/Blender's/site-packages"
```

#### Use
See examples for now. This section will be more thoroughly filled in shortly.
