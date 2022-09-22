import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from nltk.corpus import stopwords
from datetime import datetime

stopw = set(stopwords.words('portuguese'))
def extrair_palavras(lista):
    palavras = set()
    for palavra in lista:
        if type(palavra) == str:
            while len(palavra) > 1:
                index = palavra.find(' ')
                if index != -1:
                    extracao = palavra[:index]
                    palavra = palavra[index + 1:]
                else:
                    extracao = palavra
                    palavra = ''
                extracao_limpa = extracao.replace('"','').replace(',','').replace('.','').replace('(','').replace(')','')
                extracao_limpa = extracao_limpa.replace(':','').replace('\n','').replace('/','').replace('-','').replace('“','')
                extracao_limpa = extracao_limpa.replace('”','').replace('?','').lower()
                if ((len(extracao_limpa) > 2) and (extracao_limpa not in stopw)) or extracao_limpa == 'ti':
                    palavras.add(extracao_limpa)
    return palavras

def legenda_area(key):
    dicionario = {
        1:'financeiro',
        2:'mercado',
        3:'pessoas',
        4:'produção',
        5:'estratégia',
        6:'legal jurídica'
    }
    if key in dicionario:
        return dicionario[key]
    else:
        return ''

def legenda_sub_area(key):
    dicionario = {
    1.1:'gestão financeira',
    2.1:'concorrência',
    2.2:'fornecedores',
    2.3:'equipe vendas',
    2.4:'vendas',
    2.5:'precificação',
    2.6:'exportação novos mercados',
    2.7:'marketing digital',
    3.1:'seleção',
    3.2:'treinamento',
    3.3:'retenção',
    3.4:'liderança',
    3.5:'estratégia marketing',
    4.1:'processo produtivo',
    4.2:'processo prestação serviço',
    4.3:'gestão estoque',
    4.4:'produtividade',
    4.5:'layout loja',
    4.6:'logística',
    4.7:'logística venda online',
    5.1:'expansão',
    5.2:'qual negócio entrar',
    5.3:'modelos negócio franquia',
    5.4:'processos ti',
    6.1:'lgpd',
    6.2:'gestão jurídica'
    }
    if key in dicionario:
        return dicionario[key]
    else:
        return ''

def verificar_se_e_conc(palavras,df,index):
    palavras_conc = extrair_palavras(df.iloc[index].values)
    for palavra in palavras_conc:
        if palavra in palavras:
            return True
    return False

def duracao_semelhante(duracao_base,duracao):
    if (abs(duracao - duracao_base) / duracao_base) < 0.5:
        return True
    return (abs(duracao - duracao_base) < 10)

def closest(lst, K): 
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

def converter_horas(string):
    try:
        return int(string)
    except:
        try:
            h_index = string.find('h')
            return int(string[:h_index])
        except:
            try:
                string = string.replace('.',':')
                string = string.replace(',',':')
                dois_p_index = string.find(':')
                return int(string[:dois_p_index])
            except:
                return None

def american_notation(string):
    string = string.lower()
    if string == 'gratuito':
        return 0
    elif (string == 'não definido') or (string == 'sob consulta') or (string == 'sem informação'):
        return None
    string = string.replace(',','.')
    return float(string)

def convert_float(number):
    number = number.replace(',','.')
    try:
        return float(number)
    except:
        if number == 'Gratuito':
            return 0
        else:
            return None

def convert_data(data):
    try:
        return pd.to_datetime(data,format = '%d/%m/%Y')
    except:
        return None

def somar(a,b):
    try:
        return a + b
    except:
        return None

def legenda_oferta(key):
    try:
        key = int(key)
    except:
        pass
    dicionario = {
        1:'EAD',
        2:'PRESENCIAL',
        3:'IN COMPANY',
        4:'VÍDEOS',
        5:'PALESTRA',
        6:'CONSULTORIA'
    }
    if key in dicionario:
        return dicionario[key]
    else:
        return ''

def legenda_maturidade(key):
    try:
        key = int(key)
    except:
        pass
    dicionario = {
        1:'Pré-Operação',
        2:'Até 2 anos',
        3:'Entre 2 e 5 anos',
        4:'Acima de 5 anos'
    }
    if key in dicionario:
        return dicionario[key]
    else:
        return 'Não Definido'

conc = pd.read_csv('Concorrentes v2.csv',sep = ';')
conc.rename(columns={'Unnamed: 1':'Nome'},inplace=True)
produtos = pd.read_csv('Produtos.csv',sep = ';',encoding = 'ANSI')

sebrae = conc.loc[conc['Nome'] == 'SEBRAE SC']
codigo_sebrae = int(sebrae['Código'])
concorrentes = conc.loc[conc['Nome'] != 'SEBRAE SC'].reset_index(drop = True)

produtos['duração'] = [converter_horas(tempo) for tempo in produtos['duração']]
produtos['grande_area_legenda'] = [legenda_area(key) for key in produtos['grande_area']]
produtos['sub_area_legenda'] = [legenda_sub_area(key) for key in produtos['sub_area']]
produtos_sebrae = produtos.loc[produtos['id_conc'] == codigo_sebrae].reset_index(drop = True)
produtos_conc = produtos.loc[produtos['id_conc'] != codigo_sebrae].reset_index(drop = True)

cargas_horarias = np.array(list(filter(lambda x:not np.isnan(x),list(produtos_sebrae['duração']))))
cargas_horarias_conc = np.array(list(filter(lambda x:not np.isnan(x),list(produtos_conc['duração']))))

concorrentes['duracao_media'] = None
concorrentes['duracao_std'] = None
concorrentes['possui_produtos'] = None
for i in range(len(concorrentes)):
    codigo = concorrentes.loc[i,'Código']
    prods = produtos_conc.loc[produtos_conc['id_conc'] == codigo]
    media = np.array(list(filter(lambda x: not np.isnan(x),prods['duração']))).mean()
    std = np.array(list(filter(lambda x: not np.isnan(x),prods['duração']))).std()
    concorrentes.loc[i,'duracao_media'] = media
    concorrentes.loc[i,'duracao_std'] = std
    concorrentes.loc[i,'possui_produtos'] = len(prods) > 0

media_sebrae = cargas_horarias.mean()
std_sebrae = cargas_horarias.std()
trashold_sebrae = media_sebrae + 2 * std_sebrae

concorrentes['cursos_longos'] = None
for i in range(len(concorrentes)):
    concorrente = concorrentes.loc[i]
    media = concorrente['duracao_media']
    concorrentes.loc[i,'cursos_longos'] = media < trashold_sebrae

duracao_keywords = {}
keys = []
for valor in cargas_horarias:
    if valor not in duracao_keywords:
        filtro = [duracao_semelhante(valor,duracao) for duracao in produtos_sebrae['duração']]
        segmento = produtos_sebrae.loc[filtro]
        keys.append(valor)
        duracao_keywords[valor] = extrair_palavras(
    list(segmento['nome_produto']) + 
    list(segmento['grande_area_legenda']) + 
    list(segmento['sub_area_legenda']))

filtro = []
for i in range(len(produtos_conc)):
    tempo = produtos_conc['duração'].iloc[i]
    if np.isnan(tempo):
        filtro.append(False)
    else:
        key = closest(keys,tempo)
        filtro.append(verificar_se_e_conc(duracao_keywords[key],produtos_conc.loc[:,['grande_area_legenda','sub_area_legenda','nome_produto']],i))
produtos_conc['is_conc_keywords'] = filtro
concorrentes['filter_keywords'] = None
for i in range(len(concorrentes)):
    concorrente = concorrentes.loc[i]
    codigo = concorrente['Código']
    segmento = produtos_conc.loc[produtos_conc['id_conc'] == codigo]
    concorrentes.loc[i,'filter_keywords'] = sum(segmento['is_conc_keywords']) > 0

filtrar = []
motivo_remocao = []
sem_produtos = 0
duracao_longa = 0
resgatado_keywords = 0
for i in range(len(concorrentes)):
    if not concorrentes.loc[i,'possui_produtos']:
        sem_produtos += 1
        filtrar.append(False)
        motivo_remocao.append('sem produtos')
    elif not concorrentes.loc[i,'cursos_longos']:
        duracao_longa += 1
        if concorrentes.loc[i,'filter_keywords']:
            resgatado_keywords += 1
            filtrar.append(True)
        else:
            filtrar.append(False)
            motivo_remocao.append('cursos muito longos')
    else:
        filtrar.append(True)

print('Sem produtos:',sem_produtos)
print('Cursos longos:',duracao_longa)
print('Resgatado pelo teste das keywords:',resgatado_keywords)

empresas_concorrentes_filtradas = concorrentes.loc[filtrar,concorrentes.columns[:-5]]
empresas_removidas = concorrentes.loc[[not x for x in filtrar],concorrentes.columns[:-5]]
empresas_removidas['motivo_remocao'] = motivo_remocao

# empresas_removidas.to_csv('concorrentes_removidos.csv',index = False,encoding = 'ANSI',sep = ';')
concorrentes_filtrados = pd.concat([empresas_concorrentes_filtradas,sebrae]).reset_index(drop = True)
# concorrentes_filtrados.to_csv('concorrentes_filtrados.csv',index = False,sep = ';',encoding = 'ANSI')

ids = list(empresas_concorrentes_filtradas['Código'])
del(empresas_concorrentes_filtradas)

produtos_conc_filtrados = produtos_conc.loc[[x in ids for x in produtos_conc['id_conc']],produtos_conc.columns[:-1]]
produtos_conc_removidos = produtos_conc.loc[[x not in ids for x in produtos_conc['id_conc']],produtos_conc.columns[:-1]]
todos_produtos = pd.concat([produtos_conc_filtrados,produtos_sebrae])

# produtos_sebrae.to_csv('produtos_sebrae.csv',index = False,encoding = 'ANSI',sep = ';')
# produtos_conc_filtrados.to_csv('produtos_concorrentes.csv',index = False,encoding = 'ANSI',sep = ';')
# produtos_conc_removidos.to_csv('produtos_removidos.csv',index = False,encoding = 'ANSI',sep = ';')
del(produtos_conc_removidos)
del(produtos_conc_filtrados)

todos_produtos['maturidade'] = [convert_float(x) for x in todos_produtos['maturidade']]

todos_produtos['faixa_peco'] = [american_notation(string) for string in todos_produtos['faixa_peco']]

# todos_produtos.to_csv('todos_produtos_filtrados.csv',index = False,encoding = 'ANSI',sep = ';')

produtos = todos_produtos.copy()
concorrentes = concorrentes_filtrados.copy()

del(todos_produtos)
del(concorrentes_filtrados)

print('size produtos:',len(produtos))
produtos_sebrae = produtos.loc[produtos['id_conc'] == codigo_sebrae]
precos_sebrae = np.array(list(filter(lambda x: not np.isnan(x),list(produtos_sebrae['faixa_peco']))))
first_quartile = np.percentile(precos_sebrae,25)
# print('first quartile:',first_quartile)
third_quartile = np.percentile(precos_sebrae,75)
# print('third quartile:',third_quartile)
inter_quartile_range = third_quartile - first_quartile
# print('inter quartile range:',inter_quartile_range)
upper_fence = third_quartile + (1.5 * inter_quartile_range)
# print('upper fence:',upper_fence)
outliers_sebrae = produtos_sebrae[produtos_sebrae['faixa_peco'] > upper_fence]
outliers_sebrae.to_csv('outliers_sebrae.csv',index = False,sep = ';')
print(outliers_sebrae['faixa_peco'])
ids_outliers = list(outliers_sebrae['id_prod'])
produtos = produtos.loc[~((produtos['id_conc'] == codigo_sebrae) & (produtos['faixa_peco'] > upper_fence))].reset_index(drop = True)
print('size produtos:',len(produtos))

produtos['valor_hora'] = produtos['faixa_peco'] / produtos['duração']
produtos['tipo_oferta'] = [legenda_oferta(x) for x in produtos['tipo_oferta']]
produtos['maturidade_legenda'] = [legenda_maturidade(x) for x in produtos['maturidade']]

concorrentes['quantidade_de_cursos'] = None
concorrentes['preco_medio'] = None
concorrentes['preco_std'] = None
concorrentes['duracao_media'] = None
concorrentes['duracao_std'] = None
concorrentes['maturidade_media'] = None
concorrentes['prop_online'] = None

for i in range(len(concorrentes)):
    id = concorrentes.loc[i,'Código']

    quantidade_cursos = len(produtos.loc[produtos['id_conc'] == id])
    concorrentes.loc[i,'quantidade_de_cursos'] = quantidade_cursos

    valores = produtos.loc[produtos['id_conc'] == id,'faixa_peco'].values
    filtrado = np.array(list(filter(lambda x: not np.isnan(x),valores)))
    if len(filtrado) != 0:
        valor_medio = filtrado.mean()
        valor_std = filtrado.std()
    else:
        valor_medio = None
        valor_std = None
    concorrentes.loc[i,'preco_medio'] = valor_medio
    concorrentes.loc[i,'preco_std'] = valor_std

    valores = produtos.loc[produtos['id_conc'] == id,'duração'].values
    filtrado = np.array(list(filter(lambda x: not np.isnan(x),valores)))
    if len(filtrado) != 0:
        valor_medio = filtrado.mean()
        valor_std = filtrado.std()
    else:
        valor_medio = None
        valor_std = None
    concorrentes.loc[i,'duracao_media'] = valor_medio
    concorrentes.loc[i,'duracao_std'] = valor_std

    valores = produtos.loc[produtos['id_conc'] == id,'maturidade'].values
    filtrado = np.array(list(filter(lambda x: not np.isnan(x),valores)))
    if len(filtrado) != 0:
        valor_medio = filtrado.mean()
    else:
        valor_medio = None
    concorrentes.loc[i,'maturidade_media'] = valor_medio

    valores = produtos.loc[produtos['id_conc'] == id,'100% Online'].values
    lista = [x == 'Sim' for x in valores]
    if len(lista) != 0:
        resultado = sum(lista) / len(lista)
    else:
        resultado = None
    concorrentes.loc[i,'prop_online'] = resultado

concorrentes['preco_hora_medio'] = concorrentes['preco_medio'] / concorrentes['duracao_media']
concorrentes['Data de início de atividade'] = [convert_data(data) for data in concorrentes['Data de início de atividade']]
concorrentes['idade'] = [((datetime.now() - data.to_pydatetime()).days) / 365 for data in concorrentes['Data de início de atividade']]

concorrentes.to_csv('concorrentes_parametros.csv',index = False)
produtos.to_csv('produtos_para_analise.csv',index = False)