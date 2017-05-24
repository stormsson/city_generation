#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys


vendor_path = os.path.dirname(os.path.abspath(__file__))+"/vendor"
vendors = [ vendor_path+"/"+f for f in os.listdir(vendor_path) if os.path.isdir(vendor_path+"/"+f)]
for v in vendors:
    sys.path.append(v)


from pcg_wrapper.mapGenerator import RoadMapGenerator

g = RoadMapGenerator()
vertexes = g.generateRoadMap(plotMap=True,plotVertexes=True)
print(len(vertexes))

