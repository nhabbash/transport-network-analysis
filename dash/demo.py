import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import networkx as nx
import operator
import random
import dash_table as dt
import folium
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from attacks import *


def degree_values(G):
    support=[]
    for i in G:
        support.append(i[1])
    tmp=Counter(support)
    x_d=[]
    y_d=[]
    for val in tmp:
        x_d.append(val)
        y_d.append(tmp[val])
    return(x_d,y_d)

def list_values(result): 
    x=[]
    for i in result:
        x.append(result[i])
    return x

def random_neighbor(dimension):
    G = nx.read_gml("../data/graphs/net_c2c.gml")
    N=nx.number_of_nodes(G)
    S=[100]
    #esegue gli attacchi
    for i in range(dimension):
        node=int(random.choice(list(G.nodes)))
        neighbor=list(G.neighbors(str(node)))
        for n in neighbor:
            G.remove_node(n)
        #prende max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        S.append((float(nx.number_of_nodes(G))/N)*100)
        
        if len(G.nodes) ==1:
            return S
    
    return S

#create net 
metro = nx.read_gml("../data/graphs/metro.gml")
bus = nx.Graph(nx.read_gml("../data/graphs/bus.gml").to_undirected())
tram = nx.Graph(nx.read_gml("../data/graphs/tram.gml").to_undirected())

# Bus and tram share some stops, some processing is needed before uniting the nets. In the composition, bus attributes take the precedence
bus_tram = nx.compose(tram, bus)

for node in tram.nodes(data = True):
    if node[1]["routes"] != bus_tram.node[node[0]]["routes"]:
        bus_tram.node[node[0]]["routes"] += "," + (node[1]["routes"])

net = nx.union(metro, bus_tram)


#attack update list rank
c2c = nx.read_gml("../data/graphs/net_c2c.gml")

U=update_rank_attack(c2c,40,'degree',0)
U1=update_rank_attack(c2c,40,'closeness',0)
U2=update_rank_attack(c2c,40,'betweenness',0)
U3=update_rank_attack(c2c,40,'eigenvector',0)
U4=update_rank_attack(c2c,40,'pagerank',0)
U5=update_rank_attack(c2c,40,'clustering',0)
#update list edge_betweenness
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
U6=update_rank_attack_edge(c2c,len(c2c.edges))


#attack static list rank
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
degree,eigen,closeness,betweenness,pagerank,clustering=measures(c2c)
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
rank_degree=ranking_nodes(degree)
R=set_rank_attack(c2c,rank_degree,40)
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
rank_eigen=ranking_nodes(eigen)
R1=set_rank_attack(c2c,rank_eigen,40)
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
rank_closeness=ranking_nodes(closeness)
R2=set_rank_attack(c2c,rank_closeness,40)
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
rank_bet=ranking_nodes(betweenness)
R3=set_rank_attack(c2c,rank_bet,40)
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
rank_pagerank=ranking_nodes(pagerank)
R4=set_rank_attack(c2c,rank_pagerank,40)
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
rank_cluster=ranking_nodes(clustering)
R5=set_rank_attack(c2c,rank_cluster,40)
#list edge_betweenness
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
edge_bet=list_edge_betweenness(c2c)
rank_edge_bet=ranking_nodes(edge_bet)
R6=set_rank_attack_edge(c2c,rank_edge_bet,len(c2c.edges))


#attacks sequence to random_vertex
attacks_rv=[]
for i in range(10):
    c2c = nx.read_gml("../data/graphs/net_c2c.gml")
    attacks_rv.append(random_vertex(c2c,60))

#random attack
Rn=random_neighbor(40)
Rv=random_vertex(nx.read_gml("../data/graphs/net_c2c.gml"),40)
Re=random_edge(nx.read_gml("../data/graphs/net_c2c.gml"),40)

c2c = nx.read_gml("../data/graphs/net_c2c.gml")
neighbor=nx.read_gml("../data/graphs/net_neighbor.gml")
x_d,y_d=degree_values(c2c.degree())
x_n,y_n=degree_values(neighbor.degree())
x_net,y_net=degree_values(net.degree())

#measures neighbor
nei_closeness=list_values(nx.closeness_centrality(neighbor))
nei_betweenness=list_values(nx.betweenness_centrality(neighbor, normalized=True))
nei_cluster=list_values(nx.clustering(neighbor))
nei_eigenvector=list_values(nx.eigenvector_centrality(neighbor))

#measures c2c
c2c_closeness=list_values(nx.closeness_centrality(c2c))
c2c_betweenness=list_values(nx.betweenness_centrality(c2c, normalized=True))
c2c_cluster=list_values(nx.clustering(c2c))
c2c_eigenvector=list_values(nx.eigenvector_centrality(c2c))

#measures net
net_closeness=list_values(nx.closeness_centrality(net))
net_betweenness=list_values(nx.betweenness_centrality(net, normalized=True))
net_cluster=list_values(nx.clustering(net))
net_eigenvector=list_values(nx.eigenvector_centrality_numpy(net))

#shortest path lenght and diameter
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
U,spl,diameter,spl_average,diameter_av =update_rank_attack(c2c,45,'closeness',1)
c2c = nx.read_gml("../data/graphs/net_c2c.gml")
E,e_spl,e_diameter,e_spl_average,e_diameter_av =update_rank_attack(c2c,45,'clustering',1)

external_stylesheets = [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://fonts.googleapis.com/css?family=Libre+Franklin&display=swap"
    
]

external_js = [
    "https://code.jquery.com/jquery-3.2.1.min.js",
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
]

app = dash.Dash(__name__, 
                external_scripts=external_js,
                external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = False

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #FF4500',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#FF7F50',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
        # Row: Title
        html.Div([
        # Col: Title
            html.Div([
                html.Div("Averaged graph analysis and failure resilience of a public transport network", className="text-center", style={"backgroundColor": "#FF7F50", "color": "#ffffff", "marginBottom": "none", "fontSize": "4.5rem", "fontWeight": "bold"})
            ], className="col-md-12 p-3"),
        ], className="row"),

        # Row: Tabs
        html.Div([
            # Col: Tabs
            html.Div([
                dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Introduction', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Averaged graphs', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Neighbor graph', value='tab-4', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Cell-to-cell flow graph', value='tab-5', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Graph comparison', value='tab-6', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Local centralities', value='tab-7', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Global centralities', value='tab-8', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Attacks', value='tab-9', style=tab_style, selected_style=tab_selected_style),
                ], style=tabs_styles, className = "m-auto"),
            ], className="col-md-12 text-center"),
        ], className="row"),


        # Row: Tabs content
        html.Div(id='tabs-content', className="row")
], className="container-fluid")


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == "tab-1":
        return html.Div([
                
                html.Div([
                    dcc.Markdown('''
                        ## Final project for the **Data Analytics** course for the MSc in Computer Science at University of Milano-Bicocca.
                        #### **Authors**: Nassim Habbash (808292), Ricardo Anibal Matamoros Aragon (807450)
                        ''', className="col-lg-11 text-center center", style={"flex-direction": "column", "marginTop":"10%"}),
                ], className="row center"),
                
            ], className = "container-fluid")
            
    elif tab == 'tab-3':
        # Averaged graphs
        return html.Div([
                html.Div([
                    html.Iframe(srcDoc=open('./maps/metro_map.html').read(), className="col-md-6 m-2"),
                    html.Iframe(srcDoc=open('./maps/metro_n_map.html').read(), className="col-md-6 m-2"),
                ], className="row"),

                html.Div([
                    dcc.Markdown('''
                        #### **Metro network**

                        Stops colored according to the line they belong to
                        
                        ''', className="col-md-6"),
                    dcc.Markdown('''
                        #### **Partitioned metro network**

                        Partitioned with the clustering algorithm with parameters gamma = 2km rho = 5km 
                        ''', className="col-md-6"),
                ], className="row text-center"),

            ], className = "container-fluid")

    elif tab == 'tab-4':
        # Neighbor map
        return html.Div([
                html.Div([
                    html.Iframe(srcDoc=open('./maps/vor_map.html').read(), className="col-md-6 m-2"),
                    html.Iframe(srcDoc=open('./maps/neigh_map.html').read(), className="col-md-6 m-2"),
                ], className="row"),

                html.Div([
                    dcc.Markdown('''
                        #### **Voronoi diagram**

                        Voronoi diagram of neighboring regions obtained from the whole network with gamma = 2km, rho = 5km
                        ''', className="col-md-6"),
                    dcc.Markdown('''
                        #### **Delaunay triangulation**

                        Graph of neighboring regions obtained from the whole network with gamma = 2km, rho = 5km
                        ''', className="col-md-6"),
                ], className="row text-center"),

            ], className = "container-fluid")

    elif tab == 'tab-5':
        # C2C flow graph
        return html.Div([
                html.Div([
                     dcc.Markdown('''
                        #### **Cell-to-cell flow graph of the public transport network**

                        Edge weights are colored and bigger according to their weight.
                        Weights represent the number of **direct** links between the stops in the regions.
                        ''', className="col-md-4", style={"marginTop":"10%"}),

                    html.Iframe(srcDoc=open('./maps/c2c_map.html').read(), className="col-md-8"),
                ], className="row center"),
            ], className = "container-fluid")

    elif tab == 'tab-6':
        # Graph comparison
        return html.Div([
                html.Div([
                    html.Iframe(srcDoc=open('./maps/neigh_c_map.html').read(), className="col-md-6 m-2"),
                    html.Iframe(srcDoc=open('./maps/c2c_c_map.html').read(), className="col-md-6 m-2"),
                ], className="row"),

                html.Div([
                    dcc.Markdown('''
                        #### **Centrality comparison**

                        Graphic point-to-point centrality comparison for the C2C and Neighbor graphs.
                        * Node size: *degree*
                        * Border color: *betweeness*
                        * Fill color: *closeness*
                        ''', className="col-md-6"),
                ], className="row center"),

            ], className = "container-fluid")

    elif tab =='tab-7':
        # Centrality distributions
        return html.Div([
            #html.H3("Centrality measures for the neighbor graph and C2C graph"),
            html.Div([
                html.Div([
                    html.H3('C2C degree distribution'),
                    dcc.Graph(id='c2c_degree', figure={'data': [{
                        'x': x_d,
                        'y': y_d,
                        'layout': {'height': 10},
                        'type': 'bar'}]})
                        
                ],
                className="col-md-3"),
                html.Div([
                    html.H3('neighbor degree distribution'),
                    dcc.Graph(id='nei_degree', 
                              figure={'data': [{
                                        'x': x_n,
                                        'y': y_n,
                                        'layout': {'height': 10},
                                        'type': 'bar'}]},
                              )
                        
                    ],
                className="col-md-3"),
                html.Div([
                    html.H3('net degree distribution'),
                    dcc.Graph(id='net_degree', 
                              figure={'data': [{
                                        'x': x_net,
                                        'y': y_net,
                                        'layout': {'height': 10},
                                        'type': 'bar'}]},
                              )
                        
                    ],
                className="col-md-3"),
                html.Div([
                    html.H3('Degree Distribution'),
                    html.H6('''This measure indicates the number of nodes directly connected to a given nodes, representing the capabilites of connecting a set of nodes directly.'''),
               
                ],
                className="col-md-3"),
                
       
            ], className="row"),
            html.Div([
               
                html.Div([
                    html.H3('C2C eigenvector distribution'),
                    dcc.Graph(id='c2c_eigen', figure={'data': [{
                     
                        'x': c2c_eigenvector,
                        'type': 'histogram'}]})
                      
                ],
                 className="col-md-3"),

                html.Div([
                    html.H3('neighbor eigenvector distribution'),
                    dcc.Graph(id='nei_eigen', figure={'data': [{
                        'x':nei_eigenvector,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],
            
                 className="col-md-3"),

                html.Div([
                    html.H3('net eigenvector distribution'),
                    dcc.Graph(id='net_eigen', figure={'data': [{
                        'x':net_eigenvector,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],
            
                 className="col-md-3"),
                html.Div([
                    html.H3('Eigenvector'),
                    html.H6('''This measure represents the importance of a certain
                                node compared to the nodes directly connected to it.
                                It does not factor in only direct influence, but also
                                the centrality of its neighbors.
                            '''),
               
                ],
                className="col-md-3"),
                
       
            ], className="row"),  
            html.Div([             
                html.Div([
                    html.H3('C2C clustering coefficient'),
                    dcc.Graph(id='c2c_clustering', figure={'data': [{
                     
                        'x': c2c_cluster,
                        'type': 'histogram'}]})
                      
                ],
                 className="col-md-3"),

                html.Div([
                    html.H3('neighbor coefficient clustering'),
                    dcc.Graph(id='nei_clustering', figure={'data': [{
                        'x':nei_cluster,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],
                 className="col-md-3"),
                html.Div([
                    html.H3('net coefficient clustering'),
                    dcc.Graph(id='net_clustering', figure={'data': [{
                        'x':net_cluster,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],
                 className="col-md-3"),
                html.Div([
                    html.H3('Clustering coefficient'),
                    html.H6('''This coefficient captures the degree by which 
                                neighbors of a certain node are connected to one 
                                another. It measures the density of
                                the local connection of a network,
                                higher the interconnection of the neighboring nodes
                                of a node and higher its local clustering coefficient is
                                gonna be.
                               '''),
               
                ],
                className="col-md-3"),
             ], className="row"), 
           ])

    elif tab =='tab-8':
        # Centrality distributions
        return html.Div([
            html.Div([               
                html.Div([
                    html.H3('C2C closeness'),
                    dcc.Graph(id='c2c_closeness', figure={'data': [{
                     
                        'x': c2c_closeness,
                        'type': 'histogram'}]})
                      
                ],
                 className="col-md-3"),

                html.Div([
                    html.H3('neighbor closeness'),
                    dcc.Graph(id='nei_closeness', figure={'data': [{
                        'x':nei_closeness,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],
                 className="col-md-3"),
                html.Div([
                    html.H3('net closeness'),
                    dcc.Graph(id='net_closeness', figure={'data': [{
                        'x':net_closeness,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],
                 className="col-md-3"),
                html.Div([
                    html.H3('Closeness'),
                    html.H6('''This measure represents the speed by which
                                a node is capable of transmitting information
                                and its capability to interact with other nodes in the network
                                given its position compared to the network's centrality.
                            '''),
               
                ],
                className="col-md-3"),         
      
            ], className="row"),
        html.Div([
            html.Div([
                    html.H3('C2C betweenness'),
                    dcc.Graph(id='c2c_bet', figure={'data': [{
                     
                        'x': c2c_betweenness,
                        'type': 'histogram'}]})
                      
                ],
                 className="col-md-3"),

                html.Div([
                    html.H3('neighbor betweenness'),
                    dcc.Graph(id='nei_betweenness', figure={'data': [{
                        'x':nei_betweenness,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],
                 className="col-md-3"),
                 html.Div([
                    html.H3('net betweenness'),
                    dcc.Graph(id='net_betweenness', figure={'data': [{
                        'x':net_betweenness,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],
                 className="col-md-3"),
                html.Div([
                    html.H3('Betweenness'),
                    html.H6('''This measure represents the importance
                                of a node in respect to the times it is 
                                used as a bridge between couples of nodes.
                                The higher its value the more control the node
                                has on different clusters of the network'''),
               
                ],
                className="col-md-3"),
             ], className="row"),
        ])
            
                
    elif tab == 'tab-9':
        # Attacks
        return html.Div([
            #html.H1('ATTACKS'),
            html.Div([
                    html.H3('Random Neighbor'),
                    dcc.Graph(id='rn', figure={'data': [{
                        'x':range(1,100),
                        'y':Rn,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}],'layout':{
                         #'title':'Basic non interactive',
                         'xaxis':{
                         'title':'percents of removed nodes'
                          },
                          'yaxis':{
                          'title':'normalized size S to GCC'
                          }
            }})
                ],
                 className="col-md-6"),
            html.Div([
                    html.H3('Random Vertex'),
                    dcc.Graph(id='rv', figure={'data': [{
                        'x':range(1,100),
                        'y':Rv,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}],'layout':{
                         #'title':'Basic non interactive',
                         'xaxis':{
                         'title':'percents of removed nodes'
                          },
                          'yaxis':{
                          'title':'normalized size S to GCC'
                          }
            }})
                ],
                 className="col-md-6"),
            html.Div([
                    html.H3('Random edge'),
                    dcc.Graph(id='re', figure={'data': [{
                        'x':range(1,100),
                        'y':Re,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}],'layout':{
                         #'title':'Basic non interactive',
                         'xaxis':{
                         'title':'percents of removed nodes'
                          },
                          'yaxis':{
                          'title':'normalized size S to GCC'
                          }
            }})
                ],
                 className="col-md-6"),
            html.Div([
                    html.H3('sequence random vertex attack'),
                    dcc.Graph(id='attack_sequence', figure={'data': [{
                        'x':range(1,100),
                        'y':attacks_rv[0],
                        'name': 'attack1',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':attacks_rv[1],
                        'name': 'attack2',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':attacks_rv[2],
                        'name': 'attack3',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                        {
                        'x':range(1,100),
                        'y':attacks_rv[3],
                        'name': 'attack4',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines+markers'}, 
                        {
                        'x':range(1,100),
                        'y':attacks_rv[4],
                        'name': 'attack5',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':attacks_rv[5],
                        'name': 'attack6',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':attacks_rv[6],
                        'name': 'attack7',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':attacks_rv[7],
                        'name': 'attack8',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}, 
                        {
                        'x':range(1,100),
                        'y':attacks_rv[8],
                        'name': 'attack9',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}, 
                        {
                        'x':range(1,100),
                        'y':attacks_rv[9],
                        'name': 'attack10',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},  
                          ],'layout':{
                         #'title':'Basic non interactive',
                         'xaxis':{
                         'title':'percents of removed nodes'
                          },
                          'yaxis':{
                          'title':'normalized size S to GCC'
                          }
            }})
                ],
                 className="col-md-6"),
            html.Div([
                    html.H3('attack update list measures'),
                    dcc.Graph(id='attack', figure={'data': [{
                        'x':range(1,100),
                        'y':U,
                        'name': 'degree',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':U1,
                        'name': 'closeness',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':U2,
                        'name': 'betweenness',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                        {
                        'x':range(1,100),
                        'y':U3,
                        'name': 'eignvector',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines+markers'}, 
                        {
                        'x':range(1,100),
                        'y':U4,
                        'name': 'pagerank',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':U5,
                        'name': 'clustering coefficient',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':U6,
                        'name': 'edge_betweenness',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}, 
                          ],'layout':{
                         #'title':'Basic non interactive',
                         'xaxis':{
                         'title':'percents of removed nodes'
                          },
                          'yaxis':{
                          'title':'normalized size S to GCC'
                          }
            }})
                ],
                 className="col-md-6"),
             html.Div([
                    html.H3('attack static list measures'),
                    dcc.Graph(id='attack_static', figure={'data': [{
                        'x':range(1,100),
                        'y':R,
                        'name': 'degree',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':R2,
                        'name': 'closeness',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':R3,
                        'name': 'betweenness',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                        {
                        'x':range(1,100),
                        'y':R1,
                        'name': 'eignvector',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines+markers'}, 
                        {
                        'x':range(1,100),
                        'y':R4,
                        'name': 'pagerank',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':R5,
                        'name': 'clustering coefficient',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                         {
                        'x':range(1,100),
                        'y':R6,
                        'name': 'edge_betweenness',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}, 
                          ],'layout':{
                         #'title':'Basic non interactive',
                         'xaxis':{
                         'title':'percents of removed nodes'
                          },
                          'yaxis':{
                          'title':'normalized size S to GCC'
                          }
            }})
                ],
                 className="col-md-6"),
            html.Div([
                    html.H3('Diameter and Shortest path length based to closeness'),
                    dcc.Graph(id='d_spl', figure={'data': [{
                        'x':range(1,100),
                        'y':spl,
                        'name': 'average_shortest_path_gcc',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                        {
                        'x':range(1,100),
                        'y':diameter,
                        'name': 'diameter_gcc',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}
                         ],'layout':{
                         #'title':'Basic non interactive',
                         'xaxis':{
                         'title':'percents of removed nodes'
                          },
                          'yaxis':{
                          'title':"measure's values"
                          }
            }})
                ],
                 className="col-md-6"),

            html.Div([
                    html.H3('Diameter and Shortest path length based to clustering coefficient'),
                    dcc.Graph(id='cc_spl', figure={'data': [{
                        'x':range(1,100),
                        'y':e_spl,
                        'name': 'average_shortest_path_gcc',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'},
                        {
                        'x':range(1,100),
                        'y':e_diameter,
                        'name': 'diameter_gcc',
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}
                         ],'layout':{
                         #'title':'Basic non interactive',
                         'xaxis':{
                         'title':'percents of removed nodes'
                          },
                          'yaxis':{
                          'title':"measure's values"
                          }
            }})
                ],
                 className="col-md-6"),
        ])

if __name__ == '__main__':
    app.run_server(debug=True)

