import argparse
import csv
from ros2node.api import get_node_names
from ros2node.api import get_publisher_info
from ros2node.api import get_subscriber_info

from ros2cli.node.strategy import NodeStrategy
from ros2cli.node.strategy import add_arguments

from ros2node.api import get_publisher_info
from ros2node.api import get_subscriber_info
from ros2node.api import get_service_server_info
from ros2node.api import get_service_client_info
from ros2node.api import get_action_client_info
from ros2node.api import get_action_server_info

class SMTNodeRelation:

	def __init__(self,store_path="./"):
		self.store_Path = store_path
		self.vertices = []
		self.edges = []
		self.topicPub = {}
		self.topicSub = {}
		self.serviceSrv = {}
		self.serviceCli = {}
		self.actionSrv ={}
		self.actionCli = {}

	def add_arguments(self, parser):
		add_arguments(parser)
		parser.add_argument(
		'-a', '--all', action='store_true',
		help='Display all nodes even hidden ones')
		parser.add_argument(
		'-c', '--count-nodes', action='store_true',
		help='Only display the number of nodes discovered')
	
	def check_dic_key_exist(self,dic,key):
		if key in dic.keys():
			return True
		else:
			return False

	def add_node_to_dic(self,dic,key,node_name):
		if self.check_dic_key_exist(dic,key):
			temp_list = dic[key]
		else:
			temp_list = []
		temp_list.append(node_name)
		dic[key]=temp_list

	def get_node_info(self, args):
		with NodeStrategy(args) as node:
			node_names = get_node_names(node=node, include_hidden_nodes=True)

			for node_name in node_names:
				full_name = node_name.full_name
				self.vertices.append([full_name,node_name.namespace,node_name.name])

				publishers = get_publisher_info(node=node, remote_node_name=full_name, include_hidden=True)
				for pub in publishers:
					self.add_node_to_dic(self.topicPub,pub.name,full_name)

				subscribers = get_subscriber_info(node=node, remote_node_name=full_name, include_hidden=True)
				for sub in subscribers:
					self.add_node_to_dic(self.topicSub,sub.name,full_name)

				service_servers = get_service_server_info(node=node, remote_node_name=full_name, include_hidden=True)
				for srv in service_servers:
					self.add_node_to_dic(self.serviceSrv,srv.name,full_name)
                
				service_clients = get_service_client_info(node=node, remote_node_name=full_name, include_hidden=True)
				for cli in service_clients:
					self.add_node_to_dic(self.serviceCli,cli.name,full_name)
				
				actions_servers = get_action_server_info(node=node, remote_node_name=full_name, include_hidden=True)
				for asrv in actions_servers:
					self.add_node_to_dic(self.actionSrv,asrv.name,full_name)

				actions_clients = get_action_client_info(node=node, remote_node_name=full_name, include_hidden=True)
				for acli in actions_clients:
					self.add_node_to_dic(self.actionCli,acli.name,full_name)
	
	def build_edges(self,start_dic,end_dic,relation):
		keys = list(set(start_dic.keys()) | set(end_dic.keys()))
		for key in keys:
			try:
				start_nodes = start_dic[key]
			except:
				start_nodes= ["None"]
			try:
				end_nodes = end_dic[key]
			except:
				end_nodes = ["None"]
			for sn in start_nodes:
				for en in end_nodes:
					self.edges.append([sn,en,relation,key])
	
	def csv_writer(self,filename,header,datas):
		with open(filename, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=' ')
			writer.writerow(header)
			for data in datas:
				writer.writerow(data)

		
def main():
    parser = argparse.ArgumentParser()
    smtNodeRelation = SMTNodeRelation()
    smtNodeRelation.add_arguments(parser)
    smtNodeRelation.get_node_info(parser.parse_args())
    smtNodeRelation.build_edges(smtNodeRelation.topicPub,smtNodeRelation.topicSub,"topic")
    smtNodeRelation.build_edges(smtNodeRelation.serviceSrv,smtNodeRelation.serviceCli,"service")
    smtNodeRelation.build_edges(smtNodeRelation.actionSrv,smtNodeRelation.actionCli,"action")
    smtNodeRelation.csv_writer(smtNodeRelation.store_Path+"vertices.csv",["id","name_space","name"],smtNodeRelation.vertices)
    smtNodeRelation.csv_writer(smtNodeRelation.store_Path+"edges.csv",["src","dst","type","type_name"],smtNodeRelation.edges)

if __name__ == "__main__":
	main()



