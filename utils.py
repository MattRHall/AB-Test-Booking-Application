import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats
import math
import numpy as np

class AB_test():

    def __init__(self, dataset):
        """ Constructs data visualizer object """

        self.dataset = dataset
 
    def ind_feature_plots(self, variant_control, shape = (4,4), figsize = (8,30), remove = [], save_fig = False):

        columns = [i for i in self.dataset.columns if i not in remove]
        fig, axes = plt.subplots(shape[0], shape[1], figsize = figsize, sharey = False)

        for ind, ax in zip(columns, axes.flatten()):

            if self.dataset[ind].dtype == 'O' or self.dataset[ind].dtype == 'bool':
                temp_df = self.dataset.groupby([ind, variant_control])[variant_control].size().unstack()
                temp_df = temp_df/temp_df.sum(axis = 0)
                temp_df.plot(kind = "bar", ax=ax, grid = True)
                ax.set_title(ind)

            if self.dataset[ind].dtype == 'int64':
                for variant_num in self.dataset["testVariant"].unique():
                    ax.hist(self.dataset[self.dataset[variant_control] == variant_num][ind].dropna())
                ax.set_title(ind)
                ax.legend(self.dataset["testVariant"].unique())
                    
        plt.tight_layout()
        if save_fig:
            plt.savefig("feature_analysis.png")
        plt.show()

    def dep_feature_analysis(self, variant_control, features = []):

        for feature in features:
            statistics = {'mean':[], 'median':[], '25th percentile': [], '75th percentile': []}
            for test in self.dataset[variant_control].unique():
                statistics["mean"].append(self.dataset[self.dataset[variant_control] == test][feature].mean())
                statistics["median"].append(self.dataset[self.dataset[variant_control] == test][feature].median())
                statistics['25th percentile'].append(np.percentile(self.dataset[self.dataset[variant_control] == test][feature], 25))
                statistics['75th percentile'].append(np.percentile(self.dataset[self.dataset[variant_control] == test][feature], 75))
            print(f'Statistics for feature: {feature}: ')
            print(pd.DataFrame(statistics))
            print("<--------------------------------------------------------->")


    def one_tail_binomial_AB_test(self, variant_control, control_num, variant_test):

        sum_df = self.dataset.groupby(variant_control)[variant_test].sum()
        count_df = self.dataset.groupby(variant_control)[variant_test].count()
        prob_df = sum_df/count_df

        z_scores = {}
        p_values = {}

        for i in self.dataset[variant_control].unique():
            if i != control_num:
                numerator = ((prob_df[control_num] * count_df[control_num]) + (prob_df[i] * count_df[i]))
                denominator = (count_df[control_num] + count_df[i])
                p = (numerator)/(denominator)
                z_score = (prob_df[i] - prob_df[control_num])/math.sqrt( p*(1-p)*(1/count_df[control_num] + 1/count_df[i]))
                z_scores[i] = z_score
                p_values[i] = scipy.stats.norm.sf(z_score)

        sorted_temp_df = prob_df.reindex(index=prob_df.index[::-1])

        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,6)) 
        ax1.barh([str(i) for i in sorted_temp_df.index], sorted_temp_df.values*100)
        ax1.set_xlabel('%')
        ax1.set_ylabel('testVariant')
        ax1.set_title('Users Using Search CTA (%)')
#
        for index, value in enumerate(sorted_temp_df.values):
            ax1.text(value*100, index, str(value*100)[0:5])
#
        ax1.set_xlim([0.0, 60])
        ax1.grid()

        ax2.barh([str(i) for i in sorted_temp_df.index],[p_values.get(i,0)*100 for i in sorted_temp_df.index])
        ax2.set_xlabel('%')
        ax2.set_ylabel('testVariant')
        ax2.set_title("Probability No Improvement in Search CTA (%)")

        return z_scores, p_values
