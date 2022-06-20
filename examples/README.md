## Examples

There are two example scenarios, corresponding to the two folders: ```gallileo``` and ```orbital_intercept```. 

### Simulations Background

#### Gallileo Spin-Up
This example models a spin up manuever of the Gallileo spacecraft as published in 'Annihilation of angular momentum bias during thrusting and spinning-up maneuvers' 
by Longuski, Kia, and Breckenridge. The data was created by running a six degree of freedom numerical simulation in MATLAB with ```ode45```. 

#### Orbital Intercept
This example models an low-thrust orbital rendezvous between one full cartesian state vector (```r1, r2, r3, v1, v2, v3```) and one position only state vector (```r1, r2, r3```) with velocity components free. It was solved using the [GEKKO library](https://gekko.readthedocs.io/en/latest/) with ```IPOPT```. See source code [here](https://github.com/jerryvarghese1/orbital_intercept)

### File Structure
Each example file contains three documents. 
- The ```.blend``` file contains the final Blender file with code already in the Scripting tab of Blender and already run. This is the final product. 
- The ```.py``` file is the script that is run from within Blender (in the scripting tab). One can observe that it is the same code as what is in the ```.blend``` file's Scripting tab. 
##### Please note that the API has changed slightly since the time the simulations have been created; the ```.py``` files are updated to reflect this, but the script inside the ```.blend``` file has not been updated. Copy and paste the ```.py``` file into Blender and replace the old script in the ```.blend``` file!
- The ```.csv``` file is the source data from the simulations.

### Tips and Tricks
- ```dyn_obj``` does not create an object. It can only modify an existing object. 
- If you have complex interconnected systems, try using Blender's ```Empty``` object, either programmatically or by using the GUI. An empty (or any Blender object, for that matter) treats its parent as an inertial frame
- All Euler angle sequences must be converted to quaternion form. The examples show how to do this, as it is easier to simulate rotational dynamics in Euler angle form.
