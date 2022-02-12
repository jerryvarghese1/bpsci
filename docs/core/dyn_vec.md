### ```dyn_vec```

Dynamic vector class

```python
from bpsci import core as bpsc

my_vec = bpsc.dyn_vec(parent, name, scale_mag, scale_off, offset, anim)
```

#### Arguments
```parent```: a ```bpy.data.object``` that will become the parent of the vector, can be ```None``` if no parent is desired. i.e., ```parent``` could be ```my_obj.pa_axes.ob```, referring to the ```empty``` object that signifies the principle axes of my_obj
<br>```name```: a ```str``` that is that name of the vector
<br> ```scale_mag```: a ```float``` that changes how much the magnitude of the vector arrow is scaled (purely aesthetic)
<br> ```scale_off```: a ```float``` that changes how much the off-axes of the vector arrow is scaled (purely aesthetic)
<br> ```offset```: a ```tuple``` of length 3 that offsets the origin of the vector arrow (purely aesthetic)

#### Attributes
```parent```: a ```bpy.data.object``` that is the parent of the vector
<br>```name```: a ```str``` that is that name of the vector
<br>```obj```: a ```bpy.data.object``` that is the physical arrow of the vector
<br>```parent_rf```: an ```ref_frame``` class object that is an internal parent of the vector
<br>```scale```: a ```tuple``` of length 3 that is the scale of the vector arrow

#### Methods

##### ```animate```

```python
my_vec.animate(x_list, y_list, z_list)
```
Animate the vector with x,y,z data

###### Arguments
```x_list```: an ```nd.array``` that contains the x positional data for the animation
<br>```y_list```: an ```nd.array``` that contains the y positional data for the animation
<br>```z_list```: an ```nd.array``` that contains the z positional data for the animation
