import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from dash.dash_table.Format import Format, Group, Scheme, Symbol

df = pd.read_excel('chant.xlsx')
df['Date']= pd.DatetimeIndex(df['Date']).strftime('%d-%m-%Y')
df['Resp']=df['Resp'].astype(str)

app = Dash(_name_)
server = Chant_Dash.server

app.layout = html.Div(children=[
html.H1(children='DOUIN DashBoard Chantier en mouvement :'),
dbc.Row([
    dbc.Col([html.H4(children='Sélection de chantiers : ')]),
    dbc.Col([lchant := dcc.Dropdown([x for x in sorted(df['Code chantier'].unique())], searchable=True, multi=True)]),
    dbc.Col([html.H4(children='Sélection de Responsables : ')]),
    dbc.Col([lresp := dcc.Dropdown([x for x in sorted(df['Resp'].unique())], searchable=True, multi=True)])
    ]),
html.H4(children='Table chantier :'),
tab_chant := dash_table.DataTable(
    data=df.to_dict('records'),
    style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'}, 
    columns=[
    dict(name='Chantier', id='Code chantier', type='text'),
    dict(name='Nom du chantier', id='Lib', type='text'),
    dict(name= 'Responsable', id='Resp', type='text'),
    dict(name='Type', id='Type', type='text'),
    dict(name='Date', id= 'Date', type='datetime'),
    dict(name='Charges', id='Charge', type='numeric', format=Format(precision=2, scheme=Scheme.fixed, group=Group.yes,
        groups=3,
        group_delimiter='.',
        decimal_delimiter=',',
        symbol=Symbol.yes,
        symbol_prefix=u'€')),
    dict(name='Facturation', id='Produit', type='numeric', format=Format(precision=2, scheme=Scheme.fixed, group=Group.yes,
        groups=3,
        group_delimiter='.',
        decimal_delimiter=',',
        symbol=Symbol.yes,
        symbol_prefix=u'€')),
    dict(name='Resultat', id='Resultat', type='numeric', format=Format(precision=2, scheme=Scheme.fixed, group=Group.yes,
        groups=3,
        group_delimiter='.',
        symbol=Symbol.yes,
        symbol_prefix=u'€')),
    dict(name='Coefficient', id='Coeff', type='numeric', format=Format(precision=3, scheme=Scheme.fixed)),
    dict(name='Avancement', id='Avance', type='numeric', format=Format(precision=2, scheme=Scheme.fixed, group=Group.yes,
        groups=3,
        group_delimiter='.',
        symbol=Symbol.yes,
        symbol_prefix=u'€')),
    ],        
        filter_action='native',
        sort_action='native',
        page_size=50,
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{Resultat} <0',
                'column_id': 'Resultat',
            },
            'backgroundColor': 'red',
            'color': 'white'
        }],
        style_header={'backgroundColor': 'rgb(220,220,220)'},
)])


@callback(
    Output(tab_chant, 'data'),
    Input(lchant, 'value'),
    Input(lresp, 'value')
)
def update_dropdown(lchant_v, lresp_v):
    dff = df.copy()

    if lchant_v:
        dff = dff[dff['Code chantier'].isin(lchant_v)]

    if lresp_v:
        dff = dff[dff['Resp'].isin(lresp_v)]

    return dff.to_dict('records')


if __name__ == "__main__":
    app.run_server(debug=True)

