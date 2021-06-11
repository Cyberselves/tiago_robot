from launch import LaunchDescription, Substitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare, ExecutableInPackage
from launch.substitutions import Command, PathJoinSubstitution
from typing import List
from launch import LaunchContext
from typing import Text

from launch_pal.arg_utils import read_launch_argument
from tiago_description.tiago_launch_utils import get_tiago_hw_arguments


class TiagoXacroConfigSubstitution(Substitution):
    """
    Substitution extracts the tiago hardware args and passes them
    as xacro variables. Used in launch system
    """

    def __init__(self) -> None:
        super().__init__()
        """
        Construct the substitution
        :param: source_file the original YAML file t
        """

    @property
    def name(self) -> List[Substitution]:
        """Getter for name."""
        return "TIAGo Xacro Config"

    def describe(self) -> Text:
        """Return a description of this substitution as a string."""
        return 'Parses tiago hardware launch arguments into xacro \
        arguments potat describe'

    def perform(self, context: LaunchContext) -> Text:
        """
           Generate the robot description and return it as a string
        """

        laser_model = read_launch_argument("laser_model", context)

        arm = read_launch_argument("arm", context)
        end_effector = read_launch_argument("end_effector", context)
        ft_sensor = read_launch_argument("ft_sensor", context)

        return " laser_model:=" + laser_model + \
            " arm:=" + arm + \
            " end_effector:=" + end_effector + \
            " ft_sensor:=" + ft_sensor


def generate_launch_description():
    parameters = {'robot_description': Command(
        [
            ExecutableInPackage(package='xacro', executable="xacro"),
            ' ',
            PathJoinSubstitution(
                [FindPackageShare('tiago_description'),
                 'robots', 'tiago.urdf.xacro']),
            TiagoXacroConfigSubstitution()
        ])
    }

    rsp = Node(package='robot_state_publisher',
               executable='robot_state_publisher',
               output='both',
               parameters=[parameters])

    tiago_args = get_tiago_hw_arguments(
        laser_model=True,
        arm=True,
        end_effector=True,
        ft_sensor=True,
        default_laser_model="sick-571")

    return LaunchDescription([*tiago_args, rsp])
