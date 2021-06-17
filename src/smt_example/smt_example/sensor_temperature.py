import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from random import randint
from random import seed
import json
class Temp(Node):

    def __init__(self):
        super().__init__('temperature',namespace="smt_example/sensor")
        self.publisher_ = self.create_publisher(String, 'sensor/temperature', 10)
        timer_period = 10  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        seed(1)
        self._msg = {"id":"temp0","data":""}

    def timer_callback(self):
        msg = String()
        val = randint(25,30)
        self._msg["data"]=str(val)
        msg.data = json.dumps(self._msg)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    temp0 = Temp()

    rclpy.spin(temp0)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    temp0.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
