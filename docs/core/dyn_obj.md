### ```dyn_obj```

Dynamic object class

```python
my_obj = bpsc.dyn_obj(obj, pa, euler_type, parent, anim)
```

#### Arguments
```obj```: a ```bpy.data.object``` that is the object that the animation should be applied to
<br>```pa```: a ```list``` that contains an Euler angle sequence that represents to rotation of the principle axes from the imported body fixed axes. An argument for a moved center of mass is being developed
<br>```euler_type```: a ```str``` that represents the Euler angle sequence (i.e. ```'zxz'``` for a 313 Euler angle sequence)
<br>```parent```: a ```bpy.data.object``` that will become the parent of the ```obj``` object, can be ```None``` if no parent is desired 
<br>```anim```: a ```init_anim``` class object that was used to initialize the animation

#### Attributes
```euler_pa```: : a ```list``` that contains an Euler angle sequence that represents to rotation of the principle axes from the imported body fixed axes
<br>```quat```: an ```nd.array``` quaternion equivalent of ```euler_pa```
<br>```non_rot```: ```bpy.data.object``` of type Empty which is the non-rotating reference frame for the object, aka contains only the translation kinematics of the animation
<br>```pa_axes```: ```bpy.data.object``` of type Empty which is the principle axes of the rotation
<br>```parent```: ```bpy.data.object``` of any type which is the parent of this dynamic_object

#### Methods

##### ```apply_animation```

```python
my_obj.apply_animation(x_list, y_list, z_list, quat_list)
```
Apply a six degree of freedom animation to an object

###### Arguments
```x_list```: an ```nd.array``` that contains the x positional data for the animation
<br>```y_list```: an ```nd.array``` that contains the y positional data for the animation
<br>```z_list```: an ```nd.array``` that contains the z positional data for the animation
<br>```quat```: an ```nd.array``` that contains the quaternion orientation information

##### ```apply_streamline```
```python
my_obj.apply_streamline(staticity, x_list, y_list, z_list, thickness)
```

###### Arguments
```staticity```: a ```str``` that determines whether the streamline is animated or not (the string can be either ```"static"``` or ```"dynamic"```)
<br>```x_list```: an ```nd.array``` that contains the x positional data for the animation
<br>```y_list```: an ```nd.array``` that contains the y positional data for the animation
<br>```z_list```: an ```nd.array``` that contains the z positional data for the animation
<br>```thickness```: a ```float``` that specifies the radius of the streamline (purely aesthetic)

