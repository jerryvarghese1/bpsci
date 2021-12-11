## bpsci ```core``` module

Import with:

```python 
from bpsci import core as bpsc # core import
import bpy # import blender python API
```
##### ```bpy``` must be imported, or ```bpsci``` will not work


### ```init_anim```
Sets up the global animation information such as beginning frame, ending frame, and speed up

### ```dyn_obj```

Dynamic object class

### ```refframe``` 
Internal class, cannot easily be animated. Initializes a reference frame that other objects and animations can be the child of. In blender, this takes the form of an Empty object. 