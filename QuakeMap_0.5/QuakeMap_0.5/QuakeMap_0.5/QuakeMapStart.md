#		GUIA QUAKEMAP

#	0	Necesario internet para su funcionamiento y navegador con javascript activado

#	0	Instalar todas las dependencias

		sudo apt-get install gunicorn python-gunicorn
		pip3 install zmq
		pip3 install scrapy
		pip3 install dropbox
		pip3 install gmplot
		pip3 install bottle
		pip3 install beautifulsoup4

#	Pasos para ejecutar el sistema QuakeMap en la misma maquina

#	1	Posicionate en el directorio raiz: cd QuakeMap_version 	
#	2	Arranca Server: python3 Scraping/StartServer.py
#	3	Arrancar 4 workers: python3 Scraping/StartWorkers.py 4
#	4	Arrancar StartClients: python3 Scraping/StartClients.py
#	5	Arrancar WebServer: cd WebServer && gunicorn -w 4 -b ipServidorWeb:puerto webServer:app
#	5	Arrancar Intermediario: python3 WebServer/intermediario.py
