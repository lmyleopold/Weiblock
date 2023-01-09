import matplotlib.pyplot as pl
import networkx as nx
import numpy as np
import random as r
import textwrap as w
from math import factorial
import json
import csv



def find_user():
    tf = open("myDic.json", "r")
    new_dict = json.load(tf)
    tf.close()
    return new_dict




def get_all_nodes():
    tf = open("myDic.json", "r")
    new_dict = json.load(tf)
    id_list = list(new_dict.keys())
    
    with open("all_id_list_covid.csv", "w", newline="") as file:
        csv_write = csv.writer(file, delimiter=',')
        for i in range(0, len(id_list)):
            csv_write.writerow([id_list[i]])
            
    file.close()



def get_k(d, value):
    k = [k for k, v in d.items() if v == value]
    return k

def get_each_round_infected(infected_t):
    tf = open("myDic.json", "r")
    new_dict = json.load(tf)
    with open("each_round_infected_covid.csv", "a", newline="") as file:
        csv_write = csv.writer(file, delimiter=',')
        for each in infected_t:
            csv_write.writerow(get_k(new_dict, each))
        csv_write.writerow('')
    file.close()



class Rumour_infection:
    
    """
    这是一个标准的SI流行病模型的变种，适用于谣言在网络中的传播模型。我们跟踪每个节点，但不关注其是否感染。相反，我们提出了一个概念，
    即每个节点都有一个介于-1和1之间的初始态度和一个介于0和1之间的暗示值，如果一个节点在某个时间段观察到谣言，
    其初始态度就会被更新，形成一个获得的态度，一个节点的获得态度是其初始态度、暗示值和是否观察到谣言的函数。
    并非所有观察到谣言的节点都会将其传递给其邻居，只有达到一定获取态度阈值的节点才会分享谣言。
    """
    
    def __init__(self):
        pass

    
    def set_attitude(g, dstrb_ia='uniform',dstrb_gull='uniform',special_infu=False,seed=None):
        """
        这个函数用来设置每个节点的初始态度（值在-1和1之间）和暗示值（值在0和1之间），使用一个特定分布中的随机变量。
        这个函数提供了正态分布、β分布和指数分布的选项。

        Parameters: 
            g: a networkx graph object 
            dstrb_ia: initial attitude distribution
                - 'uniform': Uniform distribution between -1 and 0
                - 'normal':  Normal distribution with mean 0 and standard dev. .3
                - 'beta':    Beta distribution between -1 and 0
                - 'expn1':   Exponential distribution skewed to -1
                - 'exp1':    Exponential distribution skewed to 1
            dstrb_gull: gullibility/suggestibility factor distribution
                - 'uniform': Uniform distribution between 0 and 1
                - 'normal':  Normal distribution with mean .5 and standard dev. .15
            special_infu: influencer as a special case of node 
                - True|False 
        """    
        
        
        #设置种子
        np.random.seed(seed)
        r.seed(seed) 
        
        # 分布的选项
        if dstrb_ia =='uniform':
            x=np.random.uniform(low=-1.0, high=1.0, size=10000)
        elif dstrb_ia =='normal':
            x= np.random.normal(0, .3, 1000)
        elif dstrb_ia =='beta':
            x= -1 + (np.random.beta(.4, .4,size=10000) * (1 - -1))
        elif dstrb_ia =='expn1':
            x=(-1 + (np.random.exponential(.1,10000)* (1 - -1)))
        elif dstrb_ia =='exp1':
            x=(-1 +((np.random.exponential(.1,10000)*-1)+1)* (1 - -1))
            
        # 暗示值的分布
        if dstrb_gull =='uniform':
            y=np.random.uniform(low=0.0, high=1.0, size=10000)
        elif dstrb_gull =='normal':
            y= np.random.normal(.5, .15, 1000)
    
        # 应用到图节点
        for i in g.nodes():
            g.node[i]['id']=i
            g.node[i]['initial_attitude']=r.choice(x)
            # We initialise acquired attitude to 0 at t=0
            g.node[i]['acquired_attitude']=0
            g.node[i]['gullibility']=r.choice(y)
    
        # 由于人们在社会网络中扮演不同的角色，我们初步认为有一成左右的人可能比其他人对谣言的传播有更大的决定性影响。
        # 他们可能代表一个机构，其利益随着时间的推移而保持固定，或者因为他们的重要性是他们所传播的信息种类的一致性的函数。
        # 我们把这些人作为节点的一个特例来模拟。我们把他们的态度看作一个固定值，而他们的暗示性是零，并用他们的程度中心性来衡量他们的影响力。
        if special_infu == True: 
            inf_nodes=int(round(len(g.nodes())*.1))
            inf_measure=nx.degree_centrality(g)
            top_infs=sorted(inf_measure, key=inf_measure.get, reverse=True)[:inf_nodes]
            for n in top_infs:
                g.node[n]['initial_attitude']=1
                g.node[n]['gullibility']=0

        return g

    def initialise_rumour_source(G,n_nodes,sel_source=None,n_sources=1,rumour=1,seed=None):
        """
         初始化函数
         Parameters: 
             G:             Input graph
             n_nodes:       Number of nodes in graph 
             n_sources:     Number of sources typically 1
             sel_source:    Used to manually select the source, if = None a 
                            source is selected at random
             rumour:        Rumour value typically 1 or -1 
             seed:          For repeatable random selection 
        
        """
        
        #设置种子
        np.random.seed(seed)
        
        #可手动选择传染源
        #也可随机选择
        if sel_source==None: 
        #随机选择
            source =(np.random.choice(range(0,n_nodes), n_sources,replace=False)).tolist()
        else:
            source=[sel_source]
        frontier = nx.Graph()
        
        infected = nx.Graph()
        #源节点受感染
        for source in source:
            infected.add_node(source) 
            infected.node[source]['initial_attitude']=0
            infected.node[source]['acquired_attitude']=rumour
            infected.node[source]['gullibility']=0

        for node in infected:
            for neighbor in G.neighbors(node):
                if not infected.has_node(neighbor):
                    frontier.add_node(neighbor)
        
        return source, infected, frontier
    
    def rumour_step(G,frontier, infected, prob,rumour,trnsmt_tshd):
            """ 
            谣言传播函数。其中有两个图，G是完整图，infected是看到谣言者的子图
            Parameters: 
                G: a networkx graph object
                frontier: graph object to store neighbours of nodes that observed rumour
                infected: graph object to store nodes that have observed rumour
                prob:     probability of observing rumour at time t 
                rumour:   We assume the rumour can be represented as a 
                          single real number between -1 and 1
                Trnsmt_tshd: The minimal acquired attitude required to transmit the rumour  
            """
            frontier_degree_t = []
            # 新观察到谣言的节点的列表
            infected_t = []
            #观察到并传播该谣言的节点列表 
            transmitted = []
            # 生成包含有i个观察到的邻居的节点的列表
            for node in frontier:
                i = 0
                for neighbor in G.neighbors(node):
                    if infected.has_node(neighbor):
                        i += 1
                try:
                    frontier_degree_t[i-1].append(node)
                except IndexError:
                    for j in range(0, i+1):
                        t = []
                        frontier_degree_t.append(t)
                    frontier_degree_t[i-1].append(node)
    
            for j in range(0, len(frontier_degree_t)):
                if len(frontier_degree_t[j]) > 0:
                    f_j = len(frontier_degree_t[j])
                    print('Number of neighbors that have not heard rumour:',f_j)
                    p_j = 1-(1-prob)**(j+1)
                    print('Probability of rumour being transmitted:',p_j)
                    n_j = int(min(np.floor(p_j*(f_j+1)), f_j))
                    print('Number of neighbors that will hear the rumour:',n_j)
                    s = np.random.choice(frontier_degree_t[j], n_j,replace=False)
                    ### 改
                    new_id_dict = find_user()
                    print('this round will infect:', s)
                    ### 改
                    get_each_round_infected(s)
                    infected_t.append(s)
                        
            # 更新新观察到谣言的节点类别
            for j in infected_t:
                # 更新每个看到谣言的节点
                for node in j:
                    if node == 33:
                        continue
                    infected.add_node(node)
                    infected.node[node]['initial_attitude']=G.node[node]['initial_attitude']
                    infected.node[node]['gullibility']=  G.node[node]['gullibility']
                    infected.node[node]['acquired_attitude']=  min(((G.node[node]['initial_attitude'])
                                                        +((G.node[node]['gullibility'])*(rumour))),1)
                    
                    #一旦加入到受感染的图中，就会从新观察到谣言列表中移除
                    frontier.remove_node(node)
                    #只有当新感染的节点超过获得的态度阀值时，它才能传播谣言。
                    if infected.node[node]['acquired_attitude'] > trnsmt_tshd:
                        transmitted.append(node)
                        for neighbor in G.neighbors(node):
                                if not infected.has_node(neighbor):
                                    frontier.add_node(neighbor) 
                                    
            return infected_t,transmitted               

    def simulation(G,frontier, infected,rumour,time_periods,prob,trnsmt_tshd,graph_plot=False,diag_plot=False,save_plot=False,labels=True):
        """ 
        迭代步骤函数，直到图形完全收敛（所有节点都听到了谣言）或没有观察到谣言的节点的 "获得态度 "超过允许的阈值。
        这组模拟的阈值 这组模拟的阈值被设定为0.25，这个阈值相对较低。
        这个函数可以可视化输出。

        
        Parameters: 
                G:              a networkx graph object
                frontier:       graph object to store neighbours of nodes that observed rumour
                infected:       graph object to store nodes that have observed rumour
                rumour:         We assume the rumour can be represented as a 
                                single real number between -1 and 1
                time_periods:   t periods to run the simulation for
                prob:           probability of observing the rumour at time t 
                trnsmt_tshd:    the minimal acquired attitude required to 
                                transmit the rumour 
                graph_plot:     True|False - for each t a graph differentiating 
                                  nodes that have/haven't observed the rumour is plotted 
                diag_plot:      True|False - display simulation diagnostic plots
                save_plots:     True|False - save plots to file.
        """
 
        t=0                 # 将时间步长初始化为0，每步增加1。
        aa_delta_t=[]       # 列表中存储了每个t中获得的平均态度
        rumour_prop=[]      # 看到过谣言的节点比例
        pass_prop=[]        # 传播谣言的节点比例
        not_infected=[1]
        # 运行模拟，直到所有节点都被感染
        #len(not_infected) > 0 时开始
        pos = nx.fruchterman_reingold_layout(G) # 保持节点位置固定
    
        while len(not_infected) > 0 and t < time_periods:
            # 运行模拟，直到所有节点都被感染或超时。
            #在这里保存一下此时的infected

            Rumour_infection.edging(G, infected)
            
            if graph_plot==True: 
                col=list((nx.get_node_attributes(infected,'acquired_attitude')).values())
                fig=pl.figure(num=None, figsize=(8, 8), dpi=80)
                ax = fig.add_subplot(111)
                
                #画原始G+（被感染）图
                nx.draw(G, pos=pos,with_labels= labels,font_size=8, font_color='black'
                        ,node_color = 'seagreen')
                
                nx.draw(infected, pos=pos,edge_color='lightcoral',font_size=8, 
                        font_color='black',font_weight='bold',
                        with_labels= labels,node_color=col,cmap=pl.cm.Blues)
                
                #加时间戳
                text1 ='Time step:'+str(t)#+'- the infected nodes are:'+str(infected.nodes()) #infected.nodes()里多出哪些昕感染的节点
                ax.text(0.01, 0.000002, (w.fill(text1, 100)), verticalalignment='bottom', 
                        horizontalalignment='left', transform=ax.transAxes,color='black', 
                        fontsize=10,wrap=True)
                
                if save_plot==True: 
                    pl.savefig("rumour_%s.png" % str(t).zfill(3),dpi=1000) # pad filename with zeros
                pl.show()
                print('Time step:',t)
                # print('此轮感染：', last_round_infected)

                ### 在这里用infected后的减去infected前的
                ### or 用上一次说的感染节点数倒数输出
        
            last_round_infected = infected.nodes()
            # print('last_round_infected:', set(last_round_infected))
            # call rumour_step 
            not_infected,transmitted =Rumour_infection.rumour_step(G, frontier,
                                                   infected, prob,1,trnsmt_tshd)
            t=t+1 #Increment t
            this_round_infected = infected.nodes()
            # print('this_round_infected:', set(this_round_infected))
            # print('此轮感染：', set(this_round_infected) - set(last_round_infected))

            aa_infected=nx.get_node_attributes(infected,'acquired_attitude')
            aa_all=nx.get_node_attributes(G,'acquired_attitude')
            not_infected_at_t = [val for sublist in not_infected for val in sublist]
            aa_not_infected = { not_infected_at_t: aa_all[not_infected_at_t] 
                               for not_infected_at_t in not_infected_at_t }
            aa_both={**aa_infected,**aa_not_infected}
            avg_aa=sum(list(aa_both.values()))/float(len(list(aa_both.values())))
            aa_delta_t.append(avg_aa)
            rumour_prop.append(len(infected.node)/len(G.node))
            pass_prop.append(len(transmitted)/len(infected.node))
            #初始状态的柱状图
            
        if diag_plot==True: # 仅在True时绘制模拟诊断图
            Rumour_infection.diagnostic_plots(G,infected,aa_delta_t,rumour_prop,pass_prop)

        return G, infected,t,aa_delta_t,rumour_prop,pass_prop, pos
        
  
        
    def edging(graph, graph_i):
        """ 
        将原始图G的边缘转置到被感染图上
        """
        for node in graph_i:
            for neighbor in graph.neighbors(node):
                if graph_i.has_node(neighbor):
                    graph_i.add_edge(node, neighbor)
        
    def diagnostic_plots(G,infected,aa_delta_t,rumour_prop,pass_prop): 
        """ 
        模拟运行后调用一些诊断图

        Parameters: 
                G:              orginal graph object 
                infected:       graph object to store nodes that have observed rumour
                aa_delta_t:     mean acquired attitude at each t of simulation
                rumour_prop:    % of nodes who have heard rumour
                pass_prop:      % of nodes who heard and transmitted  the rumour            
        """
        
        pl.figure(figsize=(8,5))
        pl.title('Distribution of initial attitude') 
        pl.hist(list((nx.get_node_attributes(G,'initial_attitude')).values()),
                50,normed=True) 
        pl.ylabel('Proportion %')
        pl.xlabel('initial attitude (0-1)')
        pl.show()
        
        pl.figure(figsize=(8,5))
        pl.title('Distribution of gullibility') 
        pl.hist(list((nx.get_node_attributes(G,'gullibility')).values()), 50, 
                 normed=True)
        pl.ylabel('Proportion %')
        pl.xlabel('gullibility (0-1)')
        pl.show()
        pl.figure(figsize=(8,5))
        pl.title('Distribution of acquired attitude') 
        pl.hist(list((nx.get_node_attributes(infected,
        'acquired_attitude')).values()), 50, normed=True)
        pl.ylabel('Proportion %')
        pl.xlabel('acquired attitude (0-1)')
        pl.show()
        
        pl.figure(figsize=(8,5))
        pl.title('Distribution of acquired attitude') 
        pl.plot(aa_delta_t)
        pl.ylabel('acquired attitude (0-1)')
        pl.xlabel('Time Step')
        pl.show()
        
        pl.figure(figsize=(8,5))
        pl.title('Rumour Propagatation: % of nodes who have heard rumour') 
        pl.plot(rumour_prop)
        pl.ylabel('% of nodes who have heard rumour')
        pl.xlabel('Time Step')
        pl.show()
        
        pl.figure(figsize=(8,5))
        pl.title('Rumour Propagatation: % of nodes who heard and transmitted the rumour') 
        pl.plot(pass_prop)
        pl.ylabel('% of nodes who heard and transmitted the rumour')
        pl.xlabel('Time Step')
        pl.show()

        




"""
第二部分
"""




G_fb = nx.read_edgelist("weibo_forward_list_num_covid.txt", create_using = nx.Graph(), nodetype = int)
G_a=Rumour_infection.set_attitude(g=G_fb,dstrb_ia='beta',dstrb_gull='uniform',special_infu=False,seed=483)
seed, infected, frontier=Rumour_infection.initialise_rumour_source(G=G_a,n_nodes=nx.number_of_nodes(G_fb),sel_source=0,n_sources=1,rumour=1,seed=None)

G_b, G_i,t,aa_delta_t,rumour_prop,pass_prop=Rumour_infection.simulation(G_a,frontier,infected,rumour=1, time_periods=50,prob=.7,trnsmt_tshd=.25,graph_plot=True,diag_plot=True,save_plot=True,labels=False)

