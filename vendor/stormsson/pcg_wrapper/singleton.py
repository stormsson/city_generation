#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

class Singleton:
    """
    Singleton Object which can only have one instance.
    Is instanciated with a modulename, e.g. "roadmap", and reads the
    corresponding "roadmap.conf" in procedural_city_generation/inputs.
    All attributes are mutable, however this class should mainly be used for
    immutable numeric values to avoid confusion/difficult-to-trace-bugs.
    """

    class __Singleton:
        def __init__(self, configurationFilePath=None):
            with open(configurationFilePath, 'r') as f:
                d=json.loads(f.read())
            for k, v in d.items():
                setattr(self, k, v["value"])
    instance=None
    def __init__(self, configurationFilePath=None):

        # it is hardcoded here, because everywhere in the original library
        # the file is read by just the name, and the full path is related to the original singleton.py
        # position
        # this allows to use the wrapper by passing the full path, and hijack the original singleton
        # by prepending the input folder path, if the name does not contain at least a directory separator character

        default_input_folder_path = os.path.dirname(os.path.abspath(__file__))+"/../../../inputs/"

        if "/" not in configurationFilePath:
            configurationFilePath = default_input_folder_path +  configurationFilePath + ".conf"

        if not Singleton.instance:
            Singleton.instance=Singleton.__Singleton(configurationFilePath)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        setattr(self.instance, name, value)

    def kill(self):
        """
        Deletes the Singleton's instance
        """
        Singleton.instance = None
