import numpy as np
import matplotlib.pyplot as plt
import os
import sys


class StaveSurvey:

    def __init__(self, virtual_file, survey_file):
        # first reading in data
        self.virtual_data = np.genfromtxt(virtual_file, dtype=float, delimiter=',', comments='#')[:, :2].copy()
        self.survey_data = np.genfromtxt(survey_file, dtype=float, delimiter=',', comments='#')[:, :2].copy()

        # finding the relative data
        self.relative_data = self.virtual_data - self.survey_data

        # separating data out to sort by modules
        self.separate_module = np.split(self.relative_data, self.relative_data.shape[0] // 4)

        # reading the first line of the survey_data if there is a fidcucial mark
        with open(survey_file) as f:
            first_line = f.readline()

        # set the fiducial found in the survey file, otherwise set it as unknown
        if 'fid' in first_line.lower():
            self.fiducial_mark = first_line.split('=')[1].strip()
        else:
            self.fiducial_mark = 'unknown'

    def plot_histogram(self, save_folder):
        dim = ['X', 'Y']
        bins = np.arange(-30, 35, 7.5)

        # create separate histograms for the x and y
        for i in range(2):
            fig = plt.figure("Histogram - " + dim[i], (10, 10))
            ax = fig.add_subplot(111)

            plt.hist(self.relative_data[:, i], bins=bins)
            plt.xlabel('$\Delta$' + dim[i] + ' [$\mu$m]', fontsize=18)
            plt.ylabel('Counts / ' + str(round(abs(bins[0] - bins[1]), 2)) + ' $\mu$m', fontsize=18)
            plt.xticks(np.arange(-50, 55, 10))
            plt.title('Relative difference for {}'.format(dim[i]))
            plt.xlim(-52.5, 52.5)

            ax.annotate('$\mu$ = ' + str(round(self.relative_data[:, i].mean(), 2)) + ' $\mu$m', xy=(0.995, 0.965),
                        xycoords='axes fraction', fontsize=16, horizontalalignment='right', verticalalignment='bottom')
            ax.annotate('$\sigma$ = ' + str(round(self.relative_data[:, i].std(), 2)) + ' $\mu$m', xy=(0.995, 0.925),
                        xycoords='axes fraction', fontsize=16, horizontalalignment='right', verticalalignment='bottom')

            # now save the pdfs into the specified folder
            if not os.path.isdir(save_folder):
                os.makedirs(save_folder)
            plt.savefig(save_folder + '\\' + dim[i] + '-Corners' + 'ABCD' + '-histogram' + '.png')
            plt.close()

    def find_if_passing(self, tolerance=0.1):
        """
        Determines if all corners are passing for both dx and dy separately

        ~~True value means that the module in a dimension (X or Y) passed~~

        :param tolerance: float determining passing tolerance in unit mm
            If a relative value falls below this, it is considered passing
        :return:
            -> list of numpy arrays in the order of the modules are placed in
                - numpy arrays has a format of array[x-passed, y-passed] with type bool
            -> numpy array of total failed: array[x-failed-total, y-failed-total] with type int
        """
        passed_modules = []

        for module in self.separate_module:
            passed_modules.append(np.less(np.absolute(module), tolerance).all(axis=0))
            # so if any dx or dy fails, (i.e. a False shows up for the module in a column),
            # the respective column is False for the module

        return passed_modules, (len(passed_modules)-sum(passed_modules))

    def separate_corners(self):
        """
        Separates each module into a list containing dictionaries of relative corner data

        :return: A list of dictionaries in the order of the modules are placed in
        dictionary keys: 'A', 'B', 'C', 'D', for each corner
        dictionary items: list of relative differences for the module corner -> [dx, dy] with type float in unit um
        """
        corners = list(enumerate('ABCD'))
        modules_nums = []

        for m in self.separate_module:
            diffs = {}
            for n_corner, corner in corners:
                diffs[corner] = np.round(m[n_corner, :]*1000, decimals=1)
            modules_nums.append(diffs)

        return modules_nums


if __name__ == '__main__':
    assert len(sys.argv) == 4, "Arguments must be in format: ideal csv, survey csv, figure path"
    ss = StaveSurvey(sys.argv[1], sys.argv[2])
    ss.plot_histogram(sys.argv[3])

#    print(ss.separate_module)
    """
    passed_modules, total_failed = ss.find_if_passing(tolerance=0.025)
#    print(passed_modules)
#    print(total_failed)

    modules = ss.separate_corners()
    for i in modules:
        print(i)
    """
