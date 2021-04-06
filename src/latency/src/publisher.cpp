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

class MinimalPublisher : public rclcpp::Node
{
  public:
    MinimalPublisher()
    : Node("minimal_publisher"), count_(0)
    {
      publisher_ = this->create_publisher<std_msgs::msg::String>("topic1", 10);
      subscription_ = this->create_subscription<std_msgs::msg::String>(
        "topic2",10,std::bind(&MinimalPublisher::topic_callback,this,_1));

      timer_ = this->create_wall_timer(
      500ms, std::bind(&MinimalPublisher::timer_callback, this));

    }

  private:

    void timer_callback()
    {
      auto message = std_msgs::msg::String();
      message.data = "Hello, world! " + std::to_string(count_++);
      RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
      this->start_time = std::chrono::high_resolution_clock::now();	
      publisher_->publish(message);
      
    }
    void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
    {
      uint64_t total_latency = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::now()-start_time).count();
      RCLCPP_INFO(this->get_logger(),"I hear: ''%s',latency %d us",msg->data.c_str(),total_latency/2);


    }
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
    size_t count_;
    std::chrono::time_point<std::chrono::high_resolution_clock> start_time;
    //mutable std::chrono::time_point<std::chrono::high_resolution_clock> end_time;
  };

  int main(int argc, char * argv[])
  {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MinimalPublisher>());
    rclcpp::shutdown();
    return 0;
  }
