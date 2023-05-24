import logging
import xml.etree.ElementTree as ET
import csv
from weakref import finalize
from unicodedata import normalize
import re

path_config = "../SRC/config/PC.CFG"

#settando configurações do logging
logging.basicConfig(filename="../LOG/processador_consultas_log.log" ,level=logging.INFO, format="%(asctime)s - %(message)s")

logging.info("Processador de Consultas - Iniciando execucao;")

#Abrindo arquivo de configuração
logging.info(f"Processador de Consultas - Lendo arquivo de configuracao: {path_config}")
pc_cfg = open(path_config, 'r')
instrucoes = []

#Obtendo instruções
logging.info(f"Obtendo Instrucoes do arquivo {path_config}")
for line in pc_cfg:
        split = line.replace("<","").rstrip(">\n ").split('=')
        instrucoes.append(split[1])

logging.info(f"Arquivo a ser lido: {instrucoes[0]}")
logging.info(f"Arquivo para armazenar consultas: {instrucoes[1]}")
logging.info(f"Arquivo para armazenar resultados esperados: {instrucoes[2]}")
pc_cfg.close()

logging.info(f"Iniciando leitura do arquivo {instrucoes[0]}")

arquivo_leia = '../SRC/data/' + str(instrucoes[0])

tree = ET.parse(arquivo_leia)

raiz = tree.getroot()

query_number = raiz.findall('.//QueryNumber')
logging.info(f"Numero de tags QueryNumber obtido: {len(query_number)}")

query_text = raiz.findall('.//QueryText')
logging.info(f"Numero de tags QueryText obtido: {len(query_text)}")

consultas = ["QueryNumber;QueryText\n"]

for i in range(len(query_number)):
        final_query_text = query_text[i].text.replace(";", "").replace("\n", "").replace("   ", " ")
        final_query_text = normalize('NFKD', final_query_text).encode('ASCII','ignore').decode('ASCII')
        final_query_text = re.sub(r"[^\w\s]", "", final_query_text)
        consultas.append(query_number[i].text + ";" + final_query_text.upper() + "\n" )
       # print(consultas[i+1])


logging.info(f"Leitura de {instrucoes[0]} finalizada")

logging.info(f"Criando arquivo {instrucoes[1]}")
arquivo_consultas = "../RESULT/"+instrucoes[1]
with open(arquivo_consultas, 'w', newline='') as consultas_csv:
        consultas_csv.writelines(consultas)
logging.info(f"Criacao do arquivo {instrucoes[1]} finalizada.")

logging.info("Obtendo DocNumber e DocVotes.")

esperados = ["QueryNumber;DocNumber;DocVotes\n"]

registros={}
# Iterar sobre as tags QUERY
for query in raiz.findall('QUERY'):
    query_number = query.find('QueryNumber')
    query_number = query_number.text
    records = []

    # Iterar sobre os itens (registros) dentro da tag RECORDS
    for item in query.find('Records'):
        score = item.get('score')
        doc_votes = len(score) - score.count("0")
        esperados.append(query_number + ";" + item.text + ";" + str(doc_votes) + "\n")

logging.info(f"Iniciando criacao do arquivo {instrucoes[2]}")
arquivo_esperados = "../RESULT/"+instrucoes[2]
with open(arquivo_esperados, 'w',  newline='') as esperados_csv:
        esperados_csv.writelines(esperados)

esperados_csv.close()
logging.info(f"Criacao do arquivo {instrucoes[2]} finalizada.")

logging.info("Processador de consultas - Finalizando execucao.")

