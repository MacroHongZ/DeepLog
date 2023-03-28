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
        print("=" * 25)
        for key, value in parameters.items():
            print(key, ": ", value)
        print("=" * 25)

    def save(self, file):
        pickle.dump(self, file)

    def from_argparse(self, args):
        parameters = args.__dict__
        self.__dict__.update(parameters)


class DeepLog():

    def __init__(self, save_path="output_file"):
        self.path = save_path + "/log"
        self.logs = collections.defaultdict(list)

    def log(self, name, value):

        self.logs[name].append(value)

    def get_log_keys(self):

        return self.logs.keys()

    def save(self, config=None, config_save=False):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        mytime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

        log_file_name = mytime + 'log.txt'
        file_path = self.path + "/" + log_file_name

        with open(file_path, "w+") as fp:
            if config != None:
                hyperparameters = config.get_parameters()
                for key, value in hyperparameters.items():
                    fp.write(key + ": " + str(value))
                    fp.write("\n")

            for key, value in self.logs.items():
                fp.write("=" * 50)
                fp.write("\n")
                fp.write(key)
                fp.write("\n")
                fp.write(str(value)[1:-1])
                fp.write("\n")

        if config_save:
            config_file_path = self.path + "/" + mytime + 'config.pickle'
            with open(config_file_path, "wb") as fp:
                config.save(fp)

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

        for i in range(int(len(lines) / 3)):
            # value = lines[3 * i + 2].split(", ")
            value = lines[3 * i + 2]
            if value[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                continue
            else:
                value = value.split(", ")
                value = [eval(v) for v in value]
                logs[lines[3 * i + 1]].extend(value)

        self.logs = logs

    def _draw(self, key):
        if key not in self.logs:
            raise ValueError("key not exist")
        matplotlib.rcParams['font.family'] = 'serif'
        plt.style.use('ggplot')

        fig = plt.figure(dpi=200)
        ax = fig.subplots()
        line1 = ax.plot(self.logs[key])

        ax.set_ylabel(key)
        plt.setp(line1, c='#72aa9d')
        ax.tick_params(axis='y', which='both', direction='in', right=False)
        ax.tick_params(axis='x', which='both', bottom="in", top=False)

        plt.show()

    def visualization(self, item):
        if item == "all":
            for key in self.logs.keys():
                self._draw(key)
        else:
            self._draw(item)

    def save_list(self, file_name):
        '''
        Only one key is in self.logs
        '''

        file_path = self.path + "/" + file_name

        li = list(self.logs.values())
        li = li[0]
        with open(file_path, "w+") as fp:
            for line in li:
                if isinstance(line, list) or isinstance(line, dict):
                    fp.write(str(line)[1:-1])
                    fp.write("\n")
                else:
                    fp.write(str(line))
                    fp.write("\n")
