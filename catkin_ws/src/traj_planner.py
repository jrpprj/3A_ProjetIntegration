from __future__ import print_function
from distutils.util import execute
from six.moves import input

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

try:
    from math import pi, tau, dist, fabs, cos
except:  # For Python 2 compatibility
    from math import pi, fabs, cos, sqrt

    tau = 2.0 * pi

    def dist(p, q):
        return sqrt(sum((p_i - q_i) ** 2.0 for p_i, q_i in zip(p, q)))


from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("traj_planner", anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface(synchronous=True)

rospy.sleep(2) # latence entre l'interface moveit et python

group_name = "hc10_arm"
move_group = moveit_commander.MoveGroupCommander(group_name)
display_trajectory_publisher = rospy.Publisher(
    "/move_group/display_planned_path",
    moveit_msgs.msg.DisplayTrajectory,
    queue_size=20,
)

def basicInfo():
    # We can get the name of the reference frame for this robot:
    planning_frame = move_group.get_planning_frame()
    print("============ Planning frame: %s" % planning_frame)

    # We can also print the name of the end-effector link for this group:
    eef_link = move_group.get_end_effector_link()
    print("============ End effector link: %s" % eef_link)

    # We can get a list of all the groups in the robot:
    group_names = robot.get_group_names()
    print("============ Available Planning Groups:", robot.get_group_names())

    # Sometimes for debugging it is useful to print the entire state of the
    # robot:
    print("============ Printing robot state")
    print(robot.get_current_state())
    print("")

    return eef_link, planning_frame

def planJointGoal():
    # We get the joint values from the group and change some of the values:
    joint_goal = move_group.get_current_joint_values()
    joint_goal[0] = 0
    joint_goal[1] = 0 #tau / 8
    joint_goal[2] = 0
    joint_goal[3] = 0 #tau / 4
    joint_goal[4] = 0
    joint_goal[5] = 0 #-tau / 6  # 1/6 of a turn

    # The go command can be called with joint values, poses, or without any
    # parameters if you have already set the pose or joint target for the group
    move_group.go(joint_goal, wait=True)

    # Calling ``stop()`` ensures that there is no residual movement
    move_group.stop()

def planPoseGoal():
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.w = 1.0
    pose_goal.position.x = 0.4
    pose_goal.position.y = 0.1
    pose_goal.position.z = 0.4

    move_group.set_pose_target(pose_goal)
    print(pose_goal)

def computePlanExecute():
    # `go()` returns a boolean indicating whether the planning and execution was successful.
    success = move_group.go(wait=True)
    # Calling `stop()` ensures that there is no residual movement
    move_group.stop()
    # It is always good to clear your targets after planning with poses.
    # Note: there is no equivalent function for clear_joint_value_targets().
    move_group.clear_pose_targets()

def cartesianPath(scale = 1.0):
    waypoints = []

    wpose = move_group.get_current_pose().pose
    wpose.position.z -= scale * 0.1  # First move up (z)
    wpose.position.y += scale * 0.4  # and sideways (y)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.x += scale * 0.1  # Second move forward/backwards in (x)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.y -= scale * 0.1  # Third move sideways (y)
    waypoints.append(copy.deepcopy(wpose))

    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0,
    # ignoring the check for infeasible jumps in joint space, which is sufficient
    # for this tutorial.
    (plan, fraction) = move_group.compute_cartesian_path(
        waypoints, 0.01, 0.0  # waypoints to follow  # eef_step
    )  # jump_threshold

    # Note: We are just planning, not asking move_group to actually move the robot yet:
    return plan, fraction

def obstacle(planning_frame, timeout = 10):
    box_pose = geometry_msgs.msg.PoseStamped()
    box_pose.header.frame_id = "world"
    box_pose.pose.orientation.w = 1.0
    box_pose.pose.position.y = 0.52  # above the panda_hand frame
    box_name = "CHIPPIE"
    scene.add_box(box_name, box_pose, size=(0.3, 0.3, 0.3))
    
    #grasping_group = "hc10_arm"
    #touch_links = robot.get_link_names(group=grasping_group)
    scene.attach_box(planning_frame, box_name)

    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
        # Test if the box is in attached objects
        attached_objects = scene.get_attached_objects([box_name])
        print("attached objects", attached_objects)
        is_attached = len(attached_objects.keys()) > 0

        # Test if the box is in the scene.
        # Note that attaching the box will remove it from known_objects
        is_known = box_name in scene.get_known_object_names()
        print("known objects", scene.get_known_object_names())

        # Test if we are in the expected state
        if (True == is_attached) and (True == is_known):
            return box_name, True

        # Sleep so that we give other threads time on the processor
        rospy.sleep(0.1)
        seconds = rospy.get_time()

    # If we exited the while loop without returning then we timed out
    return box_name, False

def collision(timeout = 0.1, box_name = ""):
    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
        # Test if the box is in attached objects
        attached_objects = scene.get_attached_objects([box_name])
        is_attached = len(attached_objects.keys()) > 0

        # Test if the box is in the scene.
        # Note that attaching the box will remove it from known_objects
        is_known = box_name in scene.get_known_object_names()

        # Test if we are in the expected state
        if (True == is_attached) and (True == is_known):
            return True

        # Sleep so that we give other threads time on the processor
        rospy.sleep(0.1)
        seconds = rospy.get_time()

    # If we exited the while loop without returning then we timed out
    return False

eef_link, planning_frame = basicInfo()
planJointGoal()
#planPoseGoal()

#box_name, done = obstacle(planning_frame)
#collision(0.1, box_name)
#print(box_name)

computePlanExecute()

plan, fraction = cartesianPath(scale=1.0)

display_trajectory = moveit_msgs.msg.DisplayTrajectory()
display_trajectory.trajectory_start = robot.get_current_state()
display_trajectory.trajectory.append(plan)
# Publish
display_trajectory_publisher.publish(display_trajectory)

execute_correct = move_group.execute(plan, wait=True)
print("execute", execute_correct)
#if (execute_correct != True):
#    print("! Box in the planning trajectory !")
#    plan, fraction = cartesianPath(scale=1.0)
    
#    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
#    display_trajectory.trajectory_start = robot.get_current_state()
#    display_trajectory.trajectory.append(plan)

#    display_trajectory_publisher.publish(display_trajectory)

#    execute_correct = move_group.execute(plan, wait=True)

#scene.remove_attached_object(planning_frame, name=box_name)
#scene.remove_world_object(box_name)