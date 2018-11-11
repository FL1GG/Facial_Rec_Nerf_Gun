# Nerf_Gun_Shooter
A Face tracking nerf gun designed to annoy.

We set out on a mission to create a face tracking nerf gun and ended up with a trigger happy bot that snapped to heads.  

The Project operates off a two axis system. One motor controls the X axis and the other the Y axis.  (I would not recommend using the motors used in this build as they only work at high speeds.)  A camera is attached to the front of gun and this is how it aligns itself. It also uses a servo for the trigger which has the unintended consquence of firing every time it starts up. (If you're not expecting it, its quite a bang. Did I mention the nerf gun we used had been moded to use an airsoft spring instead of the normal nerf one.)


![A picture of the Beast](https://raw.githubusercontent.com/Auto19/Nerf_Gun_Shooter/master/20181108_160843.jpg)


The code for this is messy but legible. (The current working version is pt2.) How it fuctions is it takes a haar-cascade and parses it over the camera feed and returns a box of the location of the face.  It compares this location to a bit below the center (accounting for camera positioning) and then applies power on both axis in a formula of {distance * constant}.  As the camera centers it slows down and once the crosshair is in the box of the face it activates the shooting sequence.  Then we annoy the face with nerf darts. (Also I should note that the test motor function drives the gun with the WASD keys, in case you need that.)


![Down the barrel](https://raw.githubusercontent.com/Auto19/Nerf_Gun_Shooter/master/20181108_160846.jpg)
