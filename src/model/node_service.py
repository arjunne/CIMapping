from py2neo import Graph, Node, Relationship
import os
import json
import logging

logger=logging.getLogger()
logger.setLevel(logging.INFO)

get_password = os.environ['password']
get_host = os.environ['host']

#connect to db

def connect_graph():
    global graph
    try:
        graph = Graph(get_host, auth=("neo4j", get_password))
    except Exception as e:
        print(e)

#Parse JSON

def parse_json(file):
    """
    Get the details of the ci
    """
    ci_items = []
    for items in file:
        ci = dict()
        ci['name']=items['ci_name']
        ci['team']=items['ci_details']['team']
        ci['area']=items['ci_details']['area']
        ci_items.append(ci)
    return ci_items


def create_nodes(lst):
    """
    Create nodes
    """
    connect_graph()
    logger.info("Connected to graph")

    try:
        for item in lst:

            # Create name nodes
            name_node = Node("CI_Name",name=item['name'])
            graph.create(name_node)
            print(f"{name_node} has been created")

            #  Create team nodes
            team_node = Node("CI_Team",name=item['team'])
            graph.create(team_node)
            print(f"{team_node} has been created")

            #Create area nodes
            area_node = Node("CI_Area",name=item['area'])
            graph.create(area_node)
            print(f"{area_node} has been created")

            #Create Relationship
            belongs_to = Relationship.type("BELONGS_TO")
            graph.merge(belongs_to(name_node,team_node), "CI_Name", "CI_Team")
            print(f"{belongs_to} relationship has been created")

            manages = Relationship.type("MANAGES")
            graph.merge(manages(name_node,area_node),"CI_Name", "CI_Area")

            # print(item['name'])

    except Exception as e:
        print(e)