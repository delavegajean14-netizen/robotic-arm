# Robotic Arm Control System

A robotic arm control system developed using **Python** and **Arduino**. The application provides a graphical interface for manual joint control, inverse kinematics-based positioning, and automated motion sequence execution through serial communication.

---

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
- Multi-threaded execution for a responsive interface

---

## Technologies

- Python
- Arduino
- Tkinter
- PySerial
- Threading
- Inverse Kinematics
- Robotics

---

## Software Architecture

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

---

## Software Components

### Python Application

- Graphical User Interface
- Manual joint control
- Inverse kinematics
- Motion sequence recording
- Motion sequence playback
- Serial communication
- Servo calibration

### Arduino Firmware

- Receives serial commands from the Python application
- Controls four servo motors
- Executes requested joint positions
- Sends communication feedback to the application

---

## System Overview

The application allows users to control a four-degree-of-freedom robotic arm in two different ways.

### Manual Control

Each joint can be controlled independently using sliders in the graphical interface.

### Cartesian Positioning

Users can enter X, Y, and Z coordinates, and the software computes the required joint angles using inverse kinematics before sending commands to the Arduino.

### Motion Sequences

Users can save multiple robotic arm positions and replay them automatically either once or continuously in loop mode.

## Team Contributions

### Jean Ioseph De la Vega Peña

- Python software development
- GUI development using Tkinter
- Arduino communication
- Inverse kinematics implementation
- Motion sequence system
- Servo calibration
- Software integration
- System testing

### Yessica Edith Ayala Salazar

- Mechanical CAD design of the robotic arm
- Mechanical design support
- Mechanical assembly

---

## Future Improvements

- ROS 2 integration
- Computer vision for object detection
- Pick-and-place automation
- Trajectory interpolation
- Forward kinematics visualization
- End-effector tool support

---

## Gallery

### Graphical User Interface

<p align="center">
  <img src="images/GUI-connected.png" width="700">
</p>

### Demonstration

The repository includes a demonstration video showing the robotic arm executing recorded motion sequences.

---

## Requirements

Install the required Python packages with:

```bash
pip install -r requirements.txt
```

---

## Author

**Jean Ioseph De la Vega Peña**

Robotics Engineering Student

Universidad Politécnica de Santa Rosa Jáuregui
