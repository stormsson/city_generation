#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys


vendor_path = os.path.dirname(os.path.abspath(__file__))+"/vendor"
input_path =  os.path.dirname(os.path.abspath(__file__))+"/inputs"
temp_path = os.path.dirname(os.path.abspath(__file__))+"/temp"

vendors = [ vendor_path+"/"+f for f in os.listdir(vendor_path) if os.path.isdir(vendor_path+"/"+f)]
for v in vendors:
    sys.path.append(v)


from pcg_wrapper.mapGenerator import RoadMapGenerator

g = RoadMapGenerator(input_path, temp_path)
rule_image_path = input_path+"/rule_pictures/example.png"
density_image_path = input_path+"/density_pictures/stubs_density.png"

vertexes = g.generateRoadMap(
    rule_image_path,
    density_image_path,
    plotMap=True,plotVertexes=True
    )
print(len(vertexes))

