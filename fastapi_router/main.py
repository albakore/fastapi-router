import os
from fastapi import FastAPI
import inspect
import importlib
import pathlib

methods = ['GET','POST','PUT','PATCH','DELETE','OPTIONS','TRACE','HEAD']


def obtenerTag(modulo):
	try: return getattr(modulo,'TAGS')
	except: return ''

def obtenerNombre(funcion):
	nombre = inspect.getcomments(funcion)
	if nombre:
		nombre = nombre.replace('@name:','')
		return nombre
	return funcion.__name__

def init_main_route(app : FastAPI,pathDir : str = 'api',nameRouteFile : str = 'route'):
	for x in os.walk(pathDir):
		path = x[0].replace('\\','/')
		if f'{nameRouteFile}.py' in x[2] :
			try:
				modulo = importlib.import_module(path.replace('/','.')+f'.{nameRouteFile}')
				for index, method in enumerate(methods):
					try:
						funcion = getattr(modulo,method)
						tags = obtenerTag(modulo)
						name = obtenerNombre(funcion)
						app.add_api_route(f'/{path}',endpoint=funcion,methods=[method],tags=[tags],name=name,)
					except: ...
			except: ...

			