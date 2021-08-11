FROM osrf/ros:foxy-desktop 
RUN apt-get update && apt-get install -y ros-${ROS_DISTRO}-cyclonedds ros-${ROS_DISTRO}-rmw-implementation ros-${ROS_DISTRO}-rmw-cyclonedds-cpp ros-${ROS_DISTRO}-demo-nodes-cpp ros-${ROS_DISTRO}-demo-nodes-py python3-pip openjdk-8-jdk openjdk-8-jre&& rm -rf /var/lib/apt/lists/*
RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /ros_entrypoint.sh
RUN pip3 install pyspark graphframes argparse
COPY ./ROS2-SMT /ROS2-SMT

