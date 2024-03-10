import json
import os.path


class OntologyManager:

    def __init__(self, ontology_group, ontology_format):
        self.__ontology_format = ontology_format
        self.__ontology_group = ontology_group

    def read_ontologies(self):
        with open(os.path.join("ontologies", self.__ontology_format, f"{self.__ontology_group}.{self.__ontology_format}"), 'r') as json_file:
            ontologies_list = json.load(json_file)

        return ontologies_list

    def read_ontology(self, ontology_name):
        with open(os.path.join("ontologies", self.__ontology_format, f"{self.__ontology_group}.{self.__ontology_format}"), 'r') as json_file:
            ontologies_list = json.load(json_file)

        if ontology_name in ontologies_list:
            return ontologies_list[ontology_name]

        return None

    def get_ontologies_items_details(self, ontologies):
        ontologies_attr = {}

        for ontology_name, ontology_items in ontologies.items():
            for item_name, item_details in ontology_items.items():

                type = item_details["type"]
                importance = item_details["importance"]

                if item_name not in ontologies_attr:
                    ontologies_attr[item_name] = {
                        "importance": 0, "ontologyName": ontology_name
                    }

                ontologies_attr[item_name]["type"] = type
                if ontologies_attr[item_name]["importance"] == 0:
                    ontologies_attr[item_name]["importance"] = importance
                else:
                    ontologies_attr[item_name]["importance"] += importance
                    ontologies_attr[item_name]["importance"] /= 2

        return ontologies_attr
