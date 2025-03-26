# Nota
## Librerias instaladas
```pip install scrapy-user-agents```

Para poder instalar los middlewares y cumplir con las paginas

```pip install marshmallow```

Para la creacion de los serializers, para validar si es articulo esta repetido

## Instalando Scrpy
Se debe eejecutar

```pip install scrapy```
## Crenado el proyecto
Para inciar el proyecto no se pudo hacer lo que el docente hizo, sino se ejceuto el siguiente comando:

```python -m scrapy startproject tarea_1```

Esto se puede deber a que se tiene anaconda instalado


## Creacion del spyder
```python -m scrapy genspider [spyderName] [urlToSpyder]```

## Ejecucion del spyder
```python -m scrapy crawl [spyderName] -o [fileResult].json```

Para los spyders que existen en el proyecto seria el siguiente comando:

```python -m scrapy crawl wiredSpyder -o wired.json```
```python -m scrapy crawl firstSpyder -o thenextweb.json```
```python -m scrapy crawl paradeSpyder -o parade.json```