import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import json

class Light(Node):

    def __init__(self,id):
        super().__init__(id,namespace='smt_example/actuator')
        self.subscription = self.create_subscription(
            String,
            '/smt_example/control/light',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.id =id
    # assume the data structure is {"id":"1235","cmd":"0"}
    def listener_callback(self, msg):
        info = json.loads(msg.data)
        if info["id"]==self.id:
            if info["data"]=='0':
                self.get_logger().info("Light "+info["id"]+" turned off")
            elif info["data"]=='1':
                self.get_logger().info("Light "+info["id"]+" turned on")

        


def main(args=None):
    rclpy.init(args=args)

    light= Light("light0")

    rclpy.spin(light)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    light.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()