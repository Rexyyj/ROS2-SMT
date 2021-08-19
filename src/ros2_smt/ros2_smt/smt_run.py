from smt_node.smt_node import SMT_NODE
from smt_relationship.smt_relationship import SMT_RELATIONSHIP
from smt_artifact.smt_artifact import SMT_ARTIFACT
import argparse
import time


class SMT_RUN():

    def __init__(self) -> None:
        self.smt_node = None
        self.smt_relationship = None
        self.smt_artifact = None
        self.group_policy = None

    def scan_nodes(self):
        counter = 0
        parser = argparse.ArgumentParser()
        smtNodeRelation = SMT_NODE()
        smtNodeRelation.add_arguments(parser)
        try:
            print("Starting scanning system, use Ctrl+C to stop scanning",end="")
            while True:
                counter = counter+1
                smtNodeRelation.get_node_info(parser.parse_args())
                time.sleep(0.1)
                if counter % 10 == 0:
                    print(".",end="")
        except KeyboardInterrupt:
            pass
        print("Rebuilding system relationship...")
        smtNodeRelation.build_all_edges()
        save = input("Save obtained information to file? [y/n]")
        if save == 'n':
            pass
        else:
            smtNodeRelation.save_all()
        self.smt_node=smtNodeRelation


def main():
    print("Please select the service:")
    print("\t1: Scan ROS2 nodes.")
    print("\t2: Analysis ROS2 node relationship with pyspark")
    print("\t3: Create ROS2 security artifacts")
    print("Note: You can enter '123' to use a serials of service")
    print("Selection(default 123): ", end='')
    services = input()
    run = SMT_RUN()
    for service in list(services):
        if service == '1':
            print("Starting scanning system, use Ctrl+C to stop scanning")
            run.scan_nodes()

        elif service == '2':
            if run.smt_node is not None:
                run.smt_relationship = SMT_RELATIONSHIP(from_file=False,
                    vertices=run.smt_node.get_vertices(), edges=run.smt_node.get_edges())
            else:
                run.smt_relationship=SMT_RELATIONSHIP(from_file=True)
            config={"remove_hidden":"True","remove_default":"True","grouping_method":"RBAC","mode":"namespace"}
            run.group_policy=run.smt_relationship.analysis(config)
            
        elif service == '3':
            if run.smt_relationship==None:
                raise ValueError
            run.smt_artifact =  SMT_ARTIFACT(group_policies=run.group_policy)
            run.smt_artifact.main()
        else:
            pass


if __name__ == '__main__':
    main()
