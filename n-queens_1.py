#!/usr/bin/python
# -*- coding: utf-8 -*-
# N-queen by Simulated Aneeling
# シミュレーティッドアニーリング（焼きなまし法）によるN-Queen
# 離散モデル
#
# エネルギー関数、重み、閾値は次の文献を参考
# https://www.jstage.jst.go.jp/article/jceeek/2008/0/2008_0_451/_pdf
#
import random
import math

class Network:
    '''
    ネットワークを管理

        size  = 盤の大きさ

        unitsum = 実体　行数分の要素、要素内の番号はその行の列位置
        unitout = 
        cost = コスト
        temperature = 温度
        alpha = 減衰率
    '''
    def __init__(self, size, temperature, alpha):
        '''
        初期化
        ネットワークを初期化（ユニット、重み、エネルギー）
        '''
        # ユニットの初期化
        self.size  = size
        self.unit = [[1 if i == j else 0 for i in range(size)] for j in range(size)]   # list(range(size))

        # 重みの設定
        p_a = 1
        p_b = 1
        p_c = 1
        p_d = 1

        self.weight = [[[[-2*p_a*self.nd(x,a)*self.d(y,b)-2*p_b*self.nd(y,b)*self.d(x,a)-2*p_c*self.d(x-y,a-b)-2*p_d*self.d(x+y,a+b) for x in range(size)] for y in range(size)] for a in range(size)] for b in range(size)]
        # 自己結合を0にする
        for x in range(self.size):
            for y in range(self.size):
                self.weight[x][y][x][y] = 0

        self.theta = -2*(p_a+p_b)

        ### Boltzman : Simulated Aneeling
        # 温度
        self.temperature = temperature
        # 減衰率
        self.alpha = alpha

    def d(self, i,j):
        '''
        delta関数
        '''
        return 1 if i==j else 0

    def nd(self, i,j):
        '''
        delta関数の反転
        '''
        return 0 if i==j else 1

    def update(self):
        '''
        任意のユニットの値を更新する
        Boltzmanマシン
        '''
        rx = random.randrange(self.size)
        ry = random.randrange(self.size)

        val_in = -self.theta  # unitへの入力値
        for a in range(self.size):
            for b in range(self.size):
                val_in += self.weight[rx][ry][a][b]*self.unit[a][b]

        # 値が1になる確率（Boltzmann分布に基づいて温度から計算する）
        try:
            p = 1.0 / ( 1.0 + math.exp(-val_in/self.temperature))
        except:
            vv = -val_in/self.temperature
            p = 0.0 if vv > 0 else 1.0 if vv < 0 else 0.5


        # 温度を減衰
        self.temperature = self.temperature * self.alpha

        # 確率に基づいて状態遷移
        val = 1 if p > random.random() else 0

        # 状態が変化したらTrue
        if val != self.unit[rx][ry]:
            self.unit[rx][ry] = val
            return True

        return False

    def energy(self):
        '''
        エネルギー計算
        '''
        item1 = 0
        item2 = 0
        for x in range(self.size):
            for y in range(self.size):
                for a in range(self.size):
                    for b in range(self.size):
                        item1 += self.weight[x][y][a][b] * self.unit[x][y] * self.unit[a][b]
                item2 += self.theta * self.unit[x][y]
        return  -item1/2.0+item2 + self.size

    def is_active(self,val):
        '''
        指定値からQueenの存在を判定
        '''
        return val == 1

    def check(self):
        '''
        正解判定
        '''
        checkunit = [[0 for i in range(self.size)] for j in range(self.size)]
        count = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.is_active(self.unit[x][y]):
                    count += 1

                    # 交わっていたらFalse
                    if checkunit[x][y] == 1:
                        return False

                    # 同じy軸
                    for cx in range(self.size):
                        checkunit[cx][y] = 1
                    # 同じx軸
                    for cy in range(self.size):
                        checkunit[x][cy] = 1
                    # 右斜め下
                    dl = y - x
                    for ix in range(self.size):
                        iy = ix + dl
                        if iy < 0:
                            continue
                        if iy >= self.size:
                            break
                        checkunit[ix][iy] = 1
                    # 右斜め上
                    dl = x + y
                    for ix in range(self.size):
                        iy = dl - ix
                        if iy < 0:
                            break
                        if iy >= self.size:
                            continue
                        checkunit[ix][iy] = 1

        # size個のQueenが交わっていなかったらTrue
        return True if count == self.size else False

    def display(self):
        '''
        表示
        '''
        print(self.energy())
        for x in range(self.size):
            print( [ 1 if self.is_active(val) else 0 for val in self.unit[x] ] )
        print()

def train(max_iter, size, temperature, alpha):
    '''
    学習
    '''
    network = Network(size, temperature, alpha)
    network.display()

    for iter in range(max_iter):
        if network.update():
            network.display()

            # 解に到達したら終了
            if network.check():
                print("OK")
                break
    return

if __name__ == '__main__':
    size = 8
    max_iter = size*size*100
    temperature = size*size*10
    alpha = 0.99

    train( max_iter, size, temperature, alpha)
