# -*- coding: utf-8 -*-
#####################################
# @author [Rex Yu]
# @email  [jiafish@outlook.com]
# @github https://github.com/Rexyyj
# @date   2021-08-19 08:50:19
# @desc 
####################################

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import json

class Controller(Node):

    def __init__(self,id):
        super().__init__(id,namespace='smt_example/control')
        self.sub1 = self.create_subscription(
            String,
            '/smt_example/sensor/infrared',
            self.listener_callback1,
            10)
        self.sub2 = self.create_subscription(
            String,
            '/smt_example/sensor/locator',
            self.listener_callback2,
            10)
        self.sub3 = self.create_subscription(
            String,
            '/smt_example/sensor/smoke',
            self.listener_callback3,
            10)
        self.sub4 = self.create_subscription(
            String,
            '/smt_example/sensor/temperature',
            self.listener_callback4,
            10)
        self.sub1  # prevent unused variable warning
        self.sub2
        self.sub3
        self.sub4
        self.pubLight = self.create_publisher(String, 'light', 10)
        self.pubDoor = self.create_publisher(String, 'door', 10)
        self.pubAlarm = self.create_publisher(String, 'alarm', 10)
        self.id =id
        self.temp=0
    # assume the data structure is {"id":"1235","cmd":"0"}
    def listener_callback1(self, msg):
        info = json.loads(msg.data)
        if int(info["data"])==1:
            self.pub_light(1)
            self.pub_door(1)
        else:
            self.pub_light(0)
            self.pub_door(0)

    def listener_callback2(self, msg):
        info = json.loads(msg.data)
        pass

    def listener_callback3(self, msg):
        info = json.loads(msg.data)
        if int(info["data"])==1 and self.temp>50:
            self.pub_alarm(1)
        else:
            self.pub_alarm(0)
    
    def listener_callback4(self, msg):
        info = json.loads(msg.data)
        temp = int(info["data"])
        self.temp=temp

    def pub_light(self,cmd,id = "light0"):
        msg = String()
        _msg={"id":id,"cmd":str(cmd)}
        msg.data = json.dumps(_msg)
        self.pubLight.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

    def pub_door(self,cmd,id = "door0"):
        msg = String()
        _msg={"id":id,"cmd":str(cmd)}
        msg.data = json.dumps(_msg)
        self.pubDoor.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
    
    def pub_alarm(self,cmd,id = "alarm0"):
        msg = String()
        _msg={"id":id,"cmd":str(cmd)}
        msg.data = json.dumps(_msg)
        self.pubAlarm.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)



def main(args=None):
    rclpy.init(args=args)

    control= Controller("control0")

    rclpy.spin(control)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    control.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()