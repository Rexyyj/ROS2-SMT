import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from random import randint
from random import seed
import json
class Infrared(Node):

    def __init__(self):
        super().__init__('infrared',namespace="smt_example/sensor")
        self.publisher_ = self.create_publisher(String, 'sensor/infrared', 10)
        timer_period = 10  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        seed(1)
        self._msg = {"id":"infrared0","data":""}

    def timer_callback(self):
        msg = String()
        val = randint(0,1)
        self._msg["data"]=str(val)
        msg.data = json.dumps(self._msg)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    infrared0 = Infrared()

    rclpy.spin(infrared0)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    infrared0.destroy_node()
    rclpy.shutdown()



if __name__ == "__main__":
    main()
