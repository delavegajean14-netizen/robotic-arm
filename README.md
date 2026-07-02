# Robotic Arm Control System

A robotic arm control system developed using **Python** and **Arduino**. The application provides a graphical interface for manual joint control, inverse kinematics-based positioning, and automated motion sequence execution through serial communication.

## Features

- Manual joint control using sliders
- Cartesian positioning through inverse kinematics
- Serial communication with Arduino
- Graphical User Interface (Tkinter)
- Servo calibration and offset management
- Motion sequence recording
- Automatic sequence playback
- Loop mode for continuous execution
- Home position reset
- Event logging
- Multi-threaded execution to keep the interface responsive

## Technologies

- Python
- Arduino
- Tkinter
- PySerial
- Threading
- Inverse Kinematics
- Robotics

## System Overview

The application allows users to control a four-degree-of-freedom robotic arm in two different ways:

### Manual Control

Each joint can be controlled independently using sliders in the graphical interface.

### Cartesian Positioning

Users can enter X, Y, and Z coordinates, and the software computes the required joint angles using inverse kinematics before sending the commands to the Arduino.

### Motion Sequences

Users can save multiple arm positions and replay them automatically either once or in an infinite loop.

## Project Structure

```
Python GUI
    │
    ├── Manual Joint Control
    ├── Inverse Kinematics
    ├── Motion Sequence Manager
    └── Serial Communication
              │
              ▼
          Arduino
              │
              ▼
        Servo Motors
```

## Team Contributions

### Jean De la Vega

- Python application development
- GUI development using Tkinter
- Arduino communication
- Inverse kinematics implementation
- Motion sequence system
- Servo calibration
- Software integration and testing

### Yessica Edith Ayala Salazar

- Mechanical CAD design of the robotic arm
- Mechanical assembly and design support

## Future Improvements

- ROS 2 integration
- Computer vision for object detection
- Pick-and-place automation
- Trajectory interpolation
- Forward kinematics visualization
- End-effector tool support

## License

This project is available under the MIT License.
