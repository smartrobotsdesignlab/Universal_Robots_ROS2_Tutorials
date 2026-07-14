from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterFile
from launch_ros.substitutions import FindPackageShare





def generate_launch_description():
    declared_arguments = []
    # UR specific arguments
    declared_arguments.append(
        DeclareLaunchArgument(
            "alice_ur_type",
            description="Type/series of used UR robot.",
            choices=[
                "ur3",
                "ur3e",
                "ur5",
                "ur5e",
                "ur10",
                "ur10e",
                "ur16e",
                "ur20",
                "ur30",
            ],
            default_value="ur3e",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "bob_ur_type",
            description="Type/series of used UR robot.",
            choices=[
                "ur3",
                "ur3e",
                "ur5",
                "ur5e",
                "ur10",
                "ur10e",
                "ur16e",
                "ur20",
                "ur30",
            ],
            default_value="ur3e",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "alice_robot_ip",
            default_value="192.168.0.101",
            description="IP address by which alice can be reached.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "bob_robot_ip",
            default_value="192.168.0.100",
            description="IP address by which bob can be reached.",
        )
    )

    # General arguments
    declared_arguments.append(
        DeclareLaunchArgument(
            "description_launchfile",
            default_value=PathJoinSubstitution(
                [
                    FindPackageShare("my_dual_robot_cell_control"),
                    "launch",
                    "rsp_proper.launch.py",
                ]
            ),
            description="Launchfile (absolute path) providing the description. "
            "The launchfile has to start a robot_state_publisher node that "
            "publishes the description topic.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "alice_use_mock_hardware",
            default_value="true",
            description="Start alice with mock hardware mirroring command to its states.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "bob_use_mock_hardware",
            default_value="true",
            description="Start bob with mock hardware mirroring command to its states.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "alice_mock_sensor_commands",
            default_value="true",
            description="Enable mock command interfaces for alice's sensors used for simple simulations. "
            "Used only if 'use_mock_hardware' parameter is true.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "bob_mock_sensor_commands",
            default_value="true",
            description="Enable mock command interfaces for bob's sensors used for simple simulations. "
            "Used only if 'use_mock_hardware' parameter is true.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "headless_mode",
            default_value="false",
            description="Enable headless mode for robot control for both arms.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "controller_spawner_timeout",
            default_value="10",
            description="Timeout used when spawning controllers.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "alice_initial_joint_controller",
            default_value="alice_scaled_joint_trajectory_controller",
            description="Initially loaded robot controller for the alice robot arm.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "bob_initial_joint_controller",
            default_value="bob_scaled_joint_trajectory_controller",
            description="Initially loaded robot controller for the bob robot arm.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "alice_activate_joint_controller",
            default_value="true",
            description="Activate loaded joint controller for the alice robot arm.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "bob_activate_joint_controller",
            default_value="true",
            description="Activate loaded joint controller for the bob robot arm.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "launch_rviz", default_value="true", description="Launch RViz?"
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "rviz_config_file",
            default_value=PathJoinSubstitution(
                [FindPackageShare("my_dual_robot_cell_description"), "rviz", "urdf.rviz"]
            ),
            description="RViz config file (absolute path) to use when launching rviz.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "alice_launch_dashboard_client",
            default_value="true",
            description="Launch Dashboard Client?",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "bob_launch_dashboard_client",
            default_value="true",
            description="Launch Dashboard Client?",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "alice_kinematics_parameters_file",
            default_value=PathJoinSubstitution(
                [
                    FindPackageShare("my_dual_robot_cell_control"),
                    "config",
                    "alice_calibration.yaml",
                ]
            ),
            description="The calibration configuration of alice.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "bob_kinematics_parameters_file",
            default_value=PathJoinSubstitution(
                [
                    FindPackageShare("my_dual_robot_cell_control"),
                    "config",
                    "bob_calibration.yaml",
                ]
            ),
            description="The calibration configuration of bob.",
        )
    )

    # General arguments
    alice_ur_type = LaunchConfiguration("alice_ur_type")
    bob_ur_type = LaunchConfiguration("bob_ur_type")

    alice_robot_ip = LaunchConfiguration("alice_robot_ip")
    bob_robot_ip = LaunchConfiguration("bob_robot_ip")
    controllers_file = LaunchConfiguration("controllers_file")
    controller_spawner_timeout = LaunchConfiguration("controller_spawner_timeout")
    description_launchfile = LaunchConfiguration("description_launchfile")

    rsp = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(description_launchfile),
        launch_arguments={
            "alice_robot_ip": alice_robot_ip,
            "bob_robot_ip": bob_robot_ip,
            "alice_ur_type": alice_ur_type,
            "bob_ur_type": bob_ur_type,
        }.items(),
    )

    return LaunchDescription(declared_arguments + [rsp])
