import logging
import pandas as pd

logging.basicConfig(filename="../LOG/avaliador_log.log", level=logging.INFO, format="%(asctime)s - %(messaage)s")
logging.info("Avaliacao de um modelo de RI - Iniciando Execucao")

path_esperados = "../RESULT/"+"esperados.csv"

logging.info(f"Iniciando leitura do arquivo: {path_esperados};")

esperados_csv = pd.read_csv(path_esperados, sep=";", encoding="utf_8")
esperados_csv.columns = ['QueryNumber', 'DocNumber', 'DocVotes']

logging.info(f"Tratando dados obtidos do {path_esperados}")

for line in esperados_csv.iterrows():
    query_number, doc_number, doc_votes = line.split(";")