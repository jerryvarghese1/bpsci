## ```ref_frame``` 

Internal class, cannot easily be animated. Initializes a reference frame that other objects and animations can be the child of. In blender, this takes the form of an Empty object. 

### Initialization
```python
bpsc.ref_frame(name, parent, anim)
```

#### Arguments
```name``` : a string that will become the name of the reference frame
<br>```parent```: a ```bpy.data.object``` that will become the parent of this reference frame
<br>```anim```: a ```init_anim``` class object that was used to initialize the animation
