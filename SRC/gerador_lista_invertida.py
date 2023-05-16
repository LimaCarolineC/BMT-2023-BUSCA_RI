import logging
import csv
import xml.etree.ElementTree as ET
import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string

path_config = "../SRC/config/GLI.CFG"
stopwords_idioma = stopwords.words('english')
stopwords_idioma.extend(["et", "al"])

logging.basicConfig(filename="../LOG/gerador_lista_invertida_log.log" ,level=logging.INFO, format="%(asctime)s - %(message)s")

logging.info("Gerador de Lista Invertida - Iniciando execucao")

#Abrindo arquivo de configuração
logging.info(f"Processador de Consultas - Lendo arquivo de configuracao: {path_config}")
gli_cfg = open(path_config, 'r')

lista_leia = []
lista_escreva = []

#Obtendo instruções
logging.info(f"Obtendo Instrucoes do arquivo {path_config}")
for line in gli_cfg:
    split = line.replace("<","").rstrip(">\n ").split('=')
    if split[0]=="LEIA":
        lista_leia.append(split[1])
    if split[0]=="ESCREVA":
        lista_escreva.append(split[1])
gli_cfg.close()

logging.info(f"Quantidade de instrucoes do arquivo config: {len(lista_leia)+len(lista_escreva)}")
logging.info(f"Quantidade de arquivos a serem lidos: {len(lista_leia)}")

lista_palavras = {}

for doc in lista_leia:
    arquivo_leia = "../SRC/data/"+str(doc)
    logging.info(f"Iniciando leitura do arquivo: {arquivo_leia}.")
    tree = ET.parse(arquivo_leia)
    raiz = tree.getroot()
    record_lista = raiz.findall(".//RECORD")

    for record in range(len(record_lista)):
        record_num = record_lista[record].find("RECORDNUM").text
        record_num = int(record_num.lstrip('0'))
        abstract = record_lista[record].find("ABSTRACT")

        if abstract is None:
            abstract = record_lista[record].find("EXTRACT")
        if abstract is None:
            continue

        abstract = abstract.text
        abstract_limpa = re.sub("[^a-zA-Z]+", " ", abstract)
        abstract_limpa = nltk.word_tokenize(abstract_limpa)

        for palavra in abstract_limpa:
            if(palavra.lower() not in stopwords_idioma and
                    palavra.lower() not in string.punctuation and not palavra.isdigit() and len(palavra.lower())>=2):
                if palavra.upper() in lista_palavras.keys():
                    lista_palavras[palavra.upper()].append(record_num)
                    continue
                lista_palavras[palavra.upper()] = [record_num]
        logging.info(f"Leitura do ABSTRACT/EXTRACT do documento {record_num} finalizada.")
    logging.info(f"Leitura do arquivo {arquivo_leia} finalizada, foram lidos {len(record_lista)} documentos.")

logging.info("Iniciando geracao de lista invertida:")
path_escreva = "..//RESULT/"+lista_escreva[0]

lista_invertida = []

for word, documents_list in lista_palavras.items():
    lista_invertida.append(word + ";" + str(documents_list)+"\n")

with open(path_escreva, 'w', newline='') as escreva_csv:
    escreva_csv.writelines(lista_invertida)

logging.info("Geracao de lista invertida finalizada.")
logging.info("Gerador de Lista Invertida - Execucao finalizada!")

