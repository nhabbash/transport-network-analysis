import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import networkx as nx

import dash_table_experiments as dt
import folium
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

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

c2c = nx.read_gml("./data/graphs/net_c2c.gml")
neighbor=nx.read_gml("./data/graphs/net_neighbor.gml")

#misure da plottare
nei_diam=nx.diameter(neighbor)
nei_avg_clus=nx.average_clustering(neighbor)
nei_avg_short=nx.average_shortest_path_length(neighbor)
c2c_diam=nx.diameter(c2c)
c2c_avg_clus=nx.average_clustering(c2c)
c2c_avg_short=nx.average_shortest_path_length(c2c)

#misure plottare
x_d,y_d=degree_values(c2c.degree())
x_n,y_n=degree_values(neighbor.degree())

nei_closeness=list_values(nx.closeness_centrality(neighbor))
nei_betweenness=list_values(nx.betweenness_centrality(neighbor, normalized=True))
nei_cluster=list_values(nx.clustering(neighbor))
nei_eigenvector=list_values(nx.eigenvector_centrality(neighbor))

c2c_closeness=list_values(nx.closeness_centrality(c2c))
c2c_betweenness=list_values(nx.betweenness_centrality(c2c, normalized=True))
c2c_cluster=list_values(nx.clustering(c2c))
c2c_eigenvector=list_values(nx.eigenvector_centrality(c2c))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('TRANSPORTATION NETWORK ANALYSIS'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Introduction', value='tab-1-example'),
        dcc.Tab(label='description data', value='tab-2-example'),
        dcc.Tab(label='Data Managament', value='tab-3-example'),
        dcc.Tab(label='MultiLayer Graphs', value='tab-4-example'),
        dcc.Tab(label='Metro Graph', value='tab-5-example'),
        dcc.Tab(label='Metro Network Analysis', value='tab-6-example'),
        dcc.Tab(label='Delaunay & Boronoy', value='tab-7-example'),
        dcc.Tab(label='Delaunay & C2C graph ', value='tab-8-example'),
        dcc.Tab(label='centrality measures', value='tab-9-example'),
    ]),

    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.H2('Data Analytics 2018-2019'),
            html.H3('Ricardo Anibal Matamoros Aragon, 807450'),
            html.H3('Nassim Habbash, 808292'),
            html.H3('Universita degli Studi di Milano-Bicocca'),
            
        ])
    elif tab =='tab-9-example':
        return html.Div([
            html.H3("misure di centralita per C2C e neighbor graph"),
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
                    html.H3('Description Degree Distribution'),
                    html.H6('''Questa misura di centralita indica il
                               numero di nodi che possono essere
                               raggiunte direttamente da un determinato
                               nodo, quindi la capacita di connettere
                               un insieme di nodi in modo diretto.'''),
               
                ],style={"height" : "25%", "width" : "25%"},
                className="six columns"),
                
       
            ], className="row"),
            html.Div([
               
                html.Div([
                    html.H3('c2c eigenvector'),
                    dcc.Graph(id='c2c_eigen', figure={'data': [{
                     
                        'x': c2c_eigenvector,
                        'type': 'histogram'}]})
                      
                ],style={"height" : "25%", "width" : "25%"},
                 className="six columns"),

                html.Div([
                    html.H3('neighbor eigenvector'),
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
            

      
    elif tab == 'tab-7-example':
        return html.Div([
            html.H3('Milano'),
            html.Iframe(id ='m',srcDoc= open('./dash/primo_plot.html').read(),height='900',width='100%')
        ])
    elif tab == 'tab-8-example':
        return html.Div([
            html.Div([
            
            html.Iframe(id ='m',srcDoc= open('./dash/secondo_plot.html').read(), style={'width': '49.5%', 'display': 'inline-block', 'margin-bottom': '20px'},height='900'),
           
            html.Iframe(id ='map',srcDoc= open('./dash/terzo_plot.html').read(),style={'width': '50%', 'display': 'inline-block', 'margin-bottom': '20px'},height='900'),
             
            ]),
      
        ])     
        
    elif tab == 'tab-2-example':
        return html.Div([
            dcc.Markdown('''
            #### Dash and Markdown

            Dash supports [Markdown](http://commonmark.org/help).

            Markdown is a simple way to write and format text.
            It includes a syntax for things like **bold text** and *italics*,
            [links](http://commonmark.org/help), inline `code` snippets, lists,
            quotes, and more.
            ''')
        ])
    elif tab == 'tab-6-example':
        return html.Div([
            html.H3('degree'),
            
        ])
      
if __name__ == '__main__':
    app.run_server(debug=True)

