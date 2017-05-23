#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
parentpath = os.path.dirname(os.path.abspath(__file__))+"/../"
sys.path.append(parentpath)

from mapGenerator import RoadMapGenerator

g = RoadMapGenerator()
vertexes = g.generateRoadMap(plotMap=False)
print(len(vertexes))

