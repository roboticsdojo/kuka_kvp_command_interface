
  

# KUKA KVP Command Interface

  

## Tested on: KUKA Agilus KR6 R900-2

  
  

## Overview

  

This ROS2 (Robot Operating System) package provides an interface for the KUKA Agilus KR6 R900-2 robot arm. It enables users to programmatically control the arm, facilitating the development of complex automation scripts and programs within the ROS ecosystem. The package is based on the KVP (KUKA Variable Protocol) for communication with the robot controller. It was originally inspired by:

-  **[kuka_kvp_hw_interface](https://github.com/itk-thrivaldi/kuka_kvp_hw_interface)**
- **[kukavarproxy-msg-format](https://github.com/akselov/kukavarproxy-msg-format)**

- kvp protocol

  

## Features

  

- ROS2 Interface of the KUKA Agilus KR6 R900-2 arm

- Tested on ROS2 Humble & Ubuntu 22.04

- KVP protocol implementation for robot communication

  

## Prerequisites

  

- ROS2 Humble

- Ubuntu 22.04

- KUKA Agilus KR6 R900-2 Robot Arm

- KR C4 Compact controller

  

## Installation and Setup

  

### 1. Robot Ethernet Interface Setup

  

Try following the instructions in the links below. Better documentation is coming soon

-  [Connecting KUKA robots to your windows PC](https://camerabotics.com/help-center/hardware-setup/robots/kuka/connecting-kuka-robots-to-your-windows-pc/)

-  [KUKA Setup Instructions](https://docs.mech-mind.net/en/robot-integration/latest/standard-interface-robot/kuka-setup-instructions.html)

  

### 2. Robot KVP Server Setup

  

**You MUST log in as an Administrator in the Teach Pendant for the steps below.**

  

This server is a TCP Server built on Visual Basic that allows connection between the Remote PC's client program (Custom ROS2 Node) and the controller's KVP space.

Read more about the server [here](https://github.com/ImtsSrl/KUKAVARPROXY/tree/master?tab=readme-ov-file).

  

- Download the server from [here](https://github.com/ImtsSrl/KUKAVARPROXY/tree/master)

- Copy it to a USB stick

- The USB stick is then inserted in the Teach Pendant's USB Port

- [Admin Role] On the Teach Pendant, go to *`KUKA > Startup > Minimize HMI`*

- Use the File Explorer to view files in the USB. Copy the KUKAVARPROXY folder onto the Desktop

- Click on the **KukavarProxy.exe** in the *`src/`* directory

- In case you get an error (`cswsk32.ocx missing`) follow the instructions [here](https://github.com/ImtsSrl/KUKAVARPROXY/issues/18) to resolve the issue.

- Additionally, you can add the server to Windows Startup Programs so that it starts automatically whenever the robot is powered up.

- Click on the Controller Interface icon to return to the main interface for the upcoming steps.

- The server communicates via TCP on Port 7000. Therefore, we must allow this port from the Controller so that external communication is allowed.

- On the Teach Pendant, navigate to *`Startup > NetworkConfiguration > NAT`*

-  **AddPort:** 7000 TCP/UDP

  

### 3. Robot KRL Script Setup

  

This script reads from the KVP space and moves the robot arm to the target position if the current position is not equal to the target position.

  

- The script in the *`KRL/`* folder of this repository should be copied to a USB Stick

- The USB stick is then inserted in the Teach Pendant's USB Port

- Copy the script to the location: *`R/Program/`*

- Click on the script, then press the *`Select`* option that appears at the bottom of the Teach Pendant.

- Once done, proceed to setting up your PC or laptop (I'll refer to this as the Remote PC) by following the steps below.

- We will come back to this script later on.

  

### 4. Remote PC Environment Setup

  

#### Assumptions

- You have Ubuntu 22.04 installed on your system, or

- You have an Ubuntu 22.04 docker container running.

- A docker image with the necessary setup will be provided once ready.

  

#### First, set up your ROS2 workspace:

  

```bash

mkdir  -p  robot_ws/src

cd  robot_ws

colcon build

source  install/setup.bash

```

  

#### Setup the kuka_kvp_command_interface package  

```bash

cd  robot_ws/src

# Clone Using HTTPS
git  clone  https://github.com/roboticsdojo/kuka_kvp_command_interface.git

# Or clone using SSH (If you have set up SSH)
git clone git@github.com:roboticsdojo/kuka_kvp_command_interface.git

rosdep  install  -y  --from-paths  .  --ignore-src

# Build packages

cd  ..

colcon build

```

  

## Usage

  

#### Prerequisite

- You are running the commands below in the Docker Container or Ubuntu 22.04 system with ROS2 Humble Installed and Sourced.

  

---

  

To use the package and its examples, you need to run several commands in different terminal sessions:

  

1. Start the kuka_kvp_interface node:

```bash

ros2 run kuka_kvp_command_interface kuka_kvp_interface

```

 
2. Send demo coordinates (we are sending different predefined joint positions):

```bash

ros2 run kuka_kvp_command_interface simulate_coordinates

```

- For the robot to move to the different positions, the **Start Key** on the Teach Pendant needs to be pressed (if operating in **T1 Mode**)

-  **Press and Release** the Play Button to first initialize the arm's position

-  **Press and Hold** the Play button for the Robot Arm to move to the target positions (demo coordinates)


 ## Work in progress

1. Get live joint states from the arm
2. Visualize the robot's movements (live joint states)
3. Simulate the Robot in gazebo

  
  
  

## Troubleshooting

  

-

  

## Contributing

  

-

## License

This project is licensed under the Apache License 2.0. You are free to use, modify, and distribute this software under the terms of the license.

For more details, see the [LICENSE](LICENSE) file in the repository or visit the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0) page.


## Contact

  

-  **Maintainer: Lenny Ng'an'ga**
- X (formerly Twitter): [@codewithlenny](https://x.com/@codewithlenny)
- LinkedIn: [Lenny Ng'ang'a](https://www.linkedin.com/in/lenny-nganga-wanjiru/)
- Email: codewithlennylen254@gmail.com
