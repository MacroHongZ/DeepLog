import collections
import os
import pickle
import time
import matplotlib.pyplot as plt
import matplotlib


class Config:
    def get_parameters(self):
        return self.__dict__

    def print_parameters(self):
        parameters = self.get_parameters()
        print("=" * 25)
        for key, value in parameters.items():
            print(key, ": ", value)
        print("=" * 25)

    def from_argparse(self, args):
        parameters = args.__dict__
        self.__dict__.update(parameters)

    def from_dict(self, d):
        self.__dict__.update(d)

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError("Can't modify attribute")
        else:
            self.__dict__[key] = value


class DeepLog:
    def __init__(self, save_path="output_files"):
        self.path = save_path + "/log/"
        self.log_file_name = (
                time.strftime("%Y%m%d_%H-%M-%S", time.localtime()) + "log.txt"
        )
        self.logs = collections.defaultdict(list)

    def log(self, name, value):
        if isinstance(value, list):
            self.logs[name].extend(value)
        else:
            self.logs[name].append(value)

    def get_keys(self):
        return self.logs.keys()

    def save(self, config=None):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        file_path = self.path + self.log_file_name
        pickle_file_path = file_path[:-4] + ".pickle"
        with open(pickle_file_path, "wb") as fp:
            pickle.dump(self.logs, fp)

        with open(file_path, "w+") as fp:
            if config is not None:
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

    def load(self, file_path):
        with open(file_path, "rb") as fp:
            self.logs = pickle.load(fp)

    def visualization(self, key, save_fig=False):
        if key not in self.logs:
            raise ValueError("key not exist")
        matplotlib.rcParams["font.family"] = "serif"
        plt.style.use("ggplot")

        fig = plt.figure(dpi=200)
        ax = fig.subplots()
        line1 = ax.plot(self.logs[key])

        ax.set_ylabel(key)
        plt.setp(line1, c="#72aa9d")
        ax.tick_params(axis="y", which="both", direction="in", right=False)
        ax.tick_params(axis="x", which="both", bottom="in", top=False)

        if save_fig:
            current_time = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
            fig_name = key + current_time + ".png"
            plt.savefig(self.path + fig_name)
        else:
            plt.show()
