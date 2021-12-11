# bpsci
High level abstraction meant to create six degree of freedom technical animations in Blender.

View the documentation [here](https://jerryvarghese1.github.io/bpsci/)

This is currently a work in progress. Documentation and instructions for use are incoming, as well as new features useful for scientific visualizations!

## Installation

#### Installation
```bash
python -m "your/path/to/blender/python" pip install bpsci
```

### Objectives of bpsci
```bpsci``` aims to provide a six degree of freedom simulation backbone to visualize an objects displacement in three dimensions, as well as the three orientation angles, given that the time series data for each degree of freedom has already been simulated. Future functionality with additional scientifically useful visualizations will most likely be added as well.

### Why do I need this library?
Graphs are nice, but can often not provide the same level of intuition as a full visualization in 3D space. For example, it is much easier to understand Euler Angles/Orientation in 3D space in an interactive 3D space, rather than a technical drawing projected on to a 2D paper. Technical visualizations build intution in a more physical understanding of an object's dynamics. 

As an example, visualizing an orbit in three dimensions with respect to time inherently bestows intution about the velocity magnitude of a spacecraft as a function of its true anomaly, in a way that a graph of the path of the orbits cannot.

### Getting Started
Please see the GitHub Pages
