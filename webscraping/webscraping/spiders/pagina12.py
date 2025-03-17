from datetime import datetime
import scrapy

class NoticiasSpider(scrapy.Spider):
    name = "pagina12"
    start_urls = ["https://www.pagina12.com.ar/"]

    def __init__(self, palabra_clave=None, *args, **kwargs):
        super(NoticiasSpider, self).__init__(*args, **kwargs)
        self.palabra_clave = palabra_clave.lower() if palabra_clave else None

    def parse(self, response):
        for article in response.css("article.headline-card-inner"):
            datos = self.extraer_datos_principales(article, response)

            if self.es_palabra_clave_valida(datos["titulo"]):
                yield scrapy.Request(
                    url=datos["url_noticia"],
                    callback=self.parse_noticia,
                    meta=datos
                )

    def parse_noticia(self, response):
        datos = response.meta
        descripcion, fecha = self.extraer_descripcion_fecha_alternativa(response, datos["descripcion"], datos["fecha"])
        fecha_formateada = self.parsear_fecha(fecha)

        yield {
            "autor": datos["autor"],
            "fecha_publicacion": fecha_formateada,
            "titulo": datos["titulo"],
            "descripcion": descripcion,
            "url_imagen": datos["url_imagen"],
            "url_noticia": datos["url_noticia"]
        }

    def extraer_datos_principales(self, article, response):
        """Extraigo los datos principales de la noticia desde la página de inicio"""
        titulo = article.css("h2.article-title a::text").get()
        descripcion = article.css("span.title-prefix a::text").get()
        autor = article.css("span.article-author a::text").get(default="Desconocido")
        fecha = article.css("time::attr(datetime)").get()
        url_noticia = response.urljoin(article.css("h2.article-title a::attr(href)").get())
        url_imagen = article.css("div.block-multimedia img::attr(src)").get()
        
        return {
            "titulo": titulo.strip() if titulo else "No disponible",
            "descripcion": descripcion.strip() if descripcion else "No disponible",
            "autor": autor,
            "fecha": fecha if fecha else "No disponible",
            "url_imagen": response.urljoin(url_imagen) if url_imagen else "No disponible",
            "url_noticia": url_noticia
        }

    def es_palabra_clave_valida(self, titulo):
        """Verifico si la palabra clave está en el titulo"""
        return not self.palabra_clave or (titulo and self.palabra_clave in titulo.lower())

    def parsear_fecha(self, fecha):
        """Convierto la fecha de formato ISO a formato dd/mm/YYYY HH:M"""
        try:
            fecha_dt = datetime.fromisoformat(fecha) if fecha and fecha != "No disponible" else None
            return fecha_dt.strftime('%d/%m/%Y %H:%M') if fecha_dt else "No disponible"
        except ValueError:
            return "No disponible"

    def extraer_descripcion_fecha_alternativa(self, response, descripcion, fecha):
        """Si la descripción o la fecha estan vacias, las intento extraer de la página de la noticia"""
        if descripcion == "No disponible":
            descripcion = response.css("meta[name='description']::attr(content)").get(default="No disponible")
        if fecha == "No disponible":
            fecha = response.css("time::attr(datetime)").get(default="No disponible")
        return descripcion, fecha
