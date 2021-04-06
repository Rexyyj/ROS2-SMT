#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;
using std::placeholders::_1;
/* This example creates a subclass of Node and uses std::bind() to register a
* member function as a callback from the timer. */

class MinimalSubscriber : public rclcpp::Node
{
  public:
    MinimalSubscriber()
    : Node("minimal_subscriber")
    {
      publisher_ = this->create_publisher<std_msgs::msg::String>("topic2", 10);
      subscription_ = this->create_subscription<std_msgs::msg::String>(
        "topic1",10,std::bind(&MinimalSubscriber::topic_callback,this,_1));

    }

  private:
  void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
  {
    RCLCPP_INFO(this->get_logger(),"I hear: ''%s'",msg->data.c_str());
    auto message = std_msgs::msg::String();
    message.data = msg->data.c_str();
    RCLCPP_INFO(this->get_logger(),"Publishing: '%s'",message.data.c_str());
    publisher_->publish(message);
  }
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

  int main(int argc, char * argv[])
  {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MinimalSubscriber>());
    rclcpp::shutdown();
    return 0;
  }
