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
--> 
plot x, t unfiltered(raw data) and on all flat part, find position = waypoints (velocity in x direction = 0 but filter noises) (for 0 velocity, maybe use all 3 dimensions)
with these waypoints - trajectory of tip of arm 

method
- first method attempted was to plot the raw data of the x position over time. Since the data looks like a decreasing step function by making a function which looks at the maneuvre duration and notes the start and end of the maneuvre. with this start/end, we are able to segment when the velocity is approximately 0 and when it is not. It worked, no further method required.
- an alternative that could have been implemented is by using the ruptures package which is also used for the analysis and segmentation of non-stationary signals. - https://www.sciencedirect.com/science/article/pii/S0165168419303494


4. compute the average/max and standard deviation of the error of the motion - what point are we comparing to what point
5. 4.1.	Is the center of the trajectory always in the same position? - does the center change or does the radius change

Y-pos
- take1 : +-2.5
- take2 : +0.75 -0.6 
- take3 : +-0.6
- take4 : +-0.6
- take5

