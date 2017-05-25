#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

# vendor setup
vendor_path = os.path.dirname(os.path.abspath(__file__))+"/vendor"
vendors = [ vendor_path+"/"+f for f in os.listdir(vendor_path) if os.path.isdir(vendor_path+"/"+f)]
sys.path += vendors

# example
from pcg_wrapper.roadMapGenerator import RoadMapGenerator

# Define the path used by the library
input_path =  os.path.dirname(os.path.abspath(__file__))+"/inputs"
temp_path = os.path.dirname(os.path.abspath(__file__))+"/temp"

# Create the generator instance
g = RoadMapGenerator(input_path, temp_path)

# Define the images to use to generate the map
rule_image_path = input_path+"/rule_pictures/example.png"
density_image_path = input_path+"/density_pictures/stubs_density.png"

# Generate the map , and obtain the vertex list
vertexes = g.generateRoadMap(
    rule_image_path,
    density_image_path,
    seed=False,
    plotMap=True,plotVertexes=False
    )
print("Map contains {0} vertexes".format(len(vertexes)))
print(vertexes[0])
