# B05_TAS
Python code used by group B05 in Test, Analysis &amp; Simulation. 

Functions:

Import Motion Capture Data

Process Motion Capture Data (filter, etc.)

Visualize and interpret Data in a useful way (graphs, etc)

TODO
1. reconstruct motion of satellite mock-up and base (done)
2. compute the velocity of the base 
- use the X, Y Z coordinates and center difference derivative 
3. filter out the base rotating 
a. removing rows of base moving based on velocity of x y and z by setting a threshold (the flat part)
b. linear interpolation between position of initial position of base and final position after rotation (2 rows removed so 2 nodes in interpolation (4 including initial and final boudary conditions))
4. compute the average/max and standard deviation of the error of the motion - what point are we comparing to what point (ask?)
5. 4.1.	Is the center of the trajectory always in the same position? - does the center change or does the radius change
