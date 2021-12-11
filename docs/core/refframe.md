## ```refframe``` 

Internal class, cannot easily be animated. Initializes a reference frame that other objects and animations can be the child of. In blender, this takes the form of an Empty object. 

### Initialization
```python
bpsc.refframe(name, parent)
```

#### Arguments
```name``` : a string that will become the name of the reference frame
<br>```parent```: a ```bpy.data.object``` that will become the parent of this reference frame
