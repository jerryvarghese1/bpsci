## Examples

There are two example scenarios, corresponding to the two folders: ```gallileo``` and ```orbital_intercept```. 

### Simulations Background

#### Gallileo Spin-Up
This example models a spin up manuever of the Gallileo spacecraft as published in 'Annihilation of angular momentum bias during thrusting and spinning-up maneuvers' 
by Longuski, Kia, and Breckenridge. The data was created by running a six degree of freedom numerical simulation in MATLAB with ```ode45```. 

#### Orbital Intercept
This example models an low-thrust orbital rendezvous between one full cartesian state vector (```r1, r2, r3, v1, v2, v3```) and one position only state vector (```r1, r2, r3```) with velocity components free. It was solved using the [GEKKO library](https://gekko.readthedocs.io/en/latest/) with ```IPOPT```.

### File Structure
Each example file contains three documents. 
- The ```.blend``` file contains the final Blender file with code already in the Scripting tab of Blender and already run. This is the final product. 
- The ```.py``` file is the script that is run from within Blender (in the scripting tab). One can observe that it is the same code as what is in the ```.blend``` file's Scripting tab. 
- The ```.csv``` file is the source data from the simulations.
