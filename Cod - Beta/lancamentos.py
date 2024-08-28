from dash import html, dcc, dash_table, callback_context
import mysql.connector


#================================== Conexão com o DB==========================================
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='finances',
            user='root',
            password='S3n1nh@s')
        
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao Banco de Dados: {e}")
        return None

#============================== Solicitação de dados da Receita ao DB ================================
def fetch_receitas():
    conn = connect_to_db()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM lancamentos_receitas")
        rows = cursor.fetchall()
        return rows
    
    except mysql.connector.Error as err:
        print(f"Erro ao buscar os dados: {err}")
        return []
    
    finally:
        cursor.close()
        conn.close()

#=================================== Renderização da Tabela ===================================

def render_historicoreceitas():
    receitas = fetch_receitas()

    return html.Div(id='layout-lancamentos', children=[
        html.Div(id='lancamento-btn', children=[
            html.Div(id='area-btn1', children=[
                    html.Button('Receitas', id='btn-lan-receitas')]),

            html.Div(id='area-btn2', children=[
                    html.Button('Despesas', id='btn-lanc-despesas')])
        ]),

        html.Div(id='back-tabela-receita', children=[
               dash_table.DataTable(
                columns=[
                    {'name': 'ID', 'id': 'id', 'type': 'numeric'},
                    {'name': 'Lançamento', 'id': 'lancamento', 'type': 'text'},
                    {'name': 'Valor Total', 'id': 'valor_total', 'type': 'numeric', 'format': {'specifier': '$,.2f'}},
                    {'name': 'Tipo de Pag', 'id': 'tipo_pag', 'type': 'text'},
                    {'name': 'Status', 'id': 'status', 'type': 'text'},
                    {'name': 'Categoria', 'id': 'categoria', 'type': 'text'},
                    {'name': 'Data', 'id': 'data', 'type': 'datetime'}
                ],
                data=receitas,
                editable=False,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center'},
                style_header={
                    'color': '#0e6657',
                    'backgroundColor': '#ffffff',
                    'borde': '2px solid',
                    'border-color': '#0e6657',
                    'fontWeight': 'bold',
                    'font-size': '12pt',
                    'whiteSpace': 'normal',  # Permitir quebra de linha
                    'overflow': 'hidden'  # Ocultar qualquer transbordo
                },

                #Estilo das Células=====================================================
                style_data_conditional=[
                    #Estilo GERAL DAS CÉLULAS
                    {
                        'background-color': '#0e6657',
                        'color': 'white',
                        'font-size': '12pt',
                        'border': '1px solid white'
                     },

                    #CONDICIONAL
                    {
                        'if': {'state': 'active'}, # Quando a célula é clicada
                            'backgroundColor': '#147575',
                            'border': '1px solid #1bc4a7'
                    }],

                 style_cell_conditional=[
                    #CONDIÇÃO GERAL PARA CÉLULAS
                      {
                        'if': {'column_id': 'id'},
                        'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',
                        'text-align': 'center'
                    },
                      
                      {
                        'if': {'column_id': 'lancamento'},
                        'minWidth': '150px', 'width': '220px', 'maxWidth': '220px',
                        'text-align': 'left'
                    },

                    {
                        'if': {'column_id': 'valor_total'},
                        'minWidth': '150px', 'width': '150px', 'maxWidth': '200px'
                    },                  

                    {
                        'if': {'column_id': 'tipo_pag'},
                        'minWidth': '80px', 'width': '80px', 'maxWidth': '80px'
                    },

                    {
                        'if': {'column_id': 'status'},
                        'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'
                    },

                    {
                        'if': {'column_id': 'categoria'},
                        'minWidth': '140px', 'width': '140px', 'maxWidth': '150px'
                    },

                    {
                        'if': {'column_id': 'data'},
                        'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'
                    }
                 ]
            ),
])]),

#============================== Solicitação de dados da Despesa ao DB ================================
def fetch_despesas():
    conn = connect_to_db()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM lancamentos_despesas")
        rows = cursor.fetchall()
        return rows
    
    except mysql.connector.Error as err:
        print(f"Erro ao buscar despesas: {err}")
        return []
    
    finally:
        cursor.close()
        conn.close()

#================================= Layout histórico Despesas =================================================
def render_historicodespesas():
    despesas = fetch_despesas()

    return html.Div(id='layout-lancamentos-despesas', children=[
        html.Div(id='back-tabela-despesa', children=[
            dash_table.DataTable(columns=[
                    {'name': 'ID', 'id': 'ID', 'type': 'numeric'},
                    {'name': 'Despesa', 'id': 'lancamento_despesa', 'type': 'text'},
                    {'name': 'Valor', 'id': 'valor_despesa', 'type': 'numeric', 'format': {'specifier': '$,.2f'}},
                    {'name': 'Tipo de Pag', 'id': 'tipo_despesa', 'type': 'text'},
                    {'name': 'Categoria', 'id': 'categoria_despesa', 'type': 'text'},
                    {'name': 'Vencimento', 'id': 'vencimento_despesa', 'type': 'datetime'},
                    {'name': 'Status', 'id': 'status_despesa', 'type': 'text'}
                ],
                    data=despesas,
                    editable=False,
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'center'},
                    style_header={
                        'color': '#0e6657',
                        'backgroundColor': '#ffffff',
                        'borde': '2px solid',
                        'border-color': '#0e6657',
                        'fontWeight': 'bold',
                        'font-size': '12pt',
                        'whiteSpace': 'normal',  # Permitir quebra de linha
                        'overflow': 'hidden'},  # Ocultar qualquer transbordo
            )
        ])
    ])

           
