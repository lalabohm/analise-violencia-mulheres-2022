import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

csv_file = "dados_tratados.csv"
df = pd.read_csv(csv_file, sep=",", encoding="utf-8")

# Mapeamento dos valores numéricos para texto
mapa_autor_sexo = {1: "Masculino", 0: "Feminino", -1: "Não Informado"}

# Aplicar o mapeamento na coluna AUTOR_SEXO
df["AUTOR_SEXO"] = df["AUTOR_SEXO"].map(mapa_autor_sexo)

# Criar faixas etárias para melhor visualização
df['Faixa Etária'] = pd.cut(df['NU_IDADE_N'], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120],
                             labels=["0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100", "101-120"])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Layout do dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard - Violência contra a Mulher", className="text-center text-dark mb-4"), width=12, className="d-flex justify-content-center")
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico_distribuicao_sexo'), width=6),
        dbc.Col(dcc.Graph(id='grafico_local_ocorrencia'), width=6)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico_idades'), width=12)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico_municipios_nao_informado'), width=12)
    ])
], fluid=True)

# Callback para atualizar gráficos
@app.callback(
    Output('grafico_distribuicao_sexo', 'figure'),
    Input('grafico_distribuicao_sexo', 'id')
)
def atualizar_distribuicao_sexo(_):
    fig = px.histogram(df, x='AUTOR_SEXO', title="Distribuição do Sexo do Autor da Violência")
    return fig
@app.callback(
    Output('grafico_local_ocorrencia', 'figure'),
    Input('grafico_local_ocorrencia', 'id')
)
def atualizar_local_ocorrencia(_):
    df_local_count = df["LOCAL_OCOR"].value_counts(normalize=True).mul(100).reset_index()
    df_local_count.columns = ["LOCAL_OCOR", "Proporção"]
    fig = px.bar(df_local_count, x='LOCAL_OCOR', y='Proporção', title="Distribuição do Local de Ocorrência", range_y=[0, 70])
    return fig

@app.callback(
    Output('grafico_idades', 'figure'),
    Input('grafico_idades', 'id')
)
def atualizar_idades(_):
    fig = px.bar(df['Faixa Etária'].value_counts().reset_index(),
                 x='Faixa Etária', y='Faixa Etária',
                 title="Distribuição de Idades (Agrupadas por Faixa Etária)",
                 labels={'Faixa Etária': 'Quantidade'},
                 width=1000, height=500)
    return fig


@app.callback(
    Output('grafico_municipios_nao_informado', 'figure'),
    Input('grafico_municipios_nao_informado', 'id')
)
def atualizar_municipios_nao_informado(_):
    df_nao_info = df[df.isna().sum(axis=1) > 3]  # Municípios com muitos valores ausentes
    fig = px.bar(df_nao_info, x='ID_MN_RESI', title="Municípios com Maior Proporção de Dados 'Não Informado'")
    return fig

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)

