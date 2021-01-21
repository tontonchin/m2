import numpy as np
from mesa import Agent, Model
import math
import random
from mesa.time import SimultaneousActivation
import matplotlib.pyplot as plt
#from  hulistics.hulistics_01 import kakudo
from hulistics_01 import kakudo, kakudo_kai
#from hulistics.hulistics_02 import plot2d, hito_sesyoku, kabe_sessyoku, func_hulistics_2
#from hulistics.syuuino import syuui1,syuui2,hankai,han_kyori
from mesa.space import ContinuousSpace
from scipy import optimize
import matplotlib.animation as animation

"""このプログラムは単なるテストである
タイムステップを増やすだけの単なるテストである"""


fig = plt.figure()
ims = []

#dRange = [0.0 , 50]

#plt.xlim(dRange[0],dRange[1])
#plt.ylim(dRange[0],dRange[1])
#plt.grid(True)
im_x = []
im_y = []


class Hokousya_ue(Agent):
    "人ですこれはmoussaidのヒューリスティクスにしたがう"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # これは設定されたパラメータ，一様である
        self.tyon = 0.5
        self.siyakaku = math.pi/4
        self.dmax = 10
        self.K = 5
        #self.a = (math.pi) / 2
        #self.vi = np.array([1.3,0])
        #self.vdes = np.array([1.3,0])*np.array([math.cos(self.a), math.sin(self.a)])
        # これは，歩行者エージェントごとに異なるもの，初期位置である


        self.iti_x = round(random.randrange(0, 10)*random.random(),2)
        self.iti_y = round(random.randrange(45, 50)*random.random(),2)


        self.a =  3* (math.pi) / 2

        self.iti = np.array([self.iti_x, self.iti_y])
        self.vi = np.array([0, -1.3])
        self.vdes = np.array([0, -1.3])
        self.m = 60
        self.a = math.pi/2


    def step(self):

        "ここで関数を用いる"
        "まず，周囲の位置情報を確認する"
        #pass
        #周囲のエージェントとの距離の確認
        #im.append(plt.scatter(self.iti[0], self.iti[1]))

        #plt.scatter(self.iti[0], self.iti[1])

        im_x.append(self.iti[0])
        im_y.append(self.iti[1])

        self.a = math.pi/2

        agents = syudan
        #print(agents)

        num_hito = num_agents

        kabe = kabes

        num_kabe = num_kabes


        fa, syu_num = self.syuui(num_hito,agents)



        #if syu_num == 0:
            #print("この人には周囲の人がいないので周囲の接触力は考えなくてもよい")

        #print("まえのself.a",self.a)

        maeno_a = self.a

        self.a = kakudo_kai(fa, self.a)

        #if maeno_a != self.a :
            #print("このエージェントは移動時に角度が変化した")
        #else :
            #print("このエージェントは移動時に角度が変化しなかった")

        #print("あとのself.a", self.a)
        #print("self.aのかた",type(self.a))

        #print("self.aは",self.a)
        #kabe_f = self.kabe_f(num_kabe, kabes)

        print("Unique_ID", self.unique_id)
        hito_f = self.syuui_f(syu_num,agents)

        #print("hito_fについて", hito_f)

        #v_des = fa/0.5

        #print("self.vdes", self.vdes)

        #2で割ったことにより1ステップごとのdvdtは0.5秒となる

        V_nomi = self.sokudo()
        dvdt = (V_nomi + hito_f + self.douro_f() ) /2


        print("self.douro_f()",self.douro_f())
        print("hito_f",hito_f)



        dvdt[0] = round(dvdt[0], 3)
        dvdt[1] = round(dvdt[1], 3)

        #dvdt_matome = ((dvdt[0]**2)+(dvdt[1]**2))**0.5

        #dvdt_matome = np.linalg.norm(dvdt)


        #print("dvdt_matome", dvdt_matome)

        dvdt_new = dvdt * np.array([math.cos(self.a), math.sin(self.a)])

        print("dvdt_new", dvdt_new)

        #dvdt[0] = dvdt_matome * math.cos(self.a)
        #dvdt[1] = dvdt_matome * math.sin(self.a)
        print("self.vdes",self.vdes)
        print("これは動く前のself.vi", self.vi)
        maeno_vi = self.vi
        self.vi = self.vi + dvdt_new
        #print("これはdtdsv", dvdt)
        print("これは辺が後のself.vi",self.vi)
        print("これは動く前のself.iti",self.iti)
        self.iti = self.iti + self.vi
        print("new_itiは",self.iti)

        if np.linalg.norm(self.vi) - np.linalg.norm(maeno_vi) >= 0.8:
            print("これは予測できない変化が発生しました")
            #print("これは辺が前のself.vi",maeno_vi)
            #print("これは辺が後のself.vi",self.vi)
            print("v_nomi",V_nomi)



    def syuui(self, num, agents):

        #変数として
        mawari_hito = np.array([])
        for i in range(num):

            matome_i =  agents[i] - self.iti
            #print("matome_i",matome_i,type(matome_i))

            hito_tan = (matome_i[0] / matome_i[1])
            #kyori = ((matome_i[0])**2 + (matome_i[1])**2)**0.5
            kyori =np.linalg.norm(matome_i)
            if kyori <= self.dmax and agents[i,1] >= self.iti[1]:
                if (-1) * math.tan(self.a) <= hito_tan and hito_tan < + math.tan(self.a):
                    mawari_hito = np.append(mawari_hito, kyori)
        if mawari_hito.size == 0:
            fa = self.dmax
        else:
            fa = np.min(mawari_hito)
        return fa,mawari_hito.size

    #def objective_function(theta, fa):
        #return self.dmax * 2 + fa ** 2 - 2 * self.dmax * fa * math.cos(math.radians(self.a - theta))


    """
    def kakudo(self, fa):
            def objective_function(theta, fa):
                return self.dmax * 2 + fa ** 2 - 2 * self.dmax * fa * math.cos(math.radians(self.a - theta))

            min = optimize.fminbound(objective_function, -self.siyakaku, self.siyakaku)
            #これのminが次の角度aになる
            return min
    """
        #その後，ヒューリスティクスの第2段階を行う
        #それらの関数は以下に置いておく
    def kabe_f(self, num, kabe):
        kouryo = np.array([])
        for i in range(num):
            #print("@@@@@@@@@@",self.iti,kabe(i))
            matome_i = kabe[i] - self.iti
            kabe_tan = (matome_i[0]/ matome_i[1])
            #nagasa = ((matome_i[0])**2 + (matome_i[1])**2)**0.5
            nagasa = np.linalg.norm(matome_i)
            niw = matome_i / nagasa
            if nagasa <= self.dmax and kabe[i,1] >= self.iti[1] :
                if (-1)*self.siyakaku <= kabe_tan and kabe_tan <+ self.siyakaku:
                    fiw = 0.5 * 9.8 * (self.m / 360 - nagasa)*(niw)
                    fiw = fiw / self.m
                    kouryo = np.append(kouryo, fiw)
        sum_fiw = np.sum(kouryo)
        return sum_fiw

    def douro_f(self):
        fiw = 0
        if self.iti[0] <= 10:
            fiw = 0.5 * 9.8 * (60/360 - self.iti[0])
        elif  self.iti[0] >= 40:
            fiw = 0.5 * 9.8 * (60/360 - (self.iti[0]-40))
        fiw_douro = np.array([fiw, 0])
        return fiw_douro




    def syuui_f(self, num, agents):
        mawari_hito = np.array([])
        for i in range(num):
            #位置関係
            matome_i = agents[i] - self.iti
            hito_tan = (matome_i[0]/ matome_i[1])
            #kyori = ((matome_i[0])**2 + (matome_i[1])**2)**0.5
            kyori = np.linalg.norm(matome_i)
            nij = matome_i / kyori
            if kyori <= self.dmax and agents[i,1] >= self.iti[1]:
                if (-1) * math.tan(self.siyakaku) <= hito_tan and hito_tan < + math.tan(self.siyakaku):
                    fij = 000000.5 * 9.8 * ((self.m/360 * 2) - kyori) *(nij)
                    fij = fij / self.m
                    mawari_hito = np.append(mawari_hito, fij)
        sum_fij = np.sum(mawari_hito)
        syuui_f = np.array([math.cos(self.a)*sum_fij, math.sin(self.a)*sum_fij])
        return syuui_f

    def sokudo(self):
        dvdt = ((self.vdes-self.vi)/0.5)
               #+ self.kabe_f() +self.syuui_f()
        return dvdt



        #print(self.unique_id, self.kaisu, "目")