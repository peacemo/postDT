import random
import numpy as np
import pandas as pd
import copy
import time
import pandas as pd
from sklearn import preprocessing #通常使用sklearn中的preproccessing库来进行数据预处理。
import matplotlib.pyplot as plt

X_border = np.array([[291, 258, 258, 313], [219, 230, 230, 209]])
y_border = np.array([42184, 15967])

def plot_loss(loss):
    plt.title("The mse curve of GA training phase.")
    plt.plot(loss, label='MSE Loss')
    plt.legend(loc='upper right')
    plt.savefig('loss.png')
    plt.show()

class Network(object):

    def __init__(self, sizes):

        '''构建神经网络结构（全连接）'''

        self.num_layers = len(sizes) # 层数
        self.sizes = sizes # [4, 6, 3]
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

        # 辅助变量
        self.bias_nitem = sum(sizes[1:])
        self.weight_nitem = sum([self.weights[i].size for i in range(self.num_layers - 2)])

    def feedforward(self, a):
        '''Return the output of the network if ``a`` is input.'''
        for b, w in zip(self.biases, self.weights):
            a = self.sigmoid(np.dot(w, a) + b)
        return a

    def sigmoid(self, z):
        '''The sigmoid function.'''
        return 1.0 / (1.0 + np.exp(-z))

    def score(self, X, y):

        '''
        @X = data to test
        @y = data-label to test
        @returns = score of network prediction (less is better)
        '''

        total_score = 0
        for i in range(X.shape[0]):
            predicted = self.feedforward(X[i].reshape(-1, 1))
            actual = y[i].reshape(-1, 1)
            total_score += np.sum(np.power(predicted - actual, 2) / 2)  # mean-squared error
        return total_score

    def accuracy(self, X, y):

        '''
        @X = data to test
        @y = data-label to test
        @returns = accuracy (%) (more is better)
        '''

        accuracy = 0
        for i in range(X.shape[0]):
            output = self.feedforward(X[i].reshape(-1, 1))
            accuracy += int(np.argmax(output) == np.argmax(y[i]))
        return accuracy / X.shape[0] * 100

    def __str__(self):
        s = "\nBias:\n\n" + str(self.biases)
        s += "\nWeights:\n\n" + str(self.weights)
        s += "\n\n"
        return s


class NNGeneticAlgo:

    def __init__(self, n_pops, net_size, mutation_rate, crossover_rate, retain_rate, X, y):

        self.n_pops = n_pops
        self.net_size = net_size
        self.nets = [Network(self.net_size) for i in range(self.n_pops)]
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.retain_rate = retain_rate
        self.X = X[:]
        self.y = y[:]

    def get_random_point(self, type):

        nn = self.nets[0]
        layer_index, point_index = random.randint(0, nn.num_layers - 2), 0
        if type == 'weight':
            row = random.randint(0, nn.weights[layer_index].shape[0] - 1)
            col = random.randint(0, nn.weights[layer_index].shape[1] - 1)
            point_index = (row, col)
        elif type == 'bias':
            point_index = random.randint(0, nn.biases[layer_index].size - 1)
        return (layer_index, point_index)

    def get_all_scores(self):
        return [net.score(self.X, self.y) for net in self.nets]

    def get_all_accuracy(self):
        return [net.accuracy(self.X, self.y) for net in self.nets]

    def crossover(self, father, mother):

        # make a copy of father 'genetic' weights & biases information
        nn = copy.deepcopy(father)

        # cross-over bias
        for _ in range(self.nets[0].bias_nitem):
            # get some random points
            layer, point = self.get_random_point('bias')
            # replace genetic (bias) with mother's value
            if random.uniform(0, 1) < self.crossover_rate:
                nn.biases[layer][point] = mother.biases[layer][point]

        # cross-over weight
        for _ in range(self.nets[0].weight_nitem):
            # get some random points
            layer, point = self.get_random_point('weight')
            # replace genetic (weight) with mother's value
            if random.uniform(0, 1) < self.crossover_rate:
                nn.weights[layer][point] = mother.weights[layer][point]

        return nn

    def mutation(self, child):

        '''
        @child_index = neural-net object to mutate its internal weights & biases value
        @returns = new mutated neural-net
        '''

        nn = copy.deepcopy(child)

        # mutate bias
        for _ in range(self.nets[0].bias_nitem):
            # get some random points
            layer, point = self.get_random_point('bias')
            # add some random value between -0.5 and 0.5
            if random.uniform(0, 1) < self.mutation_rate:
                nn.biases[layer][point] += random.uniform(-0.5, 0.5)

        # mutate weight
        for _ in range(self.nets[0].weight_nitem):
            # get some random points
            layer, point = self.get_random_point('weight')
            # add some random value between -0.5 and 0.5
            if random.uniform(0, 1) < self.mutation_rate:
                nn.weights[layer][point[0], point[1]] += random.uniform(-0.5, 0.5)

        return nn

    def evolve(self):

        # calculate score for each population of neural-net
        self.score_list_ = list(zip(self.nets, self.get_all_scores()))

        # sort the network using its score
        self.score_list_.sort(key=lambda x: x[1])

        # exclude score as it is not needed anymore
        self.score_list = [obj[0] for obj in self.score_list_]
        # print(score_list[0].weights)
        # print(score_list[0].biases)

        # keep only the best one
        retain_num = int(self.n_pops * self.retain_rate)
        score_list_top = self.score_list[:retain_num]

        # return some non-best ones
        retain_non_best = int((self.n_pops - retain_num) * self.retain_rate)
        for _ in range(random.randint(0, retain_non_best)):
            score_list_top.append(random.choice(self.score_list[retain_num:]))

        # breed new childs if current population number less than what we want
        while len(score_list_top) < self.n_pops:

            father = random.choice(score_list_top)
            mother = random.choice(score_list_top)

            if father != mother:
                new_child = self.crossover(father, mother)
                new_child = self.mutation(new_child)
                score_list_top.append(new_child)

        # copy our new population to current object
        self.nets = score_list_top


def main():
    # load data from data02.xlsx into X and y
    df = pd.read_excel("module_week\preMod\data02.xlsx")
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1:].values
    min_max_scaler = preprocessing.MinMaxScaler()
    # print(X.max(0), X.min(0))
    # print(y.max(), y.min())
    X = min_max_scaler.fit_transform(X)
    y = min_max_scaler.fit_transform(y)
    # print(X)
    # print(y)
    #
    # print(X.shape)
    # print(y.shape)


    # parameters
    N_POPS = 30
    NET_SIZE = [4, 6, 1]
    MUTATION_RATE = 0.2
    CROSSOVER_RATE = 0.4
    RETAIN_RATE = 0.4

    # start our neural-net & optimize it using genetic algorithm
    score_min = np.inf
    nnga = NNGeneticAlgo(N_POPS, NET_SIZE, MUTATION_RATE, CROSSOVER_RATE, RETAIN_RATE, X, y)

    start_time = time.time()

    # run for n iterations
    mse_list = []
    for i in range(2000):
        mse_list.append(float('{:.4f}'.format(nnga.get_all_scores()[0])))
        if i % 10 == 0:
            print("Current iteration : {}".format(i + 1))
            print("Time taken by far : %.1f seconds" % (time.time() - start_time))
            print("Current top member's network mse: %.4f\n" % nnga.get_all_scores()[0])
            # mse_list.append(float('{:.4f}'.format(nnga.get_all_scores()[0])))
            # print("Current top member's network accuracy: %.2f%%\n" % nnga.get_all_accuracy()[0])

        # evolve the population
        nnga.evolve()
        if nnga.score_list_[0][1] < score_min: # mse值小于最佳值，才会更新权重
            print("updating network")
            # print(nnga.score_list[0].weights)
            # print(nnga.score_list[0].biases)
            np.savez("weights.npz", w1=nnga.score_list[0].weights[0], w2=nnga.score_list[0].weights[1], b1=nnga.score_list[0].biases[0], b2=nnga.score_list[0].biases[1])
            # with open('weights.txt', 'w') as f:  # 设置文件对象
            #     f.write([nnga.score_list[0].weights, nnga.score_list[0].biases])
            score_min = nnga.score_list_[0][1]


    # print(len(mse_list))
    plot_loss(mse_list)


if __name__ == "__main__":
    main()