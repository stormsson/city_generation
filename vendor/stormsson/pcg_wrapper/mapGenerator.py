#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from copy import copy
import matplotlib.pyplot as plt

from pcg_wrapper.configurationInstance import ConfigurationInstance
from procedural_city_generation.roadmap.getSuggestion import getSuggestion
from procedural_city_generation.roadmap.check import check
from procedural_city_generation.additional_stuff.pickletools import save_vertexlist

gui=None

class RoadMapGenerator():
    def __init__(self, input_dir_path, temp_dir_path):
        self.input_dir_path = input_dir_path
        self.temp_dir_path = temp_dir_path

    def generateRoadMap(self, rule_image_path, density_image_path, seed=False, plotMap=False, plotVertexes=False):
        configurationInstance = ConfigurationInstance(seed, self.input_dir_path, self.temp_dir_path)
        self.singleton = configurationInstance.getRoadmapSingleton(rule_image_path, density_image_path)

        front=copy(self.singleton.global_lists.vertex_list)
        front.pop(0)
        front.pop()
        vertex_queue = copy(self.singleton.global_lists.vertex_queue)

        self.singleton.iterationszaehler=0


        if plotMap:
            plt.close()
            fig=plt.figure()
            ax=plt.subplot(111)

            fig.canvas.draw()
            ax.set_xlim((-self.singleton.border[0], self.singleton.border[0]))
            ax.set_ylim((-self.singleton.border[1], self.singleton.border[1]))

        i=0
        while (front!=[] or self.singleton.global_lists.vertex_queue    !=[]):
            i+=1
            front=self.iteration(front)

            if plotMap == 1:
                if i%self.singleton.plot_counter == 0:
                        # plt.pause(0.001)
                        try:
                            fig.canvas.blit(ax.bbox)
                            fig.canvas.flush_events()
                        except:
                            fig.canvas.draw()

                self.singleton.iterationszaehler=0

        vertexes = [];
        for v in self.singleton.global_lists.vertex_list:
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
        # print("Roadmap is complete!")

        if plotMap:
            plt.show()

        return vertexes

    def iteration(self, front):
        """
        Gets Called in the mainloop.
        Manages the front and newfront and the queue

        Parameters
        ----------
        front : list<Vertex>

        Returns
        -------
        newfront : list<Vertex>

        """
        newfront=[]

        for vertex in front:
            for suggested_vertex in getSuggestion(vertex):
                newfront=check(suggested_vertex, vertex, newfront)

        #Increments index of each element in queue
        self.singleton.global_lists.vertex_queue=[[x[0], x[1]+1] for x in self.singleton.global_lists.vertex_queue]

        #Finds elements in queue which are to be added into the newfront
        while self.singleton.global_lists.vertex_queue!=[] and self.singleton.global_lists.vertex_queue[0][1]>=self.singleton.minor_road_delay:
            newfront.append(self.singleton.global_lists.vertex_queue.pop(0)[0])

        return newfront