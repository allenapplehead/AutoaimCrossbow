# AutoaimCrossbow

This project is a turreted autoaiming autoloading crossbow, with a webcam trained using a relatively fast neural net to detect toy soldiers, aim, and shoot them fully automatically. Accuracy is near perfect at 60cm based on initial testing so far.

[![Autoaim Crossbow August 28th Testing](https://img.youtube.com/vi/Op886L5IfEM/0.jpg)](https://youtu.be/Op886L5IfEM)

## Software:
I trained a `SSD MobileNet V2 FPNLite 320x320` object detection model from the TensorFlow Detection Model Zoo to detect green toy soldiers of 3 different types: GreenMachineGunner, GreenMultiGunner, and GreenRadioman. I chose this single shot detector mobilenet due to its high speed as the webcam tracks the targets (toy soldiers) in real time on a live webcam feed. This model is then fed into opencv, which then allows bounding boxes to be drawn around the targets (toy soldiers) live on the camera feed, and informing their exact coordinates, tracking multiple targets at once. As this process is computationally expensive, I am running all code on my computer, and instructing the EV3 Mindstorms brick to execute commands using Christoph Gaukel's ev3 direct commands library `ev3_dc` in python. Multithreading and modified PID control was used to move the pan (turntable) and tilt (tilter) motors to move in a more efficient manner.

## Hardware:
The crossbow was built using LEGO on the EV3 Mindstorms platform. The principle by which the shooting mechanism works was inspired by ats1995's autoloading lego crossbow, while its implementation, along with the rest of the build are original. Shoots consistently out to about 30 inches, and can shoot about 2 projectiles per second. 2 large motors control the crossbow's pan and tilt, which allows it to be aimed by the webcam.

## Next Steps:
* Optimize motion algorithm to allow for faster aiming
* Current neural net has trouble distinguishing between the GreenRadioman and GreenMachineGunner, as they are quite similar especially since they are small and placed far away from the webcam. Retrain model with more steps and better training data to improve this
* Implement tilter to allow for crossbow to shoot targets of varying heights

