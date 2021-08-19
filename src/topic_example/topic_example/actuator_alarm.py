# -*- coding: utf-8 -*-
#####################################
# @author [Rex Yu]
# @email  [jiafish@outlook.com]
# @github https://github.com/Rexyyj
# @date   2021-08-19 08:49:43
# @desc 
####################################

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import json

class Alarm(Node):

    def __init__(self,id):
        super().__init__(id,namespace='smt_example/actuator')
        self.subscription = self.create_subscription(
            String,
            '/smt_example/control/alarm',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.id =id
    # assume the data structure is {"id":"1235","cmd":"0"}
    def listener_callback(self, msg):
        info = json.loads(msg.data)
        if info["id"]==self.id:
            if info["cmd"]=='0':
                self.get_logger().info("Alarm "+info["id"]+" deactivated")
            elif info["cmd"]=='1':
                self.get_logger().info("Alarm "+info["id"]+" activated")

        


def main(args=None):
    rclpy.init(args=args)

    alarm = Alarm("light0")

    rclpy.spin(alarm)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    alarm.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()