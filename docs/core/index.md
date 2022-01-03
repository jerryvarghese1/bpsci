## bpsci ```core``` module

Import with:

```python 
from bpsci import core as bpsc # core import
import numpy as np
import bpy
```
##### ```bpy``` must be imported, or ```bpsci``` will not work

#### Click on any of the headers below for specific documentation

### [```init_anim```](https://jerryvarghese1.github.io/bpsci/core/init_anim)
Sets up the global animation information such as beginning frame, ending frame, and speed up

### [```dyn_obj```](https://jerryvarghese1.github.io/bpsci/core/dyn_obj)

Dynamic object class, used to create a animated 6DOF simulation

### [```dyn_vec``` ](https://jerryvarghese1.github.io/bpsci/core/dyn_vec)
Dynamic vector class, used to create a dynamically moving vector

### [```ref_frame``` ](https://jerryvarghese1.github.io/bpsci/core/ref_frame)
Internal class, cannot easily be animated. Initializes a reference frame that other objects and animations can be the child of. In blender, this takes the form of an Empty object. 
