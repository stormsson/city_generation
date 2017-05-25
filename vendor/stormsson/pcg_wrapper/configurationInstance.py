#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import pickle
import os
import random
from collections import namedtuple
import procedural_city_generation

from procedural_city_generation.roadmap.Vertex import Vertex, set_plotbool

from procedural_city_generation.roadmap.config_functions.find_radial_centers import find_radial_centers
from scipy.spatial import cKDTree

from pcg_wrapper.config_functions.input_image_setup import ImageSetup
from pcg_wrapper.singleton import Singleton
from pcg_wrapper.additional_stuff import randommap

class Global_Lists:
    def __init__(self):
        self.vertex_list=[]
        self.vertex_queue=[]
        self.tree=None

class ConfigurationInstance():
    def __init__(self, seed, input_dir_path, temp_dir_path ):

        if(seed):
            random.seed(seed)
            np.random.seed(seed)

        if not os.path.isdir(input_dir_path):
            raise  IOError("Input directory {0} not found".format(input_dir_path))


        if not os.path.isdir(temp_dir_path):
            raise  IOError("Temp directory {0} not found".format(temp_dir_path))

        self.input_dir_path = input_dir_path
        self.temp_dir_path = temp_dir_path

    def getRoadmapSingleton(self, rule_image_path, density_image_path ):
        """
        Starts the program up with all necessary things. Reads the inputs,
        creates the Singleton objects properly, sets up the heightmap for later,
        makes sure all Vertices in the axiom have the correct neighbor. Could
        need a rework in which the Singletons are unified and not broken as they
        are now.

        Returns
        -------
        variables : Variables object
            Singleton with all numeric values which are not to be changed at runtime
        singleton.global_lists : singleton.global_lists object
            Singleton with the Global Lists which will be altered at runtime
        """

        configuration_file_path = self.input_dir_path+"/roadmap.conf"

        if not os.path.isfile(configuration_file_path):
            raise  IOError("Roadmap configuration file {0} not found ".format(configuration_file_path))

        if not os.path.isfile(rule_image_path):
            raise  IOError("Input rule_image_path {0} not found".format(rule_image_path))

        if not os.path.isfile(density_image_path):
            raise  IOError("Input density_image_path {0} not found".format(density_image_path))


        self.singleton=Singleton(configuration_file_path)
        ImageSetupInstance = ImageSetup(self.temp_dir_path)

        #Creates Singleton-Variables object from namedtuple


        #Creates Vertex objects from coordinates
        self.singleton.axiom=[Vertex(np.array([float(x[0]), float(x[1])])) for x in self.singleton.axiom]
        self.singleton.border=np.array([self.singleton.border_x, self.singleton.border_y])
        set_plotbool(self.singleton.plot)

        #Finds the longest possible length of a connection between to vertices
        self.singleton.maxLength=max(self.singleton.radiallMax, self.singleton.gridlMax, self.singleton.organiclMax, self.singleton.minor_roadlMax, self.singleton.seedlMax)

        # self.singleton.img, self.singleton.img2=input_image_setup(self.singleton.rule_image_name, self.singleton.density_image_name)
        self.singleton.img, self.singleton.img2 = ImageSetupInstance.getImages(rule_image_path, density_image_path)

        with open (self.temp_dir_path+"/"+self.singleton.output_name+"_densitymap.txt", 'w') as f:
            imagePath = density_image_path.split(".")[0]+"diffused.png"
            f.write(imagePath)
            # f.write(self.singleton.density_image_name.split(".")[0]+"diffused.png")


        self.singleton.center=find_radial_centers(self.singleton)
        self.singleton.center= [np.array([self.singleton.border[0]*((x[1]/self.singleton.img.shape[1])-0.5)*2, self.singleton.border[1]*(((self.singleton.img.shape[0]-x[0])/self.singleton.img.shape[0])-0.5)*2]) for x in self.singleton.center]


        heightmap_name = "random"
        self.setup_heightmap(heightmap_name)


        self.singleton.global_lists=Global_Lists()
        self.singleton.global_lists.vertex_list.extend(self.singleton.axiom)
        self.singleton.global_lists.coordsliste=[x.coords for x in self.singleton.global_lists.vertex_list]



        for vertex in self.singleton.axiom:
            """ Correctly Sets up the neighbors for a vertex from the axiom.

            Parameters
            ----------
            vertex : vertex Object
            """

            d=np.inf
            neighbour=None
            for v in self.singleton.axiom:
                if v is not vertex:
                    dneu=np.linalg.norm(v.coords-vertex.coords)
                    if dneu<d:
                        d=dneu
                        neighbour=v
            vertex.neighbours=[neighbour]


        self.singleton.global_lists.tree=cKDTree(self.singleton.global_lists.coordsliste, leafsize=160)

        return self.singleton

    def setup_heightmap(self, name):
        #TODO: Document
        '''Sets up the heightmap image from roadmap.conf entry heightmap_name, writes ./Heightmaps/inuse.txt so other functions know which heightmap to load
        possible inputs:
        random: generates a new random map with randommap.py
        insert_name
        insert_name.png
        insert_name.txt
        '''

        #TODO make inputs more flexible
        # name=self.singleton.heightmap_name


        if name == "random":
            #print("New random heightmap is being created with randommap.py")
            #Writes correct inuse.txt

            randommap.main(self.singleton.border, self.temp_dir_path)

            with open(self.temp_dir_path+"/"+self.singleton.output_name+"_heightmap.txt", 'w') as f:
                f.write("randommap_"+str(self.singleton.border[0])+"_"+str(self.singleton.border[1]))
            return 0


        #Writes correct inuse.txt
        with open(self.temp_dir_path+"/"+self.singleton.output_name+"_heightmap.txt", 'w') as f:
            f.write(name[0:-4]+"_"+str(self.singleton.border[0])+"_"+str(self.singleton.border[1]))

        #If a txt has already been written for the input in the image, OR if the input was a .txt to begin with, simply load that txt
        if (name[0:-4]+"_"+str(self.singleton.border[0])+"_"+str(self.singleton.border[1]) in os.listdir(self.temp_dir_path)):
            return 0

        #If the given image has no .txt yet, write the corresponding.txt

        #Load image and resize
        from PIL import Image
        img = Image.open(self.input_dir_path+'/heightmaps/'+name)


        #TODO: set these numbers to some file where they can be edited easier
        rsize = img.resize(((self.singleton.border[1]+20)*10, (self.singleton.border[0]+20)*10))
        array = np.asarray(rsize)
        from copy import copy
        array= np.rot90(copy(array), k=3)


        #If image is a jpeg, all values have to be divided by 255
        array=array[::, :, 0]/255.

        print("You have selected a heightmap which has no .txt file yet, OR the given .txt file has the wrong dimensions. The parameter heightDif will be used to describe the height difference between the lowest and the highest points on the map.")
        h=self.singleton.heightDif
        print("Processing image")


        #TODO: Find and Fix this Bug
        array*=abs(h)
        #Caused weird bugs when -=h was used.. I still can't explain them...
        array-= h+0.01

        #Create all necessary stuff for the heightmap
        from scipy.spatial import Delaunay as delaunay
        indices    =    np.vstack(np.unravel_index(np.arange(array.shape[0]*array.shape[1]), array.shape)).T
        points= np.column_stack((indices, array[indices[:, 0], indices[:, 1]]))


        triangles=np.sort(delaunay(indices).simplices)
        print("Processed image being saved as ", name)

        #TODO: set thse numbers to some file where they can be edited easier
        points*=[0.1, 0.1, 1]
        points-=np.array([ (self.singleton.border[1]+20)/2, (self.singleton.border[0]+20)/2, 0])
        points=points.tolist()


        with open(self.temp_dir_path+"/"+name[0:-4]+"_"+str(self.singleton.border[0])+"_"+str(self.singleton.border[1]), "wb") as f:
            f.write(pickle.dumps([points, triangles.tolist()]))

        return 0