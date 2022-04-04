import xml.etree.ElementTree as ET
from typing import List

from Arc import Arc
from Item import Item
from Place import Place
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
        if item.name == name:
            return item


def read_xml(file_name: str) -> (List[Place], List[Transition], List[Arc]):
    """
    This function parse xml file to lists of objects: places, transitions and arcs
    :param file_name: name of file
    :return: lists of objects
    """
    tree = ET.parse(file_name)
    root = tree.getroot()

    transitions: List[Transition] = []
    places: List[Place] = []
    arcs: List[Arc] = []

    for transition in root.findall("transition"):
        transitions.append(Transition(transition.find("id").text))

    for place in root.findall("place"):
        places.append(Place(place.find("id").text, int(place.find("tokens").text)))

    for arc in root.findall("arc"):
        arcs.append(
            Arc(get_item_by_name(transitions, places, arc.find("sourceId").text),
                get_item_by_name(transitions, places, arc.find("destinationId").text),
                int(arc.find("multiplicity").text)
                ))

    return places, transitions, arcs
