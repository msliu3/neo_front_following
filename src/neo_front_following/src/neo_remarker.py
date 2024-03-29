#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ros_marker.py    
@Contact :   liumingshanneo@163.com

@Modify Time      @Author    @Version
------------      -------    --------
2019/11/28 11:49   msliu      1.0      

@Description
------------
None
"""

# !/usr/bin/env python
import rospy
from people_msgs.msg import PositionMeasurementArray
# from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose2D


class ExtractLegDetector(object):
    """docstring for extract_leg_detector"""

    def __init__(self):
        super(ExtractLegDetector, self).__init__()

        self.pub = rospy.Publisher('neo_marker', Marker, queue_size=10)
        rospy.init_node('neo_talker_leg', anonymous=True)
        self.robot_x = 0
        self.robot_y = 0

    def leg_callback(self, data):
        # rospy.loginfo(rospy.get_caller_id() + "\nI heard %s", data.people[0].object_id)
        people = data.people
        # item = self.people
        print("test")
        for item in people:
            if -0.3 < (item.pos.x) < 0.3 and -0.3 < (item.pos.y-self.robot_y) < 0.3:
                print("name: " + item.name)
                print("object_id: " + item.object_id)
                print("Point: " + str(item.pos.x) + " " + str(item.pos.y) + " " + str(item.pos.z))
                print("reliability: " + str(item.reliability))

    def listener_pose2D(self):
        # rospy.init_node('neo_listener_leg', anonymous=True)
        rospy.Subscriber("/pose2D", Pose2D, self.pose2D)

    def pose2D(self,data):
        # print("yes")
        self.robot_x = data.x
        self.robot_y = data.y
        pass

    def listener_leg_tracker_measurements(self):
    # rospy.init_node('neo_listener_leg', anonymous=True)
        rospy.Subscriber("/leg_tracker_measurements", PositionMeasurementArray, self.leg_callback)

    def marker_callback(self, data):
        #this position is base line 
        if -0.2 < (data.pose.position.x -self.robot_x) < 0.46 and -0.275 < (data.pose.position.y -self.robot_y )< 0.275:
            try:
                if data.text != "" and -1< float(data.text) < 0.8:
                    rospy.loginfo("Point: " + str(data.pose.position.x) + " " + str(data.pose.position.y) + " " + str(data.pose.position.z))
                    rospy.loginfo("reliability: " + data.text)
                    self.pub.publish(data)
            except Exception as e:
                raise
            else:
                pass
            finally:
                pass
        pass

    def listener_visualization_marker(self):
        rospy.Subscriber("/visualization_marker", Marker, self.marker_callback)
        pass

if __name__ == '__main__':
    ed = ExtractLegDetector()
    ed.listener_visualization_marker()
    print("hehe")
    ed.listener_pose2D()
    # ed.listener_leg_tracker_measurements()
    rospy.spin()



