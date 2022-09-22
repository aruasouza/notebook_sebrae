import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math
from plotly.subplots import make_subplots
import plotly.io as pio
# from os import path

# bundle_dir = path.abspath(path.dirname(__file__))
# path_to_conc = path.join(bundle_dir, 'concorrentes_parametros.csv')
# path_to_prod = path.join(bundle_dir, 'produtos_para_analise.csv')

pio.templates.default = "plotly"

concorrentes = pd.read_csv('concorrentes_parametros.csv')
produtos = pd.read_csv('produtos_para_analise.csv')

def idade():
    sorted = concorrentes.loc[[not np.isnan(x) for x in list(concorrentes['idade'])]].sort_values('idade',ascending = False).reset_index(drop=True)
    
    array = np.array(list(filter(lambda x: x > 0,sorted['idade'])))
    mean = array.mean()
    std = array.std()
    median = np.median(array)
    print('Média:',mean,'Desvio padrão:',std,'Mediana:',median)

    colors = ['rgba(99,111,251,255)',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'darkblue'
    fig = go.Figure(data = [go.Bar(x=concorrentes.index,y=sorted['idade'],hovertext=sorted['Nome'],
    name='Idade do Concorrente',marker_color = colors),
    go.Scatter(x=concorrentes.index,y=[mean for i in range(len(concorrentes))],name='Idade Média',line = dict(color = 'tomato')),
    go.Scatter(x=concorrentes.index,y=[mean + std for i in range(len(concorrentes))],name='Desvio Padrão',line = dict(color = 'tomato',dash = 'dot')),
    go.Scatter(x=concorrentes.index,y=[mean - std for i in range(len(concorrentes))],name='Desvio Padrão',line = dict(color = 'tomato',dash = 'dot')),
    ])
    fig.update_layout(title = 'Idade dos Concorrentes',showlegend=False)
    fig.update_xaxes(title = '',showticklabels = False)
    return fig

def preco_medio():
    sorted = concorrentes.loc[[not np.isnan(x) for x in list(concorrentes['preco_std'])]].sort_values('preco_medio',ascending = False).reset_index(drop=True)
    
    array = sorted['preco_medio'].values
    mean = array.mean()
    std = array.std()
    median = np.median(array)
    print('Média:',mean,'Desvio padrão:',std,'Mediana:',median)

    colors = ['Concorrentes',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'SEBRAE SC'
    fig = px.scatter(sorted,x=sorted.index,y='preco_medio',error_y = 'preco_std',color = colors,
    size = [math.log(x) for x in sorted['quantidade_de_cursos']],hover_name='Nome')
    fig.update_layout(title = 'Preço médio dos Cursos dos Concorrentes',showlegend=False)
    fig.update_xaxes(title = '',showticklabels = False,showgrid = False)
    fig.update_yaxes(title = '')
    return fig

def duracao_media():
    sorted = concorrentes.loc[[not np.isnan(x) for x in list(concorrentes['duracao_std'])]].sort_values('duracao_media',ascending = False).reset_index(drop=True)
    
    array = sorted['duracao_media'].values
    mean = array.mean()
    std = array.std()
    median = np.median(array)
    print('Média:',mean,'Desvio padrão:',std,'Mediana:',median)

    colors = ['Concorrentes',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'SEBRAE SC'
    fig = px.scatter(sorted,x=sorted.index,y='duracao_media',error_y = 'duracao_std',color = colors,
    size = [math.log(x) for x in sorted['quantidade_de_cursos']],hover_name='Nome')
    fig.update_layout(title = 'Duração média dos Cursos dos Concorrentes',showlegend=False)
    fig.update_xaxes(title = '',showticklabels = False,showgrid = False)
    fig.update_yaxes(title = '')
    return fig

def quantidade_cursos():

    array = concorrentes['quantidade_de_cursos'].values
    mean = array.mean()
    std = array.std()
    median = np.median(array)
    print('Média:',mean,'Desvio padrão:',std,'Mediana:',median)

    fig = px.treemap(concorrentes,path = [px.Constant('all'),'Nome'],values = 'quantidade_de_cursos')
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(title='Quantidade de Cursos por Concorrente')
    return fig

def preco_hora():
    sorted = concorrentes.loc[[not np.isnan(x) for x in list(concorrentes['preco_hora_medio'])]].reset_index(drop = True)

    array = np.array(list(filter(lambda x: x < 10**10,sorted['preco_hora_medio'])))
    mean = array.mean()
    std = array.std()
    median = np.median(array)
    print('Média:',mean,'Desvio padrão:',std,'Mediana:',median)

    colors = ['Concorrentes',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'SEBRAE SC'
    fig = px.strip(sorted,x='preco_hora_medio',hover_name='Nome',color = colors,stripmode = 'overlay')
    fig.update_layout(title = 'Preço/Hora médio dos Concorrentes',showlegend=False)
    fig.update_xaxes(title = '')
    fig.update_yaxes(showticklabels = False)
    return fig

def graficos():
    lista = produtos['grande_area_legenda'].drop_duplicates(keep = 'first').values
    mean = len(produtos) / len(lista)
    fig1 = go.Figure(data = [
        go.Histogram(x=produtos['grande_area_legenda'],name = 'Contagem',
        text = [len(produtos.loc[produtos['grande_area_legenda'] == g]) for g in lista]),
        go.Scatter(x = lista,y = [mean for i in range(len(lista))],name = 'Média',line = dict(dash = 'dot'),mode = 'lines')
    ])
    fig1.update_layout(title = 'Total de Produtos por Grande Área',showlegend=False,title_font_size=12)

    filtered = produtos.loc[[not np.isnan(x) for x in produtos['duração']]]
    mean = filtered['duração'].values.mean()
    fig2 = go.Figure(data = [
        go.Histogram(x = filtered['grande_area_legenda'],y = filtered['duração'],histfunc = 'avg',name = 'Média Área',
        text = [round(filtered.loc[filtered['grande_area_legenda'] == g,'duração'].values.mean(),1) for g in lista]),
        go.Scatter(x = lista,y = [mean for i in range(len(lista))],name = 'Média Geral',line = dict(dash = 'dot'),mode = 'lines')
    ])
    fig2.update_layout(title = 'Duração Média dos Produtos Encontrados (em horas)',showlegend=False,title_font_size=12)

    filtered = produtos.loc[[not np.isnan(x) for x in produtos['faixa_peco']]]
    mean = filtered['faixa_peco'].values.mean()
    fig3 = go.Figure(data = [
        go.Histogram(x = filtered['grande_area_legenda'],y = filtered['faixa_peco'],histfunc = 'avg',name = 'Média Área',
        text = [round(filtered.loc[filtered['grande_area_legenda'] == g,'faixa_peco'].values.mean(),1) for g in lista]),
        go.Scatter(x = lista,y = [mean for i in range(len(lista))],name = 'Média Geral',line = dict(dash = 'dot'),mode = 'lines')
    ])
    fig3.update_layout(title = 'Preço Médio dos Produtos por Grande Área (em reais)',showlegend=False,title_font_size=12)

    filtered = produtos.loc[produtos['tipo_oferta'] != '']
    lista = filtered['tipo_oferta'].drop_duplicates(keep = 'first').values
    mean = len(filtered) / len(lista)
    fig4 = go.Figure(data = [
        go.Histogram(x=filtered['tipo_oferta'],name = 'Contagem',text = [len(filtered.loc[filtered['tipo_oferta'] == g]) for g in lista]),
        go.Scatter(x = lista,y = [mean for i in range(len(lista))],name = 'Média',line = dict(dash = 'dot'),mode = 'lines')
    ])
    fig4.update_layout(title = 'Total de Produtos por Tipo de Oferta',showlegend=False,title_font_size=12)

    filtered = produtos
    lista = ['Pré-Operação','Até 2 anos','Entre 2 e 5 anos','Acima de 5 anos','Não Definido']
    mean = len(filtered) / len(lista)
    fig5 = go.Figure(data = [
        go.Histogram(x=filtered['maturidade_legenda'],name = 'Contagem',
        text = [len(filtered.loc[filtered['maturidade_legenda'] == g]) for g in lista]),
        go.Scatter(x = lista,y = [mean for i in range(len(lista))],name = 'Média',line = dict(dash = 'dot'),mode = 'lines')
    ])
    fig5.update_layout(title = 'Maturidade por Produto Encontrado',showlegend=False,title_font_size=12,
    xaxis={'categoryorder':'array', 'categoryarray':lista})

    return [fig1,fig2,fig3,fig4,fig5]

def quadrantes():
    figures = []
    # Criar Figura
    fig = make_subplots(rows = 1,cols = 3)

    # Plot 1
    sorted = concorrentes.loc[[x != None for x in list(concorrentes['preco_medio'])]].reset_index(drop = True)
    colors = ['rgba(99,111,251,255)',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'crimson'
    y = (max(sorted['quantidade_de_cursos']) + min(sorted['quantidade_de_cursos'])) / 2
    x = (max(sorted['preco_medio']) + min(sorted['preco_medio'])) / 2
    fig.add_trace(go.Scatter(x = sorted['preco_medio'],y = sorted['quantidade_de_cursos'],mode = 'markers',
    hovertext = sorted['Nome'],marker_color = colors),row = 1,col = 1)
    fig.add_hline(y = y,row = 1,col = 1)
    fig.add_vline(x = x,row = 1,col = 1)
    fig.update_xaxes(title = 'Preço Médio',row = 1,col = 1,showgrid = False)
    fig.update_yaxes(title = 'Quantidade de Cursos',row = 1,col = 1,showgrid = False)

    # Plot 2
    sorted = sorted.loc[[x != None for x in list(sorted['duracao_media'])]].reset_index(drop = True)
    colors = ['rgba(99,111,251,255)',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'crimson'
    y = (max(sorted['preco_medio']) + min(sorted['preco_medio'])) / 2
    x = (max(sorted['duracao_media']) + min(sorted['duracao_media'])) / 2
    fig.add_trace(go.Scatter(x = sorted['duracao_media'],y = sorted['preco_medio'],mode = 'markers',
    hovertext = sorted['Nome'],marker_color = colors),row = 1,col = 2)
    fig.add_hline(y = y,row = 1,col = 2)
    fig.add_vline(x = x,row = 1,col = 2)
    fig.update_xaxes(title = 'Duração Média',row = 1,col = 2,showgrid = False)
    fig.update_yaxes(title = 'Preço Médio',row = 1,col = 2,showgrid = False)

    # Plot 3
    sorted = concorrentes.loc[[x != None for x in list(concorrentes['duracao_media'])]].reset_index(drop = True)
    colors = ['rgba(99,111,251,255)',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'crimson'
    y = (max(sorted['quantidade_de_cursos']) + min(sorted['quantidade_de_cursos'])) / 2
    x = (max(sorted['duracao_media']) + min(sorted['duracao_media'])) / 2
    fig.add_trace(go.Scatter(x = sorted['duracao_media'],y = sorted['quantidade_de_cursos'],mode = 'markers',
    hovertext = sorted['Nome'],marker_color = colors),row = 1,col = 3)
    fig.add_hline(y = y,row = 1,col = 3)
    fig.add_vline(x = x,row = 1,col = 3)
    fig.update_xaxes(title = 'Duração Média',row = 1,col = 3,showgrid = False)
    fig.update_yaxes(title = 'Quantidade de Cursos',row = 1,col = 3,showgrid = False)

    # Título
    fig.update_layout(showlegend = False)

    figures.append(fig)

    # Criar segunda figura
    fig = make_subplots(rows = 1,cols = 3)

    # Plot 1
    sorted = concorrentes.loc[[x != None for x in list(concorrentes['maturidade_media'])]]
    sorted = sorted.loc[[x != None for x in list(sorted['preco_medio'])]].reset_index(drop = True)
    colors = ['rgba(99,111,251,255)',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'crimson'
    x = (max(sorted['maturidade_media']) + min(sorted['maturidade_media'])) / 2
    y = (max(sorted['preco_medio']) + min(sorted['preco_medio'])) / 2
    fig.add_trace(go.Scatter(x = sorted['maturidade_media'],y = sorted['preco_medio'],mode = 'markers',
    hovertext = sorted['Nome'],marker_color = colors),row = 1,col = 1)
    fig.add_hline(y = y,row = 1,col = 1)
    fig.add_vline(x = x,row = 1,col = 1)
    fig.update_xaxes(title = 'Maturidade Média',row = 1,col = 1,showgrid = False)
    fig.update_yaxes(title = 'Preço Médio',row = 1,col = 1,showgrid = False)

    # Plot 2
    sorted = concorrentes.loc[[x != None for x in list(concorrentes['maturidade_media'])]].reset_index(drop = True)
    colors = ['rgba(99,111,251,255)',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'crimson'
    x = (max(sorted['maturidade_media']) + min(sorted['maturidade_media'])) / 2
    y = (max(sorted['quantidade_de_cursos']) + min(sorted['quantidade_de_cursos'])) / 2
    fig.add_trace(go.Scatter(x = sorted['maturidade_media'],y = sorted['quantidade_de_cursos'],mode = 'markers',
    hovertext = sorted['Nome'],marker_color = colors),row = 1,col = 2)
    fig.add_hline(y = y,row = 1,col = 2)
    fig.add_vline(x = x,row = 1,col = 2)
    fig.update_xaxes(title = 'Maturidade Média',row = 1,col = 2,showgrid = False)
    fig.update_yaxes(title = 'Quantidade de produtos',row = 1,col = 2,showgrid = False)

    # Plot 3
    sorted = concorrentes.loc[[x != None for x in list(concorrentes['duracao_media'])]]
    sorted = sorted.loc[[x != None for x in list(concorrentes['prop_online'])]].reset_index(drop = True)
    colors = ['rgba(99,111,251,255)',] * len(sorted)
    index_sebrae = sorted.loc[sorted['Nome'] == 'SEBRAE SC'].index[0]
    colors[index_sebrae] = 'crimson'
    x = (max(sorted['prop_online']) + min(sorted['prop_online'])) / 2
    y = (max(sorted['duracao_media']) + min(sorted['duracao_media'])) / 2
    fig.add_trace(go.Scatter(x = sorted['prop_online'],y = sorted['duracao_media'],mode = 'markers',
    hovertext = sorted['Nome'],marker_color = colors),row = 1,col = 3)
    fig.add_hline(y = y,row = 1,col = 3)
    fig.add_vline(x = x,row = 1,col = 3)
    fig.update_xaxes(title = 'Proporção Online',row = 1,col = 3,showgrid = False)
    fig.update_yaxes(title = 'Duração Média',row = 1,col = 3,showgrid = False)

    # Título
    fig.update_layout(showlegend = False)

    figures.append(fig)

    return figures


def boxplot():
    sorted = concorrentes.loc[[x != None for x in list(concorrentes['preco_std'])]].sort_values(by = 'preco_medio',ascending = False)
    sorted = sorted.loc[sorted['preco_medio'] != 0]
    sorted = sorted.loc[sorted['Nome'] != 'SEBRAE SC']
    codigo_sebrae = int(concorrentes.loc[concorrentes['Nome'] == 'SEBRAE SC','Código'])
    sebrae = produtos.loc[produtos['id_conc'] == codigo_sebrae]
    ids = list(sorted['Código'])
    nomes = sorted['Nome'].values
    fig = go.Figure(data = [go.Box(y = list(filter(lambda x: not np.isnan(x),sebrae['faixa_peco'])),
    name = 'SEBRAE SC',x0 = -1,marker_color = 'black')] + [go.Box(y = list(produtos.loc[produtos['id_conc'] == id,'faixa_peco']),
    name = nomes[ids.index(id)],x0 = ids.index(id)) for id in ids])
    fig.update_yaxes(type = 'log')
    fig.update_xaxes(showticklabels = False)
    fig.update_layout(title = 'Boxplot de Preços por Concorrente (escala logarítmica)')

    return fig