# OpenCV_RobotArm

Here's 3-degree-of-freedom robot arm I designed from scratch in solidworks, inspired by the half-pantograph linkage mechanism seen on top of electric trains. Both links of the arm are controlled by stationary motors, and the claw uses a compliant mechanism!

Code was done in arduino and python. The robotArm.py file uses the Machine Learning-powered Mediapipe library in OpenCV, on order to detect hands and extract position data. This information is sent to the arduino (robotArm.ino), which moves the two joints, rotates the base, and opens/closes the claw accordingly. 
