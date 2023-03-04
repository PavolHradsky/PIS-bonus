import xml.etree.ElementTree as ET
from typing import List

from Arc import Arc
from Item import Item
from Place import Place
from Role import Role
from Transition import Transition


def get_item_by_name(transitions: List[Transition], places: List[Place], name: str) -> Item:
    """
    This function is finding object of place or transition based on its name (label)
    :param transitions: list of objects transition
    :param places: list of objects place
    :param name: name (label) of place or transition
    :return: founded object
    """
    for item in transitions:
        if item.name == name:
            return item

    for item in places:
        if item.id == name:
            return item


def read_xml(file_name, fuzzy_flag, weights_flag, treshold_flag):
    """
    This function parse xml file to lists of objects: places, transitions and arcs
    :param file_name: name of file
    :return: lists of objects
    """
    """
    script_path = os.path.dirname(os.path.realpath(__file__))

    path_to_file = os.path.join(script_path, 'petri nets', file_name)
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    roles: List[Role] = []
    transitions: List[Transition] = []
    places: List[Place] = []
    arcs: List[Arc] = []

    for transition in root.findall("transition"):
        if weights_flag and not treshold_flag:
            transitions.append(Transition(transition.find("id").text, transition.find("label").text, transition.find("weight").text, None))
        if weights_flag and treshold_flag:
            transitions.append(Transition(transition.find("id").text, transition.find("label").text, transition.find("weight").text, transition.find("treshold").text))
        if not weights_flag and not treshold_flag:
            transitions.append(Transition(transition.find("id").text, transition.find("label").text, None, None))

    for place in root.findall("place"):
        if place.find("label") is None:
            label = place.find("id").text
            places.append(Place(place.find("id").text, float(place.find("tokens").text), label))
        else:
            places.append(Place(place.find("id").text, float(place.find("tokens").text), place.find("label").text))
    for role in root.findall("role"):
        roles.append(Role(role.find("id").text, role.find("title").text))

    for arc in root.findall("arc"):
        if fuzzy_flag and arc.find("sourceId").text[0] == 'p' and arc.find("destinationId").text[0] == 't':
            arcs.append(
                Arc(arc.find("id").text, get_item_by_name(transitions, places, arc.find("sourceId").text),
                    get_item_by_name(transitions, places, arc.find("destinationId").text),
                    round(float(arc.find("multiplicity").text), 2)
                    ))
        else:
            arcs.append(
                Arc(arc.find("id").text, get_item_by_name(transitions, places, arc.find("sourceId").text),
                    get_item_by_name(transitions, places, arc.find("destinationId").text),
                    float(arc.find("multiplicity").text)
                    ))

    return places, transitions, arcs, roles


def list_is_greater(list1, list2):
    is_greater = False
    for i, x in enumerate(list1):
        if x > list2[i]:
            is_greater = True
        if x < list2[i]:
            return False
    return is_greater
