"""
@author: Bobak Kechavarzi (bdkech)
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Data loading
SHAP_DAT = pandas.read_csv(open("data/staging/all_shap_melt_mod_log.txt", 'r'),
                           sep="\t")
FLD_CHNG_DAT = pandas.read_csv(open("data/staging/all_fld_chng_melt.txt", 'r'),
                           sep="\t")
CORR = pandas.read_csv(open("data/staging/correlations.txt", 'r'),
                           sep="\t")
def get_gene_ids():
    return sorted(list(CORR['hgnc_symbol'].unique()))

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
                dcc.Dropdown(id='input-1',
                    options = [{'label': i, 'value': i} for i in get_gene_ids()],
                    value='Select gene'
                ),
                html.Hr(),

                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(id='graph1')
                        ],className='twelve columns'),

                        html.Div([
                            dcc.Graph(id='graph2')
                        ],className='twelve columns'),

                        html.Div([
                            dcc.Graph(id='graph3')
                        ],className='twelve columns')
                    ], className='six columns'),
                    html.Div([
                        html.Iframe(id='i_frame_1', src='',
                            style={
                                'height': '100vh',
                                'width': '100%'}),
                    ], className='six columns')
                ], className='row'),
        ])
@app.callback(
        Output('i_frame_1', 'src'),
        [Input('input-1', 'value')])
def update_iframe(gene_id):
    search_string = "https://www.ncbi.nlm.nih.gov/gene/?term={}"
    return search_string.format(gene_id)

@app.callback(
        Output('graph1','figure'),
        [Input('input-1', 'value')])
def update_graph(gene_id):
    dat_brca = FLD_CHNG_DAT[(FLD_CHNG_DAT['variable'] == gene_id) & (FLD_CHNG_DAT['histology'] == 'BRCA')]
    dat_ov = FLD_CHNG_DAT[(FLD_CHNG_DAT['variable'] == gene_id) & (FLD_CHNG_DAT['histology'] == 'OV')]
    trace = {'x': dat_brca['type'].values, 'y': dat_brca['value'].values,
            'type':'violin', 'name': 'BRCA'}
    trace2 = {'x': dat_ov['type'].values, 'y': dat_ov['value'].values,
            'type':'violin', 'name': 'OV'}

    #trace = go.Box(y=dat['value'].values, x=dat['type'].values)
    data = [trace, trace2]
    return {
            'data': data,
            'layout': go.Layout(
                        xaxis = {'title': 'Data Type'},
                        yaxis = {'title': 'Log2 fold change'}
                )
            }
@app.callback(
        Output('graph2','figure'),
        [Input('input-1', 'value')])
def update_graph(gene_id):
    dat_brca = SHAP_DAT[(SHAP_DAT['variable'] == gene_id) & (SHAP_DAT['histology'] == 'BRCA')]
    dat_ov = SHAP_DAT[(SHAP_DAT['variable'] == gene_id) & (SHAP_DAT['histology'] == 'OV')]
    trace = {'x': dat_brca['type'].values, 'y': dat_brca['value'].values,
            'type':'violin', 'name': 'BRCA'}
    trace2 = {'x': dat_ov['type'].values, 'y': dat_ov['value'].values,
            'type':'violin', 'name': 'OV'}

    #trace = go.Box(y=dat['value'].values, x=dat['type'].values)
    data = [trace, trace2]
    return {
            'data': data,
            'layout': go.Layout(
                        xaxis = {'title': 'Data Type'},
                        yaxis = {'title': 'Modified SHAP'}
                )
            }

@app.callback(
        Output('graph3','figure'),
        [Input('input-1', 'value')])
def update_graph(gene_id):
    dat_brca = CORR[(CORR['hgnc_symbol'] == gene_id) & (CORR['project'] == 'TCGA-BRCA')]
    dat_ov = CORR[(CORR['hgnc_symbol'] == gene_id) & (CORR['project'] == 'TCGA-OV')]
    trace = {'x': dat_brca['variable'].values, 'y': dat_brca['value'].values,
            'type':'bar', 'name': 'BRCA'}
    trace2 = {'x': dat_ov['variable'].values, 'y': dat_ov['value'].values,
            'type':'bar', 'name': 'OV'}

    #trace = go.Box(y=dat['value'].values, x=dat['type'].values)
    data = [trace, trace2]
    return {
            'data': data,
            'layout': go.Layout(
                        xaxis = {'title': 'Data Type'},
                        yaxis = {'title': 'Correlation'}
                        )
            }

if __name__ == "__main__":
    app.run_server(host='0.0.0.0')
