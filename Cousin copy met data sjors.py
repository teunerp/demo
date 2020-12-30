#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px
from IPython import get_ipython
from IPython import get_ipython
# get_ipython().run_line_magic('inline')
import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

#---------------------------------------------------------------

import datetime 
# get_ipython().run_line_magic('matplotlib', 'inline')

deelnemers = pd.read_excel (r'C:\Users\Teun\Documents\Untitled Folder\deelnemers2.xlsx')
deelnemers = deelnemers[['Inschrijf datumtijd','Periode']]


deelnemers['Inschrijf datumtijd'] = deelnemers['Inschrijf datumtijd'].apply(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y %H:%M:%S'))
deelnemers["Inschrijf datumtijdnew"] = pd.to_datetime(deelnemers["Inschrijf datumtijd"], '%d-%m-%Y  %H:%M:%S')
deelnemers["Inschrijf datumtijdnew"] = deelnemers["Inschrijf datumtijdnew"].dt.date 


# make number of days. 
nondel = deelnemers.groupby("Periode")['Inschrijf datumtijdnew'].agg([min])
nondel ["Periode"] = nondel.index
nondel.index = [0,1,2,3];

          
for lab, row in nondel.iterrows():
    a=nondel["min"].iloc[lab]
    b=(nondel["Periode"].iloc[lab])
    deelnemers.loc[deelnemers['Periode'] == b, 'Startdate'] = a 


deelnemers["days"] = pd.to_numeric(deelnemers["Inschrijf datumtijdnew"]- deelnemers["Startdate"])/86400000000000
deelnemers = deelnemers[['Periode','days']]

# deelnemers.days.mean()
deelnemers1 = deelnemers
test = (deelnemers1.groupby(["Periode",'days']).days.count().groupby(level=0).cumsum())
df = pd.DataFrame(test)

df.columns = ["dayscumsum"]

df.reset_index(inplace=True)
df.columns = ["CUISINE DESCRIPTION",'INSPECTION DATE',"SCORE"]
print(df)


# In[ ]:


app.layout = html.Div([

    html.Div([
        dcc.Graph(id='our_graph')
    ],className='nine columns'),

    html.Div([

        html.Br(),
        html.Label(['Choose 3 Cuisines to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='cuisine_one',
            options=[{'label':x, 'value':x} for x in df.sort_values('CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
            value='African',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Cuisine...',
            className='form-dropdown',
            style={'width':"70%"},
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='cuisine_two',
            options=[{'label':x, 'value':x} for x in df.sort_values('CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
            value='Asian',
            multi=False,
            clearable=False,
            persistence='string',
            style={'width':"70%"},
            persistence_type='session'),

        dcc.Dropdown(id='cuisine_three',
            options=[{'label':x, 'value':x} for x in df.sort_values('CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
            value='Donuts',
            multi=False,
            clearable=False,
            persistence='string',
            style={'width':"70%"},
            persistence_type='local'),

    ],className='three columns'),

])

#---------------------------------------------------------------

@app.callback(
    Output('our_graph','figure'),
    [Input('cuisine_one','value'),
     Input('cuisine_two','value'),
     Input('cuisine_three','value')]
)

def build_graph(first_cuisine, second_cuisine, third_cuisine):
    dff=df[(df['CUISINE DESCRIPTION']==first_cuisine)|
           (df['CUISINE DESCRIPTION']==second_cuisine)|
           (df['CUISINE DESCRIPTION']==third_cuisine)]
    # print(dff[:5])

    fig = px.line(dff, x="INSPECTION DATE", y="SCORE", color='CUISINE DESCRIPTION', height=600)
    fig.update_layout(yaxis={'title':'NEGATIVE POINT'},
                      title={'text':'Restaurant Inspections in NYC',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





# In[ ]:




