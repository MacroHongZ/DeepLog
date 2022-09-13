# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:33:18 2022

@author: H
"""
import collections
import os
import pickle
import time
import matplotlib.pyplot as plt
import matplotlib


class Config():

    def __init__(self):
        pass

    def get_parameters(self):
        return self.__dict__

    def print_parameters(self):
        parameters = self.get_parameters()
        for key, value in parameters.items():
            print(key, ": ", value)

    def save(self, file):
        pickle.dump(self, file)


class DeepLog():

    def __init__(self, project_name="MyProject"):

        self.project_name = project_name
        self.path = self.project_name + "_log"
        self.logs = collections.defaultdict(list)

    def log(self, name, value):

        self.logs[name].append(value)

    def get_log_keys(self):

        return self.logs.keys()

    @staticmethod
    def transDD(defaultdict):
        dic = {}
        for i, j in defaultdict.items():
            dic[i] = j

        return dic

    def save(self, config=None, config_save=False, type="txt"):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        mytime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

        if type == "txt":
            log_file_name = mytime + 'log.txt'
            file_path = self.path + "/" + log_file_name

            with open(file_path, "w+") as fp:
                if config != None:
                    hyperparameters = config.get_parameters()
                    for key, value in hyperparameters.items():
                        fp.write(key + ": " + str(value))
                        fp.write("\n")
                    fp.write("=" * 50)
                    fp.write("\n")

                for key, value in self.logs.items():
                    fp.write(key)
                    fp.write("\n")
                    fp.write(str(value)[1:-1])
                    fp.write("\n")

            if config_save:
                config_file_path = self.path + "/" + mytime + 'config.pickle'
                with open(config_file_path, "wb") as fp:
                    config.save(fp)
        else:
            log_file_name = mytime + 'log.pickle'
            file_path = self.path + "/" + log_file_name

            with open(file_path, "wb") as fp:
                pickle.dump(self.transDD(self.logs), fp)

    def load_config(self, file_name):

        config_file_path = self.path + "/" + file_name
        with open(config_file_path, "rb") as fp:
            config = pickle.load(fp)
        return config

    def load_logs(self, file_path):

        logs = collections.defaultdict(list)
        lines = []
        begin = False
        with open(file_path, "r") as fp:
            for line in fp:
                if line[0] == "=":
                    begin = True
                if begin:
                    lines.append(line.strip())
        lines = lines[1:]
        for i in range(int(len(lines)/2)):
            value = lines[2*i+1].split(", ")
            value = [eval(v) for v in value]
            logs[lines[2*i]].extend(value)

        self.logs = logs

    def draw(self, key):
        if key not in self.logs:
            raise ValueError("key not exist")
        matplotlib.rcParams['font.family'] = 'serif'
        plt.style.use('ggplot')

        fig = plt.figure(dpi=100)
        ax = fig.subplots()
        line1 = ax.plot(self.logs[key])

        ax.set_ylabel(key)
        plt.setp(line1, c='#72aa9d')
        ax.tick_params(axis='y', which='both', direction='in', right=False)
        ax.tick_params(axis='x', which='both', bottom="in", top=False)

        plt.show()

    def visualization(self, item="all"):

        if item == "all":
            for key in self.logs.keys():
                self.draw(key)
        else:
            self.draw(item)
