
# KUKA KVP Command ROS1 Package

## Robot: KUKA Agilus R900-2


## Overview

This ROS1 (Robot Operating System) package provides an interface for the KUKA Agilus R900-2 robot arm. It enables users to programmatically control the arm, facilitating the development of complex automation scripts and programs within the ROS ecosystem. The package is based on the KVP (KUKA Variable Protocol) for communication with the robot controller. It was originally inspired by:
- [kuka_kvp_hw_interface](https://github.com/itk-thrivaldi/kuka_kvp_hw_interface)
- kvp protocol

## Features

- ROS1 Interface of the KUKA Agilus R900-2 arm
- Tested on ROS1 Noetic & Ubuntu 20.04
- KVP protocol implementation for robot communication

## Prerequisites

- ROS1 Noetic
- Ubuntu 20.04
- KUKA Agilus R900-2 robot arm and controller
	- Tested on the KRC4 controller

## Installation and Setup

### 1. Robot Ethernet Interface Setup

Try following the instructions in the links below. Better documentation is coming soon
- [Connecting KUKA robots to your windows PC](https://camerabotics.com/help-center/hardware-setup/robots/kuka/connecting-kuka-robots-to-your-windows-pc/)
- [KUKA Setup Instructions](https://docs.mech-mind.net/en/robot-integration/latest/standard-interface-robot/kuka-setup-instructions.html)

### 2. Robot KVP Server Setup

**You MUST log in as an Administrator in the Teach Pendant for the steps below.**

This server is a TCP Server built on Visual Basic that allows connection between the Remote PC's client program (Custom ROS1 Node) and the controller's KVP space.
Read more about the server here.

- Download the server from [here](https://github.com/ImtsSrl/KUKAVARPROXY/tree/master)
- Copy it to a USB stick
- The USB stick is then inserted in the Teach Pendant's USB Port
- [Admin Role] On the Teach Pendant, go to *`KUKA > Startup > Minimize HMI`*
- Use the File Explorer to view files in the USB. Copy the KUKAVARPROXY folder onto the Desktop
- Click on the **KukavarProxy.exe** in the *`src/`* directory
- In case you get an error (`cswsk32.ocx missing`)  follow the instructions [here](https://github.com/ImtsSrl/KUKAVARPROXY/issues/18) to resolve the issue.
- Additionally, you can add the server to Windows Startup Programs so that it starts automatically whenever the robot is powered up.
- Click on the Controller Interface icon to return to the main interface for the upcoming steps.
- The server communicates via TCP on Port 7000. Therefore, we must allow this port from the Controller so that external communication is allowed.
- On the Teach Pendant, navigate to *`Startup > NetworkConfiguration > NAT`*
	- **AddPort:** 7000 TCP/UDP

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
- You have Ubuntu 20.04 installed on your system, or
- You have an Ubuntu 20.04 docker container running.
	- A docker image with the necessary setup will be provided once ready by clicking < here >

First, set up your ROS1 workspace:

```bash
mkdir -p robot_ws/src
cd robot_ws
catkin_make
source devel/setup.bash
```

### 2. Package Dependencies

#### a. kuka_experimental

**Importance:**  getting the KUKA KR6 files e.g. URDF files used for robot_description

```bash
cd robot_ws/src
git clone https://github.com/ros-industrial/kuka_experimental.git
cd ..
rosdep install --from-paths src --ignore-src
catkin_make
```

#### b. kuka_kvp_hw_interface

**Importance:** getting access to the robot's joint states

```bash
cd robot_ws/src
git clone https://github.com/itk-thrivaldi/kuka_kvp_hw_interface
cd ..
rosdep install --from-paths src --ignore-src

# Edit params.yaml to your robot's IP Address
catkin_make
```
- Ensure that you've edited the `params.yaml` file in the `kuka_kvp_hw_interface/config/` directory to include your robot's IP address.
	- For example: Change from the default address **`10.0.0.1`** to **`172.31.1.147`**

#### c. kuka_kvp_command_interface

**Importance:** This is the package of interest.

```bash
cd robot_ws/src
git clone https://github.com/codewithlennylen/kuka-kvp-command
cd ..
rosdep install --from-paths src --ignore-src
catkin_make
```

## Usage

#### Prerequisite
- You are running the commands below in the Docker Container or Ubuntu 20.04 system with ROS1 Noetic Installed.

---

To use the package and its dependencies, you need to run several commands in different terminal sessions:

1. Start the ROS master:
   ```bash
   roscore
   ```

2. Send data (in the example provided, we are sending different predefined joint positions) to the robot via KVP:
   ```bash
   rosrun kuka_kvp_command_interface send_to_robot
   ```

3. Send demo coordinates (joint positions):
   ```bash
   rosrun kuka_kvp_command_interface simulate_coordinates
   ```
- For the robot to move to the different positions, the **Start Key** on the Teach Pendant needs to be pressed (if operating in **T1 Mode**)
	- **Press and Release** the Play Button to first initialize the arm's position
	- **Press and Hold** the Play button for the Robot Arm to move to the target positions (demo coordinates)

4. Get live joint states from the arm:
   ```bash
   roslaunch kuka_kvp_hw_interface test_joint_trajectory_interface.launch
   ```

5. Visualize the robot's movements:
   ```bash
   rviz
   ```
- In RViz, set the map to base
- Click Plugins: add TF and Robot Model



## Troubleshooting

- 

## Contributing

- 

## License

- 

## Contact

- **Maintainer: Lenny Ng'an'ga** 
	- X (formerly Twitter): [@codewithlenny](https://x.com/@codewithlenny)
	- LinkedIn: [Lenny Ng'ang'a](https://www.linkedin.com/in/lenny-nganga-wanjiru/)
