from module_week.preMod.ga_net import Network, X_border, y_border
import numpy as np

class FitnessCalculator:
    def __init__(self) -> None:
        self.net = Network([4, 3, 1])
        # 加载权重
        self.data = np.load('/home/shikamaru/workspace/postDT/module_week/preMod/weights.npz')
        w = [self.data['w1'], self.data['w2']]
        b = [self.data['b1'], self.data['b2']]
        self.net.weights[0], self.net.weights[1] = w[0], w[1]
        self.net.biases[0], self.net.biases[1] = b[0], b[1]
        pass

    def calFitness(self, code: list):

        # 设置特征输入 (N, 4)
        X = np.array([[code[0], code[1], code[2], code[3]]])

        # 归一化
        X = (X-X_border[1])/(X_border[0]-X_border[1])
        # 预测并放缩
        fitness = self.net.feedforward(X.T).reshape(-1)*(y_border[0]-y_border[1])+y_border[1]

        # print(fitness)
        return fitness

    def testCost(self, pop):
        fit = 0
        # print(pop)
        for i in range(len(pop['d'])):
            r, s, h, c = 0, 0, 0, 0
            r = sum(pop['r'][i].values())
            s = sum(pop['s'][i].values())
            h = sum(pop['h'][i].values())
            c = sum(pop['c'][i].values())
            fit += int(self.calFitness([r, s, h, c]))
        return fit
        pass


# calFitness([253, 162, 162, 250])
