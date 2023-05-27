IMPLEMENTAÇÃO DE UM SISTEMA DE RECUPERAÇÃO EM MEMÓRIA SEGUNDO O MODELO VETORIAL - INSERÇÃO STEMMER

Os códigos devem ser executados na seguinte orgem:
	1 - processador_consultas.py
	2 - gerador_lis_invertida.py
	3 - indexador.py
	4 - buscador.pu
	
Na pasta SRC é possível encontrar os arquivos acima, bem como as pastas data e config.

No diretório 'data' são armazenados os arquivos xml utilizados:
	* cf74.xml;
	* cf75.xml;
	* cf76.xml;
	* cf77.xml;
	* cf78.xml;
	* cf79.xml;
	* cfquery.xml;

No diretório 'config' estão armazenados os arquivos de configuração utilizados em cada módulo:
	* PC.CFG
	* GLI.CFG
	* INDEX.CFG
	* BUSCA.CFG
	
Na raiz existem duas pastas 'RESULT' e 'LOG'.

No diretório 'LOG' estão armazenados os logs de cada módulo:
	* processaor_consultas_log.log
	* indexador_log.log
	* gerador_lista_invertida_log.log
	* buscador_log.log
	
No diretório 'RESULT' estão armazenados os arquivos gerados por cada módulo:
	* consultas.csv
	* esperados.csv
	* lista_invertida.csv
	* modelo_vetorial.csv
	* resultados.csv
	
O modo como os arquivos modelo_vetorial.csv e resultados.csv estão estruturados é descrito no arquivo 'MODELO.DOC'


Módulo STEMMER
Após a inserção, é preciso inserir o termo 'STEMMER' ou 'NOSTEMMER' nos arquivos de configuração abaixo:
	* GLI.CFG
	* INDEX.CFG
	* BUSCA.CFG
	* AVALIA.CFG

O arquivo AVALIA.CFG foi criado neste módulo a fim de controlar os métodos de avaliação do Método de avaliação previamente desenvolvido.

O diretório 'AVALIA' possui os gráficos e csv já obtidos. A aplicação já foi compilada para o STEMMER e NOSTEMMER