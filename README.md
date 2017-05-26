## Introduction

This project is a wrapper for procedural_city_generation sources from https://github.com/josauder/procedural_city_generation.

The core of this code so is made by its original author and the documentation can be found [here](http://josauder.github.io/procedural_city_generation).

The aim of this project is to provide a quick and simple way to create map instances to use for other purposes than visualization.

To make it easier to refactor and create the wrapper **the original sources included in this project may have been modified**.

## Content

### inputs, outputs,temp directories
The main library relies on certain folders to be present to read data.
In a first step to detach the file structure from the logical structure these folder are moved (copied, actually) from the original library file structure, to a more accessible folder.

In the future, if the project proceeds, the objective is to render the directory structure not mandatory.


### vendor/josauder
Inside vendor/josauder directory there is the main library that actually generate the city, but some of the sources have been altered.

### vendor/stormsson/pcg_wrapper
When possible or necessary the original code has been mantained untouched and an equivalent code has been created inside vendor/stormsson/pcg_wrapper.


## Installation
Just install requirements:

    pip install -r requirements.txt

## Quickstart
Simply check exampleRoadmapGeneration.py: the steps are quite simple

1) include vendor dir to sys.path


        vendor_path = os.path.dirname(os.path.abspath(__file__))+"/vendor"
        vendors = [ vendor_path+"/"+f for f in os.listdir(vendor_path) if os.path.isdir(vendor_path+"/"+f)]
        sys.path += vendors


2) import the roadmap generator

        from pcg_wrapper.roadMapGenerator import RoadMapGenerator

3) the generator instance needs 2 folder path: input and temp dir to make the original library work correctly (hopefully this will be removed in the future).

        g = RoadMapGenerator(input_path, temp_path)

4) to generate the map the generator needs the path to a rgb image that defines the rules on how to grow the city and the path a b/w image that defines the population density.

See [here](http://josauder.github.io/procedural_city_generation) for further informations.

Furthermore you can pass an integer **seed** parameter to generate the same map.

    vertexes = g.generateRoadMap(
        rule_image_path,
        density_image_path,
        seed=False,
        plotMap=True,plotVertexes=False
        )

The generator returns a list of vertexes (see next section)

## Vertex dictionary
The vertex is simply a dictionary that replicates the original Vertex object, with the following keys:

    'coords': list of x,y coordinate of the vertex (ex: [ 1. , 0.3 ] )
    'neighbours': list of x,y coordinates for neighbours ( ex:  [ [1. , 0.3 ], [ 2. , 0.1 ], ... ])
    'minor_road': bool to check if the vertex belongs to a minor road or not
