import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import pandas as pd
import requests
import config
import APIs
from Bert import BertModel

gs = APIs.GSAPI()
tw = APIs.TwitterAPI()

model = BertModel()
model.loadmodel('bert model')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2('Sentiment Analysis', style={'textAlign': 'center'}),
    html.Div([
        html.Div(id='container-button-basic',
                 children='Enter a keyword and press submit'),
        html.Div([dcc.Input(id='input-on-submit', type='text'),
                  html.Button('Submit', id='submit-val', n_clicks=0)])],
        style={'textAlign': 'center'}
    ),
    html.H3('Twitter results', style={'color':'blue'}),
    html.Div(id='table1'),
    html.H3('Google Search results', style={'color':'red'}),
    html.Div(id='table2')
])

@app.callback(
    dash.dependencies.Output('table1', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')])
def display_table(n_clicks, value): 
    twsentiment = []
    if n_clicks:  
        keyword = value
        twresult = tw.search(keyword,10)
        for i in range(len(twresult)):
            twsentiment.append(model.predict(twresult[i]))
        dftw = pd.DataFrame({'Sentence':twresult, 'Sentiment':twsentiment})
        return [dt.DataTable(
            id = 'table1',
            data = dftw.to_dict('records'),
            columns = [{"name": i, "id": i} for i in dftw.columns],
            #page_size = 10,
            fixed_rows = {'headers':True},
            style_table = {'height':400},
            style_cell = {'textAlign': 'left',
                          'whiteSpace': 'normal',
                          'height': 'auto',
                         },
            
            style_data_conditional=[
                {'if': {'filter_query':'{Sentiment} = 0'},
                 'backgroundColor': '#FFC1E0'},
                {'if': {'filter_query': '{Sentiment} = 1'},
                 'backgroundColor': '#93FF93'},
                {'if': {'column_id':'Sentence'},
                 'width': '200px'},
                {'if': {'column_id':'Sentiment'},
                 'width': '25px'},],
        )]


@app.callback(
    dash.dependencies.Output('table2', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')])
def update_table(n_clicks, value): 
    gssentiment = []
    if n_clicks:  
        keyword = value
        gsresult = gs.search(keyword,10)
        for i in range(len(gsresult)):
            gssentiment.append(model.predict(gsresult[i]))
        dfgs = pd.DataFrame({'Sentence':gsresult, 'Sentiment':gssentiment})
        return [dt.DataTable(
            id = 'table2',
            data = dfgs.to_dict('records'),
            columns = [{"name": i, "id": i} for i in dfgs.columns],
            #page_size = 10,
            fixed_rows = {'headers':True},
            style_table = {'height':400},
            style_cell = {'textAlign': 'left',
                          'whiteSpace': 'normal',
                          'height': 'auto',
                         },
            
            style_data_conditional=[
                {'if': {'filter_query':'{Sentiment} = 0'},
                 'backgroundColor': '#FFC1E0'},
                {'if': {'filter_query': '{Sentiment} = 1'},
                 'backgroundColor': '#93FF93'},
                {'if': {'column_id':'Sentence'},
                 'width': '225px'},
                {'if': {'column_id':'Sentiment'},
                 'width': '25px'},],
        )]

if __name__ == '__main__':
    app.run_server(debug=True)