import mysql.connector
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from mysql.connector import Error

def render_cadastrodespesas_popup():
        return html.Div(id="sombra-pop-up", className="sombra", children=[
                
                 html.Div(className="pop-up", children=[
                         
                    html.Div(id="area-btn-close", children=[
                        html.Span("X", className="close", id="btn-close")]),
                        
                    html.Div(id="area-title-pop-up", children=[
                        html.H3("Cadastrar Nova Despesa", className="title-pop-up")]),

                    html.Form(id='form-cad-despesa', children=[
                        html.Fieldset(id='field-cad',children=[

                                html.Div(id='area-bloco1-form', children=[
                                    html.Div(id='area-cad-lanc-despesa', children=[ 
                                        html.Label('Despesa', className='label-cad'),
                                        dcc.Input(id='cad-lanc-des', className='cad-camp', placeholder='Compra de equipamanto', required=True)]),

                                    html.Div(id='area-cad-valor-despesa', children=[
                                        html.Label('Valor', className='label-cad'),
                                        dcc.Input(id='cad-valor-des', className='cad-camp', placeholder='R$ 100,00', required=True)])                                  
                                ]),

                                html.Div(id='area-bloco2-form', children=[
                                    html.Div(id='area-cad-tipo-pag', children=[
                                        html.Label('Tipo de Pag', className='label-cad'),
                                        dcc.Dropdown(id='cad-tipo-pag',  options=[
                                                                            {'label': 'Débito', 'value': 'Debito'},
                                                                            {'label': 'Crédito', 'value': 'Credito'},
                                                                            {'label': 'Pix', 'value': 'Pix'},
                                                                            {'label': 'Espécie', 'value': 'Especia'},
                                                                            {'label': 'Boleto', 'value': 'Boleto'},
                                                                            {'label': 'Outro', 'value': 'Outro'}],                                        
                                        className='cad-camp', placeholder='Pix')]),

                                    html.Div(id='area-cad-categoria', children=[
                                        html.Label('Categoria', className='label-cad'),
                                        dcc.Dropdown(id='cad-categoria-des', options=[
                                                                             {'label': 'Alimentação', 'value': 'Alimentacao'},
                                                                             {'label': 'Transporte', 'value': 'Transporte'},
                                                                             {'label': 'Eletrônicos', 'value': 'Eletronico'},
                                                                             {'label': 'Mat Limpeza', 'value': 'Mat Limpeza'}],                                        
                                         className='cad-camp', placeholder='Eletrônico')])
                                    ]),
                                        
                                html.Div(id='area-bloco3-form', children=[
                                    html.Div(id='area-cad-vencimento', children=[
                                        html.Label('Vencimento', className='label-cad'),
                                        dcc.DatePickerSingle(id='cad-vencimento-des', placeholder='Selecione...', display_format='DD/MM/YYYY', className='cad-camp')]),

                                    html.Div(id='area-cad-status-des', children=[
                                        html.Label('Status', className='label-cad'),
                                        dcc.Dropdown(id='cad-status-des', options=[
                                                                            {'label': 'Pago', 'value': 'Pago'},
                                                                            {'label': 'Processando', 'value': 'Processando'},
                                                                            {'label': 'Pendente', 'value': 'Pendente'}],
                                     className='cad-camp', placeholder='Pago')])
                                ])

                        ]),#=> Fechamento do field-set
                        html.Button('Cadastrar', id='btn-form-enviar-despesa', type='button')
                    ])#=> Fechamento do Formulário
                 ]) #=> Fechamento do Pop-Up

        ])

# Conexão com o banco de dados
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='finances',
            user='root',
            password='S3n1nh@s')
        
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Erro ao conectar ao Banco de Dados: {e}")
        return None
        
#=================================================== Salvar dados no Banco ========================================

def save_despesa_callback(app):
    @app.callback(
        Output('form-cad-despesa', 'children'),
        Input('btn-form-enviar-despesa', 'n_clicks'),
        State('cad-lanc-des', 'value'),
        State('cad-valor-des', 'value'),
        State('cad-tipo-pag', 'value'),
        State('cad-categoria-des', 'value'),
        State('cad-vencimento-des', 'date'),
        State('cad-status-des', 'value')
    )

    def salvar_lancamento_despesa(n_clicks, lancamento_despesa,valor_despesa, tipo_despesa, categoria_despesa, vencimento_despesa, status_despesa):
        if n_clicks is None:
            raise PreventUpdate
        
        conn = connect_to_db()
        if conn is None:
            return print("Erro ao conectar ao Banco de Dados.")
        
        cursor = conn.cursor()

        try:
            # Preparando a consulta SQL
            query = """INSERT INTO lancamentos_despesas
                    (lancamento_despesa, valor_despesa, tipo_despesa, categoria_despesa, vencimento_despesa, status_despesa)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            valores_despesa = (lancamento_despesa, valor_despesa, tipo_despesa, categoria_despesa, vencimento_despesa, status_despesa)

            # Depuração: Imprimir os valores para verificar
            print(f"Executando Query de Despesa: {query}")
            print(f"Valores despesa: {valores_despesa}")

            # Executando a consulta SQL
            cursor.execute(query, valores_despesa)
            conn.commit()

            # Verificando se o commit foi bem-sucedido
            if conn.is_connected():
                print("Dados da Despesa cadastrados com sucesso!")
            else:
                print("Erro: Falha no commit.")
                
        finally:
            cursor.close()
            conn.close()
