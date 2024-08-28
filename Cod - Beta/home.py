import dash
from dash import Dash, dcc, html, Input, Output, State
from dashboard import render_dashboard
from lancamentos import render_historicoreceitas, render_historicodespesas
from cadreceita import render_cadastroreceita_popup, save_receita_callback
from caddespesas import render_cadastrodespesas_popup, save_despesa_callback
from dash.exceptions import PreventUpdate
from mysql.connector import Error

# Instância do Dash ===========================================================================================
app = Dash(__name__, external_stylesheets=['assents/estilizacao-home.py', 'assets/estilizacao-global.css',
                                           'assets/estilizacao-pop-despesa.css', 'assets/estilizacao-lancamento.css']) 
app.title = 'Home'

# Menu esquerdo===============================================================================================
app.layout = html.Tbody(id='body', children=[
              
        html.Div(id='painel-esquerdo', className='painel-visivel', children=[

            html.Div(id='area-bloco1-painel-esquerdo', children=[                
                html.Div(id='area-nome', children=[
                    html.P(['Controle',
                        html.Br(),
                        'Financeiro'], id='nome')])               
                
                ]),

            html.Hr(),
            html.Button('Dashboard', className='btn-principal', id='btn-dashboard'),
            html.Button('Lançamentos', className='btn-principal', id='btn-lancamentos'),

            html.Div(id='area-btn-cad', children=[
                html.Button('Receita', id='btn-receita'),
                html.Button('Despesa', id='btn-despesa')])
            ]),

# ÁREA PRINCIPAL DE EXIBIÇÃO DA MAIN 2=================================================

        html.Div(id='main2', children=[
            #CABEÇALHO
            html.Div(id='cabecalho', children=[
                html.Div(id='area-btn-recolher', children=[
                    html.Button('<', id='btn-recolher')]),

                html.H4(['cabeçalho', html.Br(), ' ']),
            ]),

            #CORPO
            html.Div(id='layout-trabalho', children=[]),

            #RODAPÉ
            html.Div(id='rodape', children=[
                html.H5('Todos os direitos reservados | 2024', id='direitos')
                ])
        ]),
        render_cadastroreceita_popup(),
        render_cadastrodespesas_popup()
])

#============================== Recolhimento do Painel Esquerdo=============================================
@app.callback(
    [Output('painel-esquerdo', 'className'), Output('btn-recolher', 'children')],
    Input('btn-recolher', 'n_clicks'),
    State('painel-esquerdo', 'className'))
    
def recolher_painel(n_clicks, current_class):
    if n_clicks is None:
        raise PreventUpdate
    
    if current_class is None:
        current_class = 'painel-visivel'

    if 'painel-recolhido' in current_class:
        return 'painel-visivel', '<'
    else:
        return 'painel-recolhido', '>'

#====================== Função que alterna entre os layouts do Dashboard e Lançamentos =============================
@app.callback(
    Output('layout-trabalho', 'children'),
    [Input('btn-dashboard', 'n_clicks'),
     Input('btn-lancamentos', 'n_clicks'),
     Input('btn-receita', 'n_clicks'),
     Input('btn-despesa', 'n_clicks')]
)

def update_area_grafico(btn_dashboard_clicks, btn_lancamentos_clicks, btn_receita_clicks, btn_despesa_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return html.H4('Controle diário!')
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'btn-dashboard':
            return render_dashboard()
        elif button_id == 'btn-lancamentos':
            return render_historicoreceitas()
        elif button_id == 'btn-receita':
            return render_cadastroreceita_popup()
        elif button_id == 'btn-despesa':
            return render_cadastrodespesas_popup()
        
# Controle do Pop-Up  =================================================================================        
@app.callback(
    Output('sombra-pop-up', 'style'),
    [Input('btn-receita', 'n_clicks'),
    Input('btn-close', 'n_clicks'),
    Input('btn-despesa', 'n_clicks')],
    [State('sombra-pop-up', 'style')]
)
def toggle_modal(n1, n2, n3, current_style):
    if n1 or n2 or n3:
        if current_style and current_style.get('display') == 'block':
            return {'display': 'none'}
        else:
            return {'display': 'block'}
    return {'display': 'none'}

# Funções de Lançamentos no Banco ====================================================

save_receita_callback(app)
save_despesa_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)