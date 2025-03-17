Este proyecto es un scraper de noticias desarrollado con Scrapy, diseñado para extraer artículos de un portal de noticias en función de una palabra clave ingresada por el usuario.
El scraper accede a un sitio de noticias, busca artículos que contengan la palabra clave proporcionada por el usuario, y extrae información clave de cada noticia, incluyendo:

Título,
Descripción,
Autor, si está disponible,
Fecha, y hora de publicación
URL de la noticia para acceder al artículo completo,
URL de la noticia

Los datos extraídos se guardan en un archivo CSV (noticias.csv).
El scraper fue diseñado buscando evitar bloqueos por parte del sitio web, respetando el archivo robots.txt, utilizando encabezados User-Agent adecuados y estableciendo tiempos de espera entre solicitudes.

Para ejecutar el proyecto localmente es necesario seguir los siguientes pasos:
pip install -r requirements.txt
ingresar a la subcarpeta dentro del proyecto, webscraping y ejecutar por terminal el siguiente comando
scrapy crawl pagina12 -a palabra_clave="milei", o la palabra por la que se desee filtrar
