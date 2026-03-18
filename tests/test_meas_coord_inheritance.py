"""
Created on 22 Feb 2023

Test suite validating that the object instances resulting from the annotation parsing 
are compliant with their VODML class definitions

@author: laurentmichel
"""

import os
import unittest
from mivot_validator.utils.session import Session
from mivot_validator.utils.xml_utils import XmlUtils
from mivot_validator.utils.dict_utils import DictUtils

from mivot_validator.instance_checking.instance_checker import (
    InstanceChecker,
    CheckFailedException,
)
from mivot_validator.instance_checking.xml_interpreter.exceptions import (
    MappingException,
)

mapping_sample = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
vodml_sample = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../mivot_validator/",
    "instance_checking/",
    "vodml/",
)


class TestMeasCoordsInheritance(unittest.TestCase):
    
    def testInheritenceGraph(self):
        self.maxDiff = None
        vodml_filepath = os.path.join(vodml_sample, "Meas-v1.vo-dml.xml")
        InstanceChecker.reset()
        InstanceChecker._build_inheritence_graph(vodml_filepath)
        self.assertDictEqual(
            InstanceChecker.inheritence_tree,
            DictUtils.read_dict_from_file(
                os.path.join(mapping_sample, "instcheck_inherit_meas.json")
            ),
        )
        InstanceChecker.inheritence_tree = {}
        vodml_filepath = os.path.join(vodml_sample, "Coords-v1.0.vo-dml.xml")
        InstanceChecker._build_inheritence_graph(vodml_filepath)
        DictUtils.print_pretty_json(InstanceChecker.inheritence_tree)
        self.assertDictEqual(
            InstanceChecker.inheritence_tree,
            DictUtils.read_dict_from_file(
                os.path.join(mapping_sample, "instcheck_inherit_coords.json")
            ),
        )

if __name__ == "__main__":
    unittest.main()
