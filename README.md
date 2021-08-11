# ROS2-SMT
ROS2 Security Management Tool (ROS2-SMT) aims at making easier the configuration to enable ROS2 security in complex ROS2 system. The main functions it provides include automatically detect and record the existing nodes in the system, automatically analysis node relationship and automatically generate corresponding security artifacts. In addition, it will provide the function to monitor the secure ROS2 system and perform the performance analysis(Under developing).

# Design
![Design](./figures/design.png)
In the design of ROS2-SMT, it will be able to perform the following functions:
1. This tool will obtain the existing communication relationship from the environment when the communication is not secured.(Node, Topic, Service, Relationship)
2. This tool will save the obtained information and possible to visualize, update and optimize the relationship in future analysis.
3. This tool will analysis the relationship of the communicating entities and group them to different groups according to the security level setting.
4. This tool will create security artifacts for each group and generate a document indicating corresponding artifact to each node.
5. This tool will modify the launch file of nodes according to the document in 4.
6. This tool will be able to obtain information from the security system once it have necessary information of the security system (CA certificates)
7. This tool will be able to analysis the performance change before and after enabling security in communication.