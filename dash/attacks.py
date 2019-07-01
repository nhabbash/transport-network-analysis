import networkx as nx
import operator
import random
import plotly.plotly as py
import plotly.graph_objs as go

#misure di centralita
def measures(G):
    degree_dic={}
    ev_dic={}
    clos_dic={}
    bet_dic={}
    page_dic={}
    clus_dic={}
    num_nodes=nx.number_of_nodes(G)
    degree=nx.degree_centrality(G)
    eigenvector=nx.eigenvector_centrality(G,weight='weight')
    closeness=nx.closeness_centrality(G)
    betweenness=nx.betweenness_centrality(G,weight='weight')
    pagerank=nx.pagerank(G,weight='weight')
    cluster=nx.clustering(G,weight='weight')
    for i in range(num_nodes):
        if str(i) in degree.keys():
            degree_dic[i]=degree[str(i)]
        if str(i) in eigenvector.keys():
            ev_dic[i]=eigenvector[str(i)]
        if str(i) in closeness.keys():
            clos_dic[i]=closeness[str(i)]
        if str(i) in betweenness.keys():
            bet_dic[i]=betweenness[str(i)]
        if str(i) in pagerank.keys():
            page_dic[i]=pagerank[str(i)]
        if str(i) in cluster.keys():
            clus_dic[i]=cluster[str(i)]
    return degree_dic,ev_dic,clos_dic,bet_dic,page_dic,clus_dic

def list_clustering(G):
    clus_dic={}
    num_nodes=nx.number_of_nodes(G)
    cluster=nx.clustering(G)
    for i in range(num_nodes):
        if str(i) in cluster.keys():
            clus_dic[i]=cluster[str(i)]
    return clus_dic

def list_pagerank(G):
    page_dic={}
    num_nodes=nx.number_of_nodes(G)
    pr=nx.pagerank(G)
    for i in range(num_nodes):
        if str(i) in pr.keys():
            page_dic[i]=pr[str(i)]
    return page_dic

def list_degree(G):
    degree_dic={}
    num_nodes=nx.number_of_nodes(G)
    degree=nx.degree_centrality(G)
    for i in range(num_nodes):
        if str(i) in degree.keys():
            degree_dic[i]=degree[str(i)]
    return degree_dic

def list_closeness(G):
    c_dic={}
    num_nodes=nx.number_of_nodes(G)
    closeness=nx.closeness_centrality(G)
    for i in range(num_nodes):
        if str(i) in closeness.keys():
            c_dic[i]=closeness[str(i)]
    return c_dic

def list_betweenness(G):
    b_dic={}
    num_nodes=nx.number_of_nodes(G)
    betweenness=nx.betweenness_centrality(G,weight='weight')
    for i in range(num_nodes):
        if str(i) in betweenness.keys():
            b_dic[i]=betweenness[str(i)]
    return b_dic
   
def list_eigenvector(G):
    e_dic={}
    num_nodes=nx.number_of_nodes(G)
    eigenvector=nx.eigenvector_centrality_numpy(G,weight='weight')
    for i in range(num_nodes):
        if str(i) in eigenvector.keys():
            e_dic[i]=eigenvector[str(i)]
    return e_dic

def list_degree_average(G):
    davg_dic={}
    num_nodes=nx.number_of_nodes(G)
    degree=nx.k_nearest_neighbors(G, weight='weight')
    for i in range(num_nodes):
        if str(i) in degree.keys():
            davg_dic[i]=degree[str(i)]
    return davg_dic

def list_edge_betweenness(G):
    edge={}
    edges_list=list(G.edges())
    edge_betweenness=nx.edge_betweenness_centrality(G, normalized=True, weight='weight')
    for i in edge_betweenness.keys():
        edge[i]=edge_betweenness[i]
    return edge

#crea una lista ordinata in modo decrescente
def ranking_nodes(measure):
    tmp= sorted_x = sorted(measure.items(), key=lambda kv: kv[1])
    tmp=tmp[::-1]
    return [i[0] for i in tmp]


#attacchi 
   
def set_rank_attack(G,ranking,dimension):
    N=nx.number_of_nodes(G)
    S=[100]
    #esegue gli attacchi
    for i in range(dimension):
        #nodi della max componente connessa 
        nodes = map(int, list(G.nodes))
        
        #prende max node presente nella componente connessa
        node=next(x for x in ranking if x in nodes )
        
        #print(node)
        G.remove_node(str(node))
        
        #prende nuova max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        S.append((float(nx.number_of_nodes(G))/N)*100)
        if len(G.nodes) ==1:
            return S
        
    return S

def random_vertex(G,dimension):
    N=nx.number_of_nodes(G)
    S=[100]
    #esegue gli attacchi
    for i in range(dimension):
        node=int(random.choice(list(G.nodes)))
    
        G.remove_node(str(node))
        #prende max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        S.append((float(nx.number_of_nodes(G))/N)*100)
        if len(G.nodes) ==1:
            return S
    return S 

def random_neighbor(G,dimension):
    N=nx.number_of_nodes(G)
    S=[100]
    #esegue gli attacchi
    for i in range(dimension):
        node=int(random.choice(list(G.nodes)))
        neighbor=list(G.neighbors(str(node)))
        for nei in neighbor:
            G.remove_node(str(nei))
        #prende max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        S.append((float(nx.number_of_nodes(G))/N)*100)
        if len(G.nodes) ==1:
            return S
    
    return S  

def random_edge(G,dimension):
    N=nx.number_of_nodes(G)
    S=[100]
    #esegue gli attacchi
    for i in range(dimension):
        node=int(random.choice(list(G.nodes)))
        neighbor=int(random.choice(list(G.neighbors(str(node)))))
        G.remove_edge(str(node),str(neighbor))
        #prende max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        S.append((float(nx.number_of_nodes(G))/N)*100)
        if len(G.nodes) ==1:
            return S
    
    return S

def set_rank_attack_edge(G,ranking,dimension):
    N=nx.number_of_nodes(G)
    S=[100]
    #esegue gli attacchi
    for i in range(dimension):
        #archi della max componente connessa 
        edges =list(G.edges)
        
        #prende max edge presente nella componente connessa
        if len(edges) < 3:
            S.append(0)
            return S
        node1,node2=next(x for x in ranking if x in edges)
        G.remove_edge(node1,node2)
        
        #prende nuova max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        S.append((float(nx.number_of_nodes(G))/N)*100)
        if len(G.edges) == 1:
            return S        
    return S

def update_rank_attack_edge(G,dimension):
    N=nx.number_of_nodes(G)
    S=[100]
   
    #esegue gli attacchi
    for i in range(dimension):
        centrality=list_edge_betweenness(G)
        
        if ranking_nodes(centrality) == []:
            S.append(0)
            return S
        node1,node2=ranking_nodes(centrality)[0]
        
        G.remove_edge(node1,node2)
        #prende nuova max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        S.append((float(nx.number_of_nodes(G))/N)*100)
        if len(G.edges) == 1:
            return S
    return S

def measure_path(G):
    aspl=[]
    for g in nx.connected_component_subgraphs(G):
        aspl.append(nx.average_shortest_path_length(g))
    average_spl=float(sum(aspl))/len(aspl)
    
    average_diameter=[]
    for g in nx.connected_component_subgraphs(G):
        average_diameter.append(nx.diameter(g))
    average_d=float(sum(average_diameter))/len(average_diameter)
    
    return average_spl, average_d
    
    
#calcolo delle misure per i cammini
def update_rank_attack(G,dimension,measure,paths):
    '''
    paths = 1 calcola le misure per i cammini
    '''
    N=nx.number_of_nodes(G)
    S=[100]
    G_copy=G.copy()
    net=[nx.average_shortest_path_length(G)]
    diameter_net=[nx.diameter(G)]
    net_average=[nx.average_shortest_path_length(G)]
    diameter_average=[nx.diameter(G)]
    
    #esegue gli attacchi
    for i in range(dimension):
        if measure =='degree':
            centrality=list_degree(G)
        elif measure =='closeness':
            centrality=list_closeness(G)
        elif measure =='betweenness':
            centrality=list_betweenness(G)
        elif measure =='eigenvector':
            centrality=list_eigenvector(G)
        elif measure =='pagerank':
            centrality=list_pagerank(G)
        elif measure =='clustering':
            centrality=list_clustering(G)
        else :
            return -1
        if ranking_nodes(centrality) ==[]:
            S.append(0)
            if paths==1:
                return S,net,diameter_net,net_average,diameter_average
            else:
                return S
        
        max_measure=ranking_nodes(centrality)[0]
        node=max_measure
        G.remove_node(str(node))
        G_copy.remove_node(str(node))
   
        #prende nuova max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        if paths==1:
            net.append(nx.average_shortest_path_length(G))
            diameter_net.append(nx.diameter(G))
            short_path, diam_av= measure_path(G_copy)
            net_average.append(short_path)
            diameter_average.append(diam_av)
        
        S.append((float(nx.number_of_nodes(G))/N)*100)
        if len(G.nodes) ==1:
            if paths==1:
                return S,net,diameter_net,net_average,diameter_average
            else:
                return S
    if paths==1:
        return S,net,diameter_net,net_average,diameter_average
    else:
        return S


def update_degree_attack(G,dimension):
    N=nx.number_of_nodes(G)
    S=[100]
    number_node=[N]
    degree_avg=[round(float(sum(list_degree(G).values()))/len(list_degree(G)),3)]
    c_avg=[round(float(sum(list_closeness(G).values()))/len(list_closeness(G)),3)]
    b_avg=[round(float(sum(list_betweenness(G).values()))/len(list_betweenness(G)),3)]
    pr_avg=[round(float(sum(list_pagerank(G).values()))/len(list_pagerank(G)),3)]
    ev_avg=[round(float(sum(list_eigenvector(G).values()))/len(list_eigenvector(G)),3)]
    short_path=[round(nx.average_shortest_path_length(G),3)]
    diameter=[nx.diameter(G)]
    cluster_avg=[round(float(sum(list_clustering(G).values()))/len(list_clustering(G)),3)]
    #esegue gli attacchi
    for i in range(dimension):
        centrality=list_degree(G)
        if ranking_nodes(centrality)==[]:
            S.append(1)
            return S
        max_measure=ranking_nodes(centrality)[0]
        node=max_measure
        G.remove_node(str(node))
        #prende nuova max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        number_node.append(nx.number_of_nodes(G))
        degree_avg.append(round(float(sum(list_degree(G).values()))/len(list_degree(G)),3))
        c_avg.append(round(float(sum(list_closeness(G).values()))/len(list_closeness(G)),3))
        b_avg.append(round(float(sum(list_betweenness(G).values()))/len(list_betweenness(G)),3))
        pr_avg.append(round(float(sum(list_pagerank(G).values()))/len(list_pagerank(G)),3))
        ev_avg.append(round(float(sum(list_eigenvector(G).values()))/len(list_eigenvector(G)),3))
        short_path.append(round(nx.average_shortest_path_length(G),3))
        diameter.append(nx.diameter(G))
        cluster_avg.append(round(float(sum(list_clustering(G).values()))/len(list_clustering(G)),3))
        S.append(round(((float(nx.number_of_nodes(G))/N)*100),3))
        if len(G.nodes) ==1:
            return S
    return S,number_node, degree_avg, c_avg, b_avg, pr_avg, ev_avg,short_path, diameter, cluster_avg



