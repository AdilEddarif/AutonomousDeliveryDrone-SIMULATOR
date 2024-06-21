#!/usr/bin/env python
# Import ROS.
import rospy
# Import the API.
from iq_gnc.py_gnc_functions import *
# To print colours (optional).
from iq_gnc.PrintColours import *


def main():
    # Initializing ROS node.
    rospy.init_node("drone_controller", anonymous=True)

    # Create an object for the API.
    drone = gnc_api()
    # Wait for FCU connection.
    drone.wait4connect()
    # Wait for the mode to be switched.
    drone.wait4start()

    # Create local reference frame.
    drone.initialize_local_frame()
    # Request takeoff with an altitude of 3m.
    drone.takeoff(3)
    # Specify control loop rate. We recommend a low frequency to not overload the FCU with messages. Too many messages will cause the drone to be sluggish.
    rate = rospy.Rate(3)

    # Log current position and orientation before setting yaw
    current_position = drone.get_current_location()
    current_orientation = drone.get_current_heading()
    rospy.loginfo(f"Initial position: {current_position}")
    rospy.loginfo(f"Initial orientation: {current_orientation} degrees")

    # Explicitly set the yaw to 0 to ensure the drone is facing forward
    rospy.loginfo("Setting initial yaw to 0 degrees.")
    drone.set_destination(x=0, y=0, z=3, psi=0)

    # Wait until the yaw is set
    rospy.sleep(5)  # wait for 5 seconds to ensure the orientation is set

    # Log the new orientation to verify it's set correctly
    current_orientation = drone.get_current_heading()
    rospy.loginfo(f"Orientation after setting yaw: {current_orientation} degrees")

    # Specify the goal to move forward 20 meters along the X-axis
    rospy.loginfo("Setting destination to move forward 20 meters.")
    goal = [20, 0, 3, -90]

    # Move to the specified goal
    drone.set_destination(x=goal[0], y=goal[1], z=goal[2], psi=goal[3])

    # Wait until the waypoint is reached
    while not drone.check_waypoint_reached():
        rospy.loginfo("Moving towards the goal...")
        rate.sleep()

    # Land after the waypoint is reached
    drone.land()
    rospy.loginfo(CGREEN2 + "Goal reached, landing now." + CEND)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
