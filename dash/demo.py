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
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from attacks import *

def read_data(name):
    with open(name, "r") as f:
        test=[float(i) for line in f for i in line.split(',')]
    return test


G = nx.read_gml("../data/graphs/net_c2c.gml")
def d_d_matrix(G):
    #contiene la distribuzione di degree
    degree_distribution={}
    for i in list(G.degree()):
        degree_distribution[i[1]]=[]
    for i in list(G.degree()):
        degree_distribution[i[1]].append(int(i[0]))

    #contiene i vicini per ogni nodo
    node_neighbor={}
    for i in list(G.nodes):
        node_neighbor[int(i)]=map(int,list(G.neighbors(i)))

    #contiene il valore di degree per ogni vicino di ogni nodo
    neighbor_degree={}
    for node in node_neighbor.keys():
        tmp=[]
        for neighbor in node_neighbor[node]:
            tmp.append(G.degree(str(neighbor)))
        neighbor_degree[node]=tmp

    n=len(degree_distribution.keys())
    degree_degree = np.zeros((n, n))

    for i in degree_distribution.keys():
        for j in degree_distribution[i]:
            for x in neighbor_degree[j]:
                degree_degree[i-1][x-1]+=1
    return degree_degree

def degree_correlation_matrix(matrix):
    avg=np.sum(matrix)/len(matrix)
    return np.divide(matrix,avg)

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

#U=update_rank_attack(c2c,40,'degree',0)
U=read_data("./data_plots/degree_u.txt")
U1=read_data("./data_plots/closeness_u.txt")
U2=read_data("./data_plots/bet_u.txt")
U3=read_data("./data_plots/eig_u.txt")
U4=read_data("./data_plots/pg_u.txt")
U5=read_data("./data_plots/clu_u.txt")
U6=read_data("./data_plots/edbe_u.txt")

#attack static list rank
R=read_data("./data_plots/degree_r.txt")
R1=read_data("./data_plots/eig_r.txt")
R2=read_data("./data_plots/clos_r.txt")
R3=read_data("./data_plots/bet_r.txt")
R4=read_data("./data_plots/pg_r.txt")
R5=read_data("./data_plots/clu_r.txt")
R6=read_data("./data_plots/edbe_r.txt")

#attacks sequence to random_vertex
attacks_rv=[]
for i in range(10):
    c2c = nx.read_gml("../data/graphs/net_c2c.gml")
    attacks_rv.append(random_vertex(c2c,60))

#random attack
Rn=read_data("./data_plots/rn.txt")
Rv=read_data("./data_plots/rv.txt")
Re=read_data("./data_plots/re.txt")

c2c = nx.read_gml("../data/graphs/net_c2c.gml")
neighbor=nx.read_gml("../data/graphs/net_neighbor.gml")
x_d,y_d=degree_values(c2c.degree())
x_n,y_n=degree_values(neighbor.degree())
x_net,y_net=degree_values(net.degree())

#measures neighbor
nei_closeness=read_data("./data_plots/nei_clo.txt")
nei_betweenness=read_data("./data_plots/nei_bet.txt")
nei_cluster=read_data("./data_plots/nei_clu.txt")
nei_eigenvector=read_data("./data_plots/nei_eig.txt")

#measures c2c
c2c_closeness=read_data("./data_plots/c2c_clo.txt")
c2c_betweenness=read_data("./data_plots/c2c_bet.txt")
c2c_cluster=read_data("./data_plots/c2c_clu.txt")
c2c_eigenvector=read_data("./data_plots/c2c_eig.txt")

#measures net
net_closeness=read_data("./data_plots/net_clo.txt")
net_betweenness=read_data("./data_plots/net_bet.txt")
net_cluster=read_data("./data_plots/net_clu.txt")
net_eigenvector=read_data("./data_plots/net_eig.txt")

#shortest path lenght and diameter
spl=read_data("./data_plots/spl.txt")
diameter=read_data("./data_plots/diameter.txt")
e_spl=read_data("./data_plots/e_spl.txt")
e_diameter=read_data("./data_plots/e_diameter.txt")

#matrix correlation degree
cc_c2c=degree_correlation_matrix(d_d_matrix(G)).tolist()
cc_neighbor=degree_correlation_matrix(d_d_matrix(nx.read_gml("../data/graphs/net_neighbor.gml")))
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
server = app.server

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
                    dcc.Tab(label='Averaged graphs', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Neighbor graph', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Cell-to-cell flow graph', value='tab-4', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Comparison', value='tab-5', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Attacks', value='tab-6', style=tab_style, selected_style=tab_selected_style),
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
            
    elif tab == 'tab-2':
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

    elif tab == 'tab-3':
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

    elif tab == 'tab-4':
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

    elif tab == 'tab-5':
        # Graph comparison
        return html.Div([
                dcc.Tabs(vertical=True, style=tabs_styles, id="tabs-comparison", children=[
                    dcc.Tab(style=tab_style, selected_style=tab_selected_style, label='General measures', children=[
                        html.Div([
                            html.Div([
                                dcc.Markdown('''
                                    |                | Vertices | Edges | Density |
                                    |----------------|----------|-------|---------|
                                    | Original graph | '''+ str(nx.number_of_nodes(net)) +'''| '''+ str(nx.number_of_edges(net)) +''' | '''+ str(nx.density(net)) +'''   |
                                    | Neighbor graph | '''+ str(nx.number_of_nodes(neighbor)) +'''| '''+ str(nx.number_of_edges(neighbor)) +''' | '''+ str(nx.density(neighbor)) +'''   ||
                                    | C2C graph      | '''+ str(nx.number_of_nodes(c2c)) +''' | '''+ str(nx.number_of_edges(c2c)) +''' | '''+ str(nx.density(c2c)) +'''   ||

                                    ''', className="col-md-6"),
                            ], className="row center"),
                        ], className = "container-fluid", style={"width": "100%"})
                    ]),
                    dcc.Tab(style=tab_style, selected_style=tab_selected_style, label='Local centralities', children=[
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.H3('C2C Graph'),
                                ],
                                className="col-md-3"),
                                html.Div([
                                    html.H3('Neighbor Graph'),],
                                className="col-md-3"),
                                html.Div([
                                    html.H3('Original Graph'),
                                    ],
                                className="col-md-3"),
                                html.Div([
                                    html.H3('Measure description'),
                                ],
                                className="col-md-3"),
                            ], className="row"),
                            html.Div([
                                html.Div([
                                    dcc.Graph(id='c2c_degree', figure={'data': [{
                                        'x': x_d,
                                        'y': y_d,
                                        'layout': {'height': 10},
                                        'type': 'bar'}]})
                                ],
                                className="col-md-3"),
                                html.Div([
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
                                    html.H3('Degree'),
                                    html.H6('''This measure indicates the number of nodes directly connected to a given nodes, representing the capabilites of connecting a set of nodes directly.'''),
                            
                                ],
                                className="col-md-3"),
                                
                    
                            ], className="row"),
                            html.Div([
                                html.Div([
                                    dcc.Graph(id='c2c_eigen', figure={'data': [{
                                    
                                        'x': c2c_eigenvector,
                                        'type': 'histogram'}]})
                                    
                                ],
                                className="col-md-3"),

                                html.Div([
                                    dcc.Graph(id='nei_eigen', figure={'data': [{
                                        'x':nei_eigenvector,
                                        'layout': {'height': '50', 'width' : '50'},
                                        'type': 'histogram'}]})
                                ],
                            
                                className="col-md-3"),
                                
                                html.Div([
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
                                    dcc.Graph(id='c2c_clustering', figure={'data': [{
                                        'x': c2c_cluster,
                                        'type': 'histogram'}]})
                                    
                                ],
                                className="col-md-3"),

                                html.Div([
                                    dcc.Graph(id='nei_clustering', figure={'data': [{
                                        'x':nei_cluster,
                                        'layout': {'height': '50', 'width' : '50'},
                                        'type': 'histogram'}]})
                                ],
                                
                                className="col-md-3"),
                                
                                html.Div([
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
                        ], className="container-fluid")
                    ]),
                    dcc.Tab(style=tab_style, selected_style=tab_selected_style, label='Global centralities', children=[
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.H3('C2C Graph'),
                                    ],
                                    className="col-md-3"),
                                    html.Div([
                                        html.H3('Neighbor Graph'),],
                                    className="col-md-3"),
                                    html.Div([
                                        html.H3('Original Graph'),
                                        ],
                                    className="col-md-3"),
                                    html.Div([
                                        html.H3('Measure description'),
                                    ],
                                    className="col-md-3"),
                                ], className="row"),
                                
                                html.Div([               
                                    html.Div([
                                        dcc.Graph(id='c2c_closeness', figure={'data': [{
                                        
                                            'x': c2c_closeness,
                                            'type': 'histogram'}]})
                                        
                                    ],
                                    className="col-md-3"),

                                    html.Div([
                                        dcc.Graph(id='nei_closeness', figure={'data': [{
                                            'x':nei_closeness,
                                            'layout': {'height': '50', 'width' : '50'},
                                            'type': 'histogram'}]})
                                    ],
                                    
                                    className="col-md-3"),
                                
                                    html.Div([
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
                                        dcc.Graph(id='c2c_bet', figure={'data': [{
                                        
                                            'x': c2c_betweenness,
                                            'type': 'histogram'}]})
                                        
                                    ],
                                    className="col-md-3"),

                                    html.Div([
                                        dcc.Graph(id='nei_betweenness', figure={'data': [{
                                            'x':nei_betweenness,
                                            'layout': {'height': '50', 'width' : '50'},
                                            'type': 'histogram'}]})
                                    ],
                                    
                                    className="col-md-3"),
                                    
                                    html.Div([
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
                    ]),
                    dcc.Tab(style=tab_style, selected_style=tab_selected_style, label='Node-to-node comparison', children=[
                        html.Div([
                            html.Div([
                                html.Iframe(srcDoc=open('./maps/neigh_c_map.html').read(), className="col-md-6 m-2"),
                                html.Iframe(srcDoc=open('./maps/c2c_c_map.html').read(), className="col-md-6 m-2"),
                            ], className="row"),

                            html.Div([
                                dcc.Markdown('''
                                    #### **Centrality comparison**

                                    Graphic point-to-point centrality comparison for the Neighbor graph (left) and C2C graph (right).
                                    * Node size: *degree*
                                    * Border color: *betweeness*
                                    * Fill color: *closeness*
                                    ''', className="col-md-6"),
                            ], className="row center"),

                        ], className = "container-fluid", style={"width": "100%"})
                    ]),
                    dcc.Tab(style=tab_style, selected_style=tab_selected_style, label='Assortativity', children=[
                        html.Div([
                            html.Div([
                                    html.Div([
                                        html.H3('C2C Graph'),
                                        ], className="col-md-6"),
                                    html.Div([
                                        html.H3('Neighbor Graph'),
                                    ], className="col-md-6"),
                                ], className="row"), 

                            html.Div([
                                    html.Div([
                                        html.H4('Degree Assortativity Coefficient: '+str(round(nx.degree_assortativity_coefficient(G, weight='weight'),2))),
                                        html.H4('Degree-Correlation Matrix: '),
                                        dcc.Graph( id = "heatmap", figure = go.Figure( data = [go.Heatmap(z=cc_c2c)] ) )
                                        ], className="col-md-6"),
                                    html.Div([
                                        html.H4('Degree Assortativity Coefficient: '+str(round(nx.degree_assortativity_coefficient(neighbor, weight='weight'),2))),
                                        html.H4('Degree-Correlation Matrix: '),
                                        dcc.Graph( id = "heatmap2", figure = go.Figure( data = [go.Heatmap(z=cc_neighbor)] ) )
                                    ], className="col-md-6"),
                                ], className="row"), 
                        ])
                    ]),
            ], className="col-md-2")
        ])
                
    elif tab == 'tab-6':
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
                          'title':'normalized size S of GCC'
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
                          'title':'normalized size S of GCC'
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
                          'title':'normalized size S of GCC'
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
                          'title':'normalized size S of GCC'
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
                          'title':'normalized size S of GCC'
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
                          'title':'normalized size S of GCC'
                          }
            }})
                ],
                 className="col-md-6"),
            html.Div([
                    html.H3('Diameter and average shortest path length based on the updated closeness scenario'),
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
                    html.H3('Diameter and average shortest path length based on the updated clustering scenario'),
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

