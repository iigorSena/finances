import mysql.connector
import datetime
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate


def render_cadastroreceita_popup():
    return html.Div(id="sombra-pop-up", className="sombra", children=[
            html.Div(className="pop-up", children=[

                    html.Div(id="area-btn-close", children=[
                        html.Span("X", className="close", id="btn-close")]),
                        
                    html.Div(id="area-title-pop-up", children=[
                        html.H3("Cadastrar Novo Lançamento", className="title-pop-up")]),

                    html.Form(id='form-cad-receita', children=[ 
                        html.Fieldset(id='field-cad',children=[

                            html.Div(id='area-bloco1-form', children=[
                                html.Div(id='cad-area-lancamento',children=[
                                    html.Label(['', html.Br(), 'Lançamento'], className='label-cad'),
                                    dcc.Input(id='cad-lancamento', className='cad-camp', placeholder='Aluguel...', required=True)]),

                                html.Div(id='cad-area-valor-total', children=[
                                    html.Label(['', html.Br(), 'Valor total'], className='label-cad'),
                                    dcc.Input(id='cad-valor-total', className='cad-camp', placeholder='R$ 5.000,00', required=True)])]),

                                html.Div(id='cad-area-tipo-de-pag', children=[
                                    html.Label('Tipo de Pag', className='label-cad'),
                                    dcc.Dropdown(id='cad-tipo-de-pag', options=[
                                                                            {'label': 'Débito', 'value': 'Debito'},
                                                                            {'label': 'Crédito', 'value': 'Credito'},
                                                                            {'label': 'Pix', 'value': 'Pix'},
                                                                            {'label': 'Espécie', 'value': 'Especia'},
                                                                            {'label': 'Boleto', 'value': 'Boleto'},
                                                                            {'label': 'Outro', 'value': 'Outro'}],
                                   placeholder='Selecione o Tipo de Pagamento', className='cad-camp')]),
                                                               
                                html.Div(id='cad-area-status', children=[
                                    html.Label('Status', className='label-cad'),
                                    dcc.Dropdown(id='cad-status', options=[
                                                                            {'label': 'Pago', 'value': 'Pago'},
                                                                            {'label': 'Pendente', 'value': 'Pendente'},
                                                                            {'label': 'Processando', 'value': 'Processando'}],
                                     className='cad-camp', placeholder='Selecione...')]),

                                html.Div(id='cad-area-categoria', children=[
                                    html.Label('Categoria', className='label-cad'),
                                    dcc.Dropdown(id='cad-categoria', options=[
                                                                             {'label': 'Alimentação', 'value': 'Alimentacao'},
                                                                             {'label': 'Transporte', 'value': 'Transporte'},
                                                                             {'label': 'Compras', 'value': 'Compras'},
                                                                             {'label': 'Material', 'value': 'Material'}],
                                        className='cad-camp', placeholder='Selecione...')]),

                                html.Div(id='cad-area-data', children=[
                                    html.Label('Data', className='label-cad'),
                                    dcc.DatePickerSingle(id='cad-data', placeholder='Selecione...', display_format='DD/MM/YYYY', className='cad-camp')])])

                        ]), #Fechamento do Fieldset
                        html.Button('Cadastrar', id='btn-form-enviar-receita', type='button')])
            ])

# Conexão com o Banco=====================================================================================

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
# Função Salvar Receitas no Banco =======================================================================
def save_receita_callback(app):
    @app.callback(
        Output('form-cad-receita', 'children'),
        Input('btn-form-enviar-receita', 'n_clicks'),
        State('cad-lancamento', 'value'),
        State('cad-valor-total', 'value'),
        State('cad-tipo-de-pag', 'value'),
        State('cad-status', 'value'),
        State('cad-categoria', 'value'),
        State('cad-data', 'date')
)

    def salvar_lancamento_receita(n_clicks, lancamento, valor_total, tipo_pag, status, categoria, data):
        if n_clicks is None:
            raise PreventUpdate
        
        conn = connect_to_db()
        if conn is None:
            return print("Erro ao conectar ao Banco de Dados.")

        cursor = conn.cursor()

        try:
            # Formatando a data
            data_formatada = datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%Y/%m/%d')

            # Preparando a consulta SQL
            query = """INSERT INTO lancamentos_receitas
                    (lancamento, valor_total, tipo_pag, status, categoria, data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores_receita = (lancamento, valor_total, tipo_pag, status, categoria, data_formatada)

            # Depuração: Imprimir os valores para verificar
            print(f"Executando Query: {query}")
            print(f"Valores: {valores_receita}")

            # Executando a consulta SQL
            cursor.execute(query, valores_receita)
            conn.commit()

            # Verificando se o commit foi bem-sucedido
            if conn.is_connected():
                print("Dados da Receita cadastrados com sucesso!")
            else:
                print("Erro: Falha no commit.")

        finally:
            cursor.close()
            conn.close()
