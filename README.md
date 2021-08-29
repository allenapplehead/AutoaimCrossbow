# AutoaimCrossbow

This project is an autoaiming autoloading crossbow, with a mounted webcam trained on a fast neural net to detect toy soldiers, aim, and shoot them fully automatically. Shooting accuracy is near perfect at 60cm, and can detect 3 different types of toy soldiers. Click on the image below to see it in action!

<a href="https://youtu.be/BRknQZD5vVs" target="_blank"><img src="https://img.youtube.com/vi/BRknQZD5vVs/0.jpg"></a>

## Software:
I trained a `SSD MobileNet V2 FPNLite 320x320` object detection model from the TensorFlow Detection Model Zoo to detect green toy soldiers of 3 different types: GreenMachineGunner, GreenMultiGunner, and GreenRadioman. I chose this single shot detector mobilenet due to its high speed as the webcam tracks the targets (toy soldiers) in real time on a live webcam feed. This model is then fed into opencv, which then allows bounding boxes to be drawn around the targets (toy soldiers) live on the camera feed, and informing their exact coordinates, tracking multiple targets at once. As this process is computationally expensive, I am running all code on my computer, and instructing the EV3 Mindstorms brick to execute commands using Christoph Gaukel's ev3 direct commands library `ev3_dc` in python. Multithreading and modified PID control was used to move the pan (turntable) and tilt (tilter) motors to move in a more efficient manner.

## Hardware:
The crossbow was built using LEGO on the EV3 Mindstorms platform. The principle by which the shooting mechanism works was inspired by ats1995's autoloading lego crossbow, while its implementation, along with the rest of the build are original. Shoots consistently out to about 30 inches, and can shoot about 2 projectiles per second. Clip size can be as large as you like, as the next round is loaded in by gravity. 2 large motors control the crossbow's pan and tilt, which allows it to be aimed by the webcam.

## Next Steps:
* Optimize motion algorithm to allow for faster aiming
* Improve framerate to allow for a smoother video feed
* Performance tune detect soldiers neural net to better distinguish soldiers at greater distances and with background distractions
* Rebuild tilter to allow for smoother and more accurate control

