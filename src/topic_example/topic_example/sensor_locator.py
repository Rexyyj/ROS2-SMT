# -*- coding: utf-8 -*-
#####################################
# @author [Rex Yu]
# @email  [jiafish@outlook.com]
# @github https://github.com/Rexyyj
# @date   2021-08-19 08:50:33
# @desc 
####################################

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from random import randint
from random import seed
import json
class Locator(Node):

    def __init__(self):
        super().__init__('locator',namespace="smt_example/sensor")
        self.publisher_ = self.create_publisher(String, 'locator', 10)
        timer_period = 2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        seed(1)
        self._msg = {"id":"locator0","data":""}

    def timer_callback(self):
        msg = String()
        val = (randint(25,30),randint(25,30))
        self._msg["data"]=str(val)
        msg.data = json.dumps(self._msg)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    locator0 = Locator()

    rclpy.spin(locator0)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    locator0.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
