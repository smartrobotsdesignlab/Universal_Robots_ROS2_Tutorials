# Universal Robots ROS 2 tutorials
This package contains tutorials around the ROS 2 packages for Universal Robots.

## Getting started
To use the tutorials from this repository, please make sure to [install ROS
2](https://docs.ros.org/en/humble/Installation.html) on your system. This branch is for ROS Humble
only.

With that, please create a workspace, clone this repo into the workspace, install the dependencies
and build the workspace.

1. Create a colcon workspace:
   ```
   export COLCON_WS=~/workspaces/ur_tutorials
   mkdir -p $COLCON_WS/src
   ```

1. Download the required repositories and install package dependencies:
   ```
   cd $COLCON_WS
   git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Tutorials.git src/ur_tutorials
   rosdep update && rosdep install --ignore-src --from-paths src -y
   ```

1. Create a colcon workspace:
   ```
   cd $COLCON_WS
   colcon build
   ```

1. Source your workspace
   ```
   source $COLCON_WS/install/setup.bash
   ```

1. Launch with fake hardware to confirm installation
   ```
   ros2 launch my_dual_robot_cell_control start_robots.launch.py alice_use_mock_hardware:=true bob_use_mock_hardware:=true alice_ur_type:=ur5e bob_ur_type:=ur5e

   ```
