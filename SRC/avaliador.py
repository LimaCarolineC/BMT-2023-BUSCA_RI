import logging
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
from nltk.metrics import precision, recall, f_measure
import math
import numpy as np

logging.basicConfig(filename="../LOG/avaliador_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")
logging.info("Avaliacao de um modelo de RI - Iniciando Execucao")

path_config = "../SRC/config/AVALIA.CFG"

recall_onze_dic = {"0": 0, "10": 0, "20": 0, "30": 0, "40": 0, "50": 0,
                   "60": 0, "70": 0, "80": 0, "90": 0, "100": 0}
r_precision_dic = {}

dcg = [0]*10
media_dcg = [0]*10
ndcg = [0]*10

MAP = []

precisions = ["QueryNumber;Precision@5;Precision@10;F1\n"]

onze_consultas = np.arange(0, 101, 10)
onze_consultas_df = pd.DataFrame(onze_consultas, columns=['Recall'])

stemmer_option = False

logging.info(f"Avaliacao - Iniciando leitura do arquivo de configuracao: {path_config};")
busca_cf = open(path_config, 'r')
config = {}

logging.info(f"Obtendo informacoes do arquivo: {path_config};")
for line in busca_cf:
    if not ("=" in line):
        if line.replace("\n", "").replace(" ", "") == "STEMMER":
            stemmer_option = True
            logging.info("STEMMER OPTION ATIVADA!")
    else:
        split = line.replace("<", "").replace(">", "").replace("\n", "").split("=")
        config[split[0]] = split[1]
        logging.info(f"Leitura Instrucao {split[1]} ok;")

busca_cf.close()
logging.info(f"Obtencao as informacoes do arquivo: {path_config} finalizada;")

path_esperados = "../RESULT/" + config["ESPERADOS"]

logging.info(f"Iniciando leitura do arquivo: {path_esperados};")

with open(path_esperados) as esperados_csv:
    next(esperados_csv)
    esperados_dic = {}
    anterior = 1
    doc_list = []

    for linha in esperados_csv:
        linha = linha.rstrip()
        query_number, doc, doc_votes = linha.split(";")
        query_number = int(query_number)

        if query_number == anterior:
            doc_list.append(int(doc))
        else:
            esperados_dic[anterior] = doc_list
            anterior = query_number
            doc_list = []
            doc_list.append(int(doc))
            esperados_dic[anterior] = doc_list

esperados_csv.close()

logging.info(f"Leitura do arquivo {path_esperados} finalizada.")

path_resultados = config["RESULTADOS"] + "-STEMMER.csv" if stemmer_option else config['RESULTADOS'] + "-NOSTEMMER.csv"
path_resultados = "../RESULT/" + path_resultados

logging.info(f"Iniciando leitura do arquivo {path_resultados}")

with open(path_resultados) as resultados_csv:
    next(resultados_csv)
    resultados_dic = {}
    anterior = 1
    doc_list = []

    for linha in resultados_csv:
        linha = linha.rstrip()
        query_number, raking, doc, similaridade = linha.split(";")
        query_number = int(query_number)

        if query_number == anterior:
            if similaridade != '0':
                doc_list.append(int(doc))
        else:
            resultados_dic[anterior] = doc_list
            anterior = query_number
            doc_list = []
            doc_list.append(int(doc))
            resultados_dic[anterior] = doc_list

resultados_csv.close()

logging.info(f"Leitura do arquivo {path_resultados} finalizada.")

logging.info("Iniciando os calculos de Revocacao e Precisao para o grafico de 11 pontos")


def interpola(onze_parcial):
    lista_nulo = []
    lim_inf = 0
    for i in range(0, 101, 10):
        if (onze_parcial[str(i)] == 0):
            lista_nulo.append(i)
        else:
            for l in lista_nulo:
                # estou settando os valores do max até agora nos que estavam nulos
                onze_parcial[str(l)] = onze_parcial[str(i)]
                lista_nulo = []

    return onze_parcial.values()


def revocacao(VP, FN):
    if (VP + FN) == 0:
        return 0
    else:
        R = VP / (VP + FN)
        r = round(R, 2)
        return r


def precisao(VP, FP):
    if (VP + FP) == 0:
        return 0
    else:
        P = VP / (VP + FP)
        return round(P, 2)


def atualiza_11_pontos(recall, precision):
    if recall < 0.1:
        if precision > recall_onze_dic["0"]:
            recall_onze_dic["0"] = round(precision * 100)

        else:
            recall_onze_dic["0"] = recall_onze_dic["0"]

    if recall >= 0.1 and recall < 0.2:
        if precision > recall_onze_dic["10"]:
            recall_onze_dic["10"] = round(precision * 100)

        else:
            recall_onze_dic["10"] = recall_onze_dic["10"]

    if recall >= 0.2 and recall < 0.3:
        if precision > recall_onze_dic["20"]:
            recall_onze_dic["20"] = round(precision * 100)
        else:
            recall_onze_dic["20"] = recall_onze_dic["20"]

    if recall >= 0.3 and recall < 0.4:
        if precision > recall_onze_dic["30"]:
            recall_onze_dic["30"] = round(precision * 100)
        else:
            recall_onze_dic["30"] = recall_onze_dic["30"]

    if recall >= 0.4 and recall < 0.5:
        if precision > recall_onze_dic["40"]:
            recall_onze_dic["40"] = round(precision * 100)
        else:
            recall_onze_dic["40"] = recall_onze_dic["40"]

    if recall >= 0.5 and recall < 0.6:
        if precision > recall_onze_dic["50"]:
            recall_onze_dic["50"] = round(precision * 100)
        else:
            recall_onze_dic["50"] = recall_onze_dic["50"]

    if recall >= 0.6 and recall < 0.7:
        if precision > recall_onze_dic["60"]:
            recall_onze_dic["60"] = round(precision * 100)
        else:
            recall_onze_dic["60"] = recall_onze_dic["60"]

    if recall >= 0.7 and recall < 0.8:
        if precision > recall_onze_dic["70"]:
            recall_onze_dic["70"] = round(precision * 100)
        else:
            recall_onze_dic["70"] = recall_onze_dic["70"]

    if recall >= 0.8 and recall < 0.9:
        if precision > recall_onze_dic["80"]:
            recall_onze_dic["80"] = round(precision * 100)
            pre = recall_onze_dic["80"]
        else:
            recall_onze_dic["80"] = recall_onze_dic["80"]
            pre = recall_onze_dic["80"]

    if recall >= 0.9 and recall < 1:
        if precision > recall_onze_dic["90"]:
            recall_onze_dic["90"] = round(precision * 100)
        else:
            recall_onze_dic["90"] = recall_onze_dic["90"]

    if recall == 1:
        if precision > recall_onze_dic["100"]:
            recall_onze_dic["100"] = round(precision * 100)
        else:
            recall_onze_dic["100"] = recall_onze_dic["100"]


def calcula_revoc_pre_onze(relevantes, recuperados):
    relevantes_num = 0
    VP = 0
    FP = 0
    FN = 0
    precision_five = 0
    precision_ten = 0
    F = 0
    r_precision = 0
    precision_r = 0
    map_interna = []
    rank = 0
    mrr_interno = 0

    for doc in recuperados:
        precision_five = precision_five + 1
        precision_ten = precision_ten + 1
        rank = rank + 1

        if doc in relevantes:
            relevantes_num = relevantes_num + 1
            r_precision = r_precision + 1
            VP = VP + 1
            FN = len(relevantes) - relevantes_num

            recall = revocacao(VP, FN)
            precision = precisao(VP, FP)

            atualiza_11_pontos(recall, precision)
            map_interna.append(precision)

            mrr_interno = mrr_interno + (1/rank)

        else:
            FP = FP + 1
            FN = len(relevantes) - relevantes_num
            recall = revocacao(VP, FN)
            precision = precisao(VP, FP)

            atualiza_11_pontos(recall, precision)

        if precision_five == 5:
            precision_five = precisao(VP, FP)

        if precision_ten == 10:
            recall_ten = revocacao(VP, FN)
            precision_ten = precisao(VP, FP)

        if r_precision == 5:
            precision_r = precisao(VP, FP)

        if rank <= 10:
            if rank == 1:
                dcg[rank - 1] = (2 ** relevantes_num - 1) / (math.log(1 + rank))
                continue
            dcg[(rank - 1)] = dcg[(rank - 2)] + (2 ** relevantes_num - 1) / (math.log(1 + rank))

    F = calcular_F(recall, precision)
    map_p = np.mean(map_interna)

    return round(precision_ten,2), round(precision_five,2), round(F,2), precision_r, map_p, mrr_interno


def calcular_F(recall, precision):
    F = 2 * ((precision*recall)/(precision+recall))
    return F


def plotar_grafico_onze():
    # Plotar o gráfico de linha
    plt.plot(onze_consultas_df['Recall'], onze_consultas_df[f'p_C(Media)'], marker='o', linestyle='-', color='#880088')

    # Configurações do gráfico
    plt.title('Gráfico de 11 pontos de precisão e recall')
    plt.xlabel('Revocação (%)')
    plt.ylabel('Precisão (%)')
    plt.ylim(0, 110)
    plt.xlim(0, 100)
    plt.xticks(range(0, 101, 10))
    plt.yticks(range(0, 101, 10))

    # Exibir o gráfico
    #plt.show()
    stemmer_text = "-STEMMER-1" if stemmer_option else "-NOSTEMMER-2"
    path_save_file = "../AVALIA/" + config["GRAFICOONZE"] + stemmer_text.lower() + ".pdf"
    plt.savefig(path_save_file)
    plt.clf()


def plotar_histograma_r_precision():
    # Criar o histograma
    plt.hist(r_precision_dic.values(), bins=20, color='green', edgecolor='black')

    # Definir os rótulos e o título do gráfico
    plt.title('Histograma de R-Precision (comparativo)')

    # Exibir o histograma
    #plt.show()
    stemmer_text = "-STEMMER-1" if stemmer_option else "-NOSTEMMER-2"
    path_save_file = "../AVALIA/" + config["RPRECISION"] + stemmer_text.lower() + ".pdf"
    plt.savefig(path_save_file)
    plt.clf()

def gerar_csv_precisions():
    stemmer_text = "-STEMMER-1" if stemmer_option else "-NOSTEMMER-2"
    precisions_path = "../AVALIA/" + config["PRECISIONS"] + stemmer_text.lower() + ".csv"
    with open(precisions_path, 'w', newline='') as precisions_csv:
        precisions_csv.writelines(precisions)

    precisions_csv.close()

def gerar_map_mrr(MAP_externo, mrr_externo):
    MRR = (1/len(esperados_dic))*mrr_externo
    MAP = np.mean(MAP_externo)

    MRR = np.round(MRR)
    MAP = np.round(MAP)

    map_mrr_text = ["MAP;MRR\n"]
    map_mrr_text.append(str(MAP)+";"+str(MRR)+"\n")

    stemmer_text = "-STEMMER-1" if stemmer_option else "-NOSTEMMER-2"
    map_mrr_path = "../AVALIA/" + config["MAPMRR"] + stemmer_text.lower() + ".csv"
    with open(map_mrr_path, 'w', newline='') as map_mrr_csv:
        map_mrr_csv.writelines(map_mrr_text)

def gerar_dcg():
    for i in range(len(dcg)):
        media_dcg[i] = media_dcg[i] + dcg[i] / 100

    x = list(range(1,11))
    plt.plot(x, media_dcg, color='blue', linestyle='solid', linewidth=3, marker='o', markerfacecolor='black', markersize=6, label='DCG')

    plt.ylim(0, 1)
    plt.xlim(1, 10)
    plt.xlabel('Ranking 10')
    plt.ylabel('DCG')
    plt.title('Discounted Cumulative Gain (médio)')

    stemmer_text = "-STEMMER-1" if stemmer_option else "-NOSTEMMER-2"
    path_save_file = "../AVALIA/" + config["DCGNDCG"] + stemmer_text.lower() + ".pdf"
    plt.savefig(path_save_file)
    #plt.show()
    plt.clf()

for row in resultados_dic.keys():
    recall_onze_dic = {"0": 0, "10": 0, "20": 0, "30": 0, "40": 0, "50": 0,
                       "60": 0, "70": 0, "80": 0, "90": 0, "100": 0}

    logging.info(f"iniciando avaliacoes da consulta {row}.")
    pre_ten, pre_five, f_one, r_pre, map_externa, mrr_externo = calcula_revoc_pre_onze(esperados_dic[row], resultados_dic[row])

    r_precision_dic[row] = r_pre

    MAP.append(map_externa)

    precisions.append(str(row)+";"+str(pre_ten)+";"+str(pre_five)+";"+str(f_one)+"\n")
    interpolados = {}
    interpolados = interpola(recall_onze_dic)
    onze_consultas_df[f'p_C{row}'] = interpolados
    logging.info(f"Avaliacoes da consulta {row} finalizadas.")

onze_consultas_df[f'p_C(Media)'] = onze_consultas_df.iloc[:, 1:(onze_consultas_df.shape[1] - 1)].mean(axis=1)

logging.info("Plotanfo grafico de 11 pontos.")
plotar_grafico_onze()
logging.info("Plotando histograma r-precision.")
plotar_histograma_r_precision()
logging.info("Gerando Precision5, Precision 10 e F1")
gerar_csv_precisions()
logging.info("Gerando MAP e MRR.")
gerar_map_mrr(MAP, mrr_externo)
logging.info("Plotando DCG e NDCG.")
gerar_dcg()

logging.info("Avaliacao de um modelo de RI - Execucao Finalizada.")