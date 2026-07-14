import os
from pathlib import Path

import yaml
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from moveit_configs_utils import MoveItConfigsBuilder


def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path) as file:
            return yaml.safe_load(file)
    except OSError:
        return None

def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


def generate_launch_description():
    # Load custom Xacro file

    xacro_file_path = os.path.join(
        get_package_share_directory("my_dual_robot_cell_control"), 
        "urdf",
        "my_dual_robot_cell_jig.urdf.xacro"
    )
    

    doc = xacro.process_file(xacro_file_path)
    robot_description_config = doc.toxml()



    controllers_yaml = load_yaml(
    "my_dual_robot_cell_moveit_config", "config/moveit_controllers.yaml"
    )
    print("[DEBUG] Controllers YAML:", controllers_yaml)

    robot_description_semantic_config = load_file(
        "my_dual_robot_cell_moveit_config", "config/my_dual_robot_cell_tube_jig.srdf"
    )
    kinematics_yaml = load_yaml(
        "my_dual_robot_cell_moveit_config", "config/kinematics.yaml"
    )
    robot_description_kinematics = {"robot_description_kinematics": kinematics_yaml}


    robot_description_semantic = {
        "robot_description_semantic": robot_description_semantic_config
    }
    moveit_controllers = controllers_yaml 

    trajectory_execution = {
        "moveit_manage_controllers": True,
        "trajectory_execution.allowed_execution_duration_scaling": 1.2,
        "trajectory_execution.allowed_goal_duration_margin": 0.5,
        "trajectory_execution.allowed_start_tolerance": 0.01,
    }
    ompl_planning_pipeline_config = {
        "move_group": {
            "planning_plugin": "ompl_interface/OMPLPlanner",
            "request_adapters": """default_planner_request_adapters/AddTimeOptimalParameterization default_planner_request_adapters/ResolveConstraintFrames default_planner_request_adapters/FixWorkspaceBounds default_planner_request_adapters/FixStartStateBounds default_planner_request_adapters/FixStartStateCollision default_planner_request_adapters/FixStartStatePathConstraints""",
            "start_state_max_bounds_error": 0.1,
        }
    }

    ompl_planning_yaml = load_yaml(
        "my_dual_robot_cell_moveit_config", "config/ompl_planning.yaml"
    )
    ompl_planning_pipeline_config["move_group"].update(ompl_planning_yaml)

    # Move group configuration
    move_group_configuration = {
        "publish_robot_description_semantic": True,
        # "allow_trajectory_execution": True,
        "publish_planning_scene": True,
        "publish_geometry_updates": True,
        "publish_state_updates": True,
        "publish_transforms_updates": True,
    }

    move_group_params = [
        {"robot_description": robot_description_config,
        #  "use_sim_time": True,
        #  "joint_state_topic": "/joint_states"
         },
        
        robot_description_semantic,
        robot_description_kinematics,
        trajectory_execution,
        ompl_planning_pipeline_config,
        
        moveit_controllers,
        move_group_configuration,
    ]

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        name="move_group",
        output="screen",
        parameters=move_group_params,
        additional_env={"DISPLAY": ":0"},
    )

    # RViz
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("my_dual_robot_cell_moveit_config"), "config", "moveit.rviz"]
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[{
            "robot_description": robot_description_config,
            "frame_prefix": "",
            "use_sim_time": False,
            "publish_frequency": 50.0,
            "tf_prefix": "",
            "ignore_timestamp": False
        }],
        # remappings=[("/joint_states", "/joint_states")],
        output="screen"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2_moveit",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[
            {"robot_description": robot_description_config},
            
            robot_description_kinematics,
            
            #ompl_planning_pipeline_config,
            
            robot_description_semantic,
        ],
    )


    fake_clock_node = Node(
        package="moveit_nodes",
        executable="fake_clock_publisher",
        name="fake_clock_node",
        output="screen",
    )

    

    return LaunchDescription([
        move_group_node,
        rviz_node,
        robot_state_publisher,
        #fake_clock_node,
    ])
    
