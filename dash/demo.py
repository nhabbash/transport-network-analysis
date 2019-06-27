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
from attacks import random_vertex, update_rank_attack

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

def random_neighbor(dimension):
    G = nx.read_gml("../data/graphs/net_c2c.gml")
    N=nx.number_of_nodes(G)
    S=[100]
    #esegue gli attacchi
    for i in range(dimension):
        node=int(random.choice(list(G.nodes)))
        neighbor=int(random.choice(list(G.neighbors(str(node)))))
        G.remove_node(str(neighbor))
        #prende max componente connessa
        G = max(nx.connected_component_subgraphs(G), key=len)
        S.append((float(nx.number_of_nodes(G))/N)*100)
        if len(G.nodes) ==1:
            return S
    
    return S 

c2c = nx.read_gml("../data/graphs/net_c2c.gml")

U=update_rank_attack(c2c,40,'degree',0)
U1=update_rank_attack(c2c,40,'closeness',0)
U2=update_rank_attack(c2c,40,'betweenness',0)
U3=update_rank_attack(c2c,40,'eigenvector',0)
U4=update_rank_attack(c2c,40,'pagerank',0)
U5=update_rank_attack(c2c,40,'clustering',0)

Rn=random_neighbor(40)
Rv=random_vertex(nx.read_gml("../data/graphs/net_c2c.gml"),40)

c2c = nx.read_gml("../data/graphs/net_c2c.gml")
neighbor=nx.read_gml("../data/graphs/net_neighbor.gml")
x_d,y_d=degree_values(c2c.degree())
x_n,y_n=degree_values(neighbor.degree())

nei_closeness=list(nx.closeness_centrality(neighbor))
nei_betweenness=list(nx.betweenness_centrality(neighbor, normalized=True))
nei_cluster=list(nx.clustering(neighbor))
nei_eigenvector=list(nx.eigenvector_centrality(neighbor))

c2c_closeness=list(nx.closeness_centrality(c2c))
c2c_betweenness=list(nx.betweenness_centrality(c2c, normalized=True))
c2c_cluster=list(nx.clustering(c2c))
c2c_eigenvector=list(nx.eigenvector_centrality(c2c))


external_stylesheets = [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    
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
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
        # Row: Title
        html.Div([
        # Col: Title
            html.Div([
                html.H1("Averaged graph analysis and failure resilience of a public transport network", className="text-center")
            ], className="col-md-12 p-3"),
        ], className="row"),

        # Row: Tabs
        html.Div([
            # Col: Tabs
            html.Div([
                dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Introduction', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Data managament', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Averaged graphs', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Neighbor graph', value='tab-4', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Cell-to-cell flow graph', value='tab-5', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Graph comparison', value='tab-6', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Centrality distributions', value='tab-7', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Attacks', value='tab-8', style=tab_style, selected_style=tab_selected_style),
                ], style=tabs_styles, className = "m-auto"),
            ], className="col-md-12 text-center"),
        ], className="row"),


        # Row: Tabs content
        html.Div(id='tabs-content', className="row")
], className="container-fluid")


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        # Intro
        return html.Div([

                html.Div([
                    dcc.Markdown('''
                        #### Desc

                        Desc
                        ''', className="col"),

                ], className="row"),

            ], className = "container")

        return html.Div([
            html.H2('Averaged graph analysis and failure resilience of a public transport network'),
            html.H3('Final project for the Data Analytics course for the MSc in Computer Science at University of Milano-Bicocca.'),
            html.H5('Authors: Nassim Habbash (808292), Ricardo Anibal Matamoros Aragon (807450)'),
        ])
    elif tab == 'tab-2':
        # Data management
        return html.Div([

        ]) 
            
    elif tab == 'tab-3':
        # Averaged graphs
        return html.Div([
                html.Div([
                    html.Iframe(srcDoc=open('./maps/metro_map.html').read(), className="col-md-6 m-2"),
                    html.Iframe(srcDoc=open('./maps/metro_n_map.html').read(), className="col-md-6 m-2"),
                ], className="row"),

                html.Div([
                    dcc.Markdown('''
                        #### Desc

                        Desc
                        ''', className="col-md-6"),
                    dcc.Markdown('''
                        #### Desc

                        Desc
                        ''', className="col-md-6"),
                ], className="row"),

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
                        #### Desc

                        Desc
                        ''', className="col-md-6"),
                    dcc.Markdown('''
                        #### Desc

                        Desc
                        ''', className="col-md-6"),
                ], className="row"),

            ], className = "container-fluid")

    elif tab == 'tab-5':
        # C2C flow graph
        return html.Div([
                html.Div([
                     dcc.Markdown('''
                        #### Desc

                        Desc
                        ''', className="col-md-4"),

                    html.Iframe(srcDoc=open('./maps/c2c_map.html').read(), className="col-md-8"),
                ], className="row center-row"),
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
                        #### Desc

                        Desc
                        ''', className="col-md-6"),
                ], className="row center-row"),

            ], className = "container-fluid")

    elif tab =='tab-7':
        # Centrality distributions
        return html.Div([
            html.H3("Centrality measures for the neighbor graph and C2C graph"),
            html.Div([
                html.Div([
                    html.H3('C2C degree distribution'),
                    dcc.Graph(id='c2c_degree', figure={'data': [{
                        'x': x_d,
                        'y': y_d,
                        'layout': {'height': 10},
                        'type': 'bar'}]})
                        
                ],style={"height" : "25%", "width" : "25%"},
                className="six columns"),
                html.Div([
                    html.H3('neighbor degree distribution'),
                    dcc.Graph(id='nei_degree', figure={'data': [{
                        'x': x_n,
                        'y': y_n,
                        'layout': {'height': 10},
                        'type': 'bar'}]})
                        
                ],style={"height" : "25%", "width" : "25%"},
                className="six columns"),
                html.Div([
                    html.H3('Degree Distribution'),
                    html.H6('''This measure indicates the number of nodes directly connected to a given nodes, 
                            representing the capabilites of connecting a set of nodes directly.'''),
               
                ],style={"height" : "25%", "width" : "25%"},
                className="six columns"),
                
       
            ], className="row"),
            html.Div([
               
                html.Div([
                    html.H3('C2C eigenvector distribution'),
                    dcc.Graph(id='c2c_eigen', figure={'data': [{
                     
                        'x': c2c_eigenvector,
                        'type': 'histogram'}]})
                      
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),

                html.Div([
                    html.H3('neighbor eigenvector distribution'),
                    dcc.Graph(id='nei_eigen', figure={'data': [{
                        'x':nei_eigenvector,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),
                html.Div([
                    html.H3('Description eigenvector'),
                    html.H6('''Questa misura indica l'importanza di un
                               determinato nodo rispetto ai nodi che lo
                               raggiungono direttamente.
                               E' utile perche indica non solo l'influenza
                               diretta, ma anche in base alla centralita dei
                               suoi vicini.'''),
               
                ],style={"height" : "25%", "width" : "25%"},
                className="six columns"),
                
       
            ], className="row"),
            html.Div([
               
                html.Div([
                    html.H3('c2c coefficient clustering'),
                    dcc.Graph(id='c2c_clustering', figure={'data': [{
                     
                        'x': c2c_cluster,
                        'type': 'histogram'}]})
                      
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),

                html.Div([
                    html.H3('neighbor coefficient clustering'),
                    dcc.Graph(id='nei_clustering', figure={'data': [{
                        'x':nei_cluster,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),
                html.Div([
                    html.H3('Description coefficient clustering'),
                    html.H6('''Questo coefficiente cattura il grado
                               con cui i vicini di un determinato nodo
                               si collegano l'un all'altro.
                               Dunque misura la densita di collegamento
                               locale della rete, quanto maggiore e'
                               l'interconnessione dei nodi vicini a un nodo,
                               piu alto e' il suo coefficiente di Clustering locale.'''),
               
                ],style={"height" : "25%", "width" : "25%"},
                className="six columns"),
                
       
            ], className="row"),
            html.Div([
               
                html.Div([
                    html.H3('c2c closeness'),
                    dcc.Graph(id='c2c_closeness', figure={'data': [{
                     
                        'x': c2c_closeness,
                        'type': 'histogram'}]})
                      
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),

                html.Div([
                    html.H3('neighbor closeness'),
                    dcc.Graph(id='nei_closeness', figure={'data': [{
                        'x':nei_closeness,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),
                html.Div([
                    html.H3('Description closeness'),
                    html.H6('''Questa misura indica la velocita con la
                               quale un nodo riesce a trasmettere
                               certa informazione, e la capacita di interagire 
                               con altri nodi nella rete data la sua posizione 
                               rispetto alla centralita della rete.'''),
               
                ],style={"height" : "25%", "width" : "25%"},
                className="six columns"),
                
       
            ], className="row"),
            html.Div([
               
                html.Div([
                    html.H3('c2c betweenness'),
                    dcc.Graph(id='c2c_bet', figure={'data': [{
                     
                        'x': c2c_betweenness,
                        'type': 'histogram'}]})
                      
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),

                html.Div([
                    html.H3('neighbor betweenness'),
                    dcc.Graph(id='nei_betweenness', figure={'data': [{
                        'x':nei_betweenness,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'histogram'}]})
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),
                html.Div([
                    html.H3('Description betweenness'),
                    html.H6('''Questa misura indica l'importanza di un
                               nodo rispetto alle volte nelle quali
                               viene utilizzato come ponte da altre
                               coppie di nodi, quindi maggiore sara' il
                               valore associato e maggiore sara' la
                               quantita' di informazione a disposizione.'''),
               
                ],style={"height" : "25%", "width" : "25%"},
                className="six columns"),
                
       
            ], className="row"),
                  
           ])
    elif tab == 'tab-8':
        # Attacks
        return html.Div([
            html.H1('ATTACKS'),
            html.Div([
                    html.H3('attack random neighbor'),
                    dcc.Graph(id='rn', figure={'data': [{
                        'x':range(1,100),
                        'y':Rn,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}]})
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),
            html.Div([
                    html.H3('attack random vertex'),
                    dcc.Graph(id='rv', figure={'data': [{
                        'x':range(1,100),
                        'y':Rv,
                        'layout': {'height': '50', 'width' : '50'},
                        'type': 'lines'}]})
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),
            html.Div([
                    html.H3('attack update measures'),
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
                        'type': 'lines'} 
                          ]})
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),
            
        ])
    elif tab =="tab-9":
         return html.Div([
            html.H1('metro net analysis'),
            dcc.Slider(
                min=0,
                max=9,
                marks={i: 'Label {}'.format(i) for i in range(10)},
                value=5,
            ) 
        ])

      
if __name__ == '__main__':
    app.run_server(debug=True)

