import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import json

class Door(Node):

    def __init__(self,id):
        super().__init__(id,namespace='smt_example/actuator')
        self.subscription = self.create_subscription(
            String,
            '/smt_example/control/door',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.id =id
    # assume the data structure is {"id":"1235","cmd":"0"}
    def listener_callback(self, msg):
        info = json.loads(msg.data)
        if info["id"]==self.id:
            if info["cmd"]=='0':
                self.get_logger().info("Door "+info["id"]+" closed")
            elif info["cmd"]=='1':
                self.get_logger().info("Door "+info["id"]+" opened")

        


def main(args=None):
    rclpy.init(args=args)

    door = Door("door0")

    rclpy.spin(door)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    door.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()