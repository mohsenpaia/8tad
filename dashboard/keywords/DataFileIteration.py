#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
##########################################################


##########################################################
# Data File Iteration
# Mohammad Mahdavi
# moh.mahdavi.l@gmail.com
# November 2016
# Homaplus Corporation
# homaplus.com
# All Rights Reserved
# Do not Change, Alter, or Remove this Licence
##########################################################


##########################################################
import os
import codecs
import ParameterConfiguration as PC
##########################################################


##########################################################
class DataFileIteration:
    """
    This class implements an iterator for data files.
    """

    def __init__(self, root_path, file_type="json"):
        """
        This constructor creates variables.
        """
        self.progress_dictionary = {0.1: "10%", 0.2: "20%", 0.3: "30%", 0.4: "40%", 0.5: "50%", 0.6: "60%", 0.7: "70%",
                                    0.8: "80%", 0.9: "90%", 1.0: "100%"}
        self.data_file_path_list = []

        def dfs(path):
            item_list = os.listdir(path)
            for item in item_list:
                if os.path.isfile(os.path.join(path, item)) and (not file_type or item.lower().endswith("." + file_type.lower())):
                    self.data_file_path_list.append(os.path.join(path, item).decode("utf-8"))
                elif os.path.isdir(os.path.join(path, item)):
                    dfs(os.path.join(path, item))

        dfs(root_path)
        self.index = 0
        self.size = len(self.data_file_path_list)

    def getNextData(self):
        """
        This method returns the next data file information.
        """
        if self.index >= self.size:
            return False
        data_dictionary = {}
        data_dictionary["path"] = self.data_file_path_list[self.index]
        data_dictionary["string"] = codecs.open(data_dictionary["path"], "r", encoding="utf-8").read()
        data_dictionary["folder"] = data_dictionary["path"].split(os.sep)[-2]
        data_dictionary["file"] = data_dictionary["path"].split(os.sep)[-1].split(".")[0]
        self.index += 1
        progress = float(self.index) / max((100 * (self.size / 100)), 100)
        if progress in self.progress_dictionary:
            print "Progress: {}".format(self.progress_dictionary[progress])
        return data_dictionary
##########################################################


##########################################################
def main():
    data_file_iteration = DataFileIteration(PC.FORMAL_CORPUS_DATA_FOLDER, "json")
    # data = data_file_iteration.getNextData()
    # while data:
    #     print data
    #     data = data_file_iteration.getNextData()
##########################################################


##########################################################
if __name__ == "__main__":
    main()
##########################################################
