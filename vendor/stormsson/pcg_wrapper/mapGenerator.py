#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from copy import copy
import matplotlib.pyplot as plt

from procedural_city_generation.roadmap.config import config
from procedural_city_generation.roadmap.iteration import iteration
from procedural_city_generation.additional_stuff.pickletools import save_vertexlist


gui=None

class RoadMapGenerator():

    def generateRoadMap(self, plotMap=False, plotVertexes=False):

        singleton=config()

        front=copy(singleton.global_lists.vertex_list)
        front.pop(0)
        front.pop()
        vertex_queue = copy(singleton.global_lists.vertex_queue)

        singleton.iterationszaehler=0


        if plotMap:
            plt.close()
            fig=plt.figure()
            ax=plt.subplot(111)

            fig.canvas.draw()
            ax.set_xlim((-singleton.border[0], singleton.border[0]))
            ax.set_ylim((-singleton.border[1], singleton.border[1]))

        i=0
        while (front!=[] or singleton.global_lists.vertex_queue    !=[]):
            i+=1
            front=iteration(front)

            if plotMap == 1:
                if i%singleton.plot_counter == 0:
                        plt.pause(0.001)
                        try:
                            fig.canvas.blit(ax.bbox)
                            fig.canvas.flush_events()
                        except:
                            fig.canvas.draw()

                singleton.iterationszaehler=0

        vertexes = [];
        for v in singleton.global_lists.vertex_list:
            neighbours =  [ n.coords for n in v.neighbours ]
            vertexes.append({
                'coords': v.coords,
                'neighbours': neighbours,
                'minor_road': v.minor_road
                })


        if plotVertexes:
            plt.plot(
                [v['coords'][0] for v in vertexes],
                [v['coords'][1] for v in vertexes],
                'o', color="red")
        print("Roadmap is complete!")

        if plotMap:
            plt.show()

        return vertexes