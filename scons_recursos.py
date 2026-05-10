# -*- coding: utf-8 -*-
# scons_recursos.py
#
# Script para compilar archivos .po a .mo y generar metadatos localmente.
# Compatible con el sistema de ActualizadorRecursos.
#
# Uso independiente:
#   python scons_recursos.py
#   python scons_recursos.py --directorio-idiomas addon/locale
#   python scons_recursos.py --solo-idiomas
#   python scons_recursos.py --solo-docs
#
# Uso con SCons (añadir al sconstruct):
#   import scons_recursos
#   scons_recursos.integrarConSCons(env)
#
# Licencia: GPL v2

import os
import sys
import subprocess
import hashlib
import json
from datetime import datetime, timezone


DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_LOCALE = os.path.join(DIR_BASE, "addon", "locale")
DIR_DOC = os.path.join(DIR_BASE, "addon", "doc")
ARCHIVO_INFO = "recursos_info.json"


def buscarMsgfmt() -> str:
	"""
	Busca el ejecutable msgfmt en el sistema.

	Returns:
		str: Ruta al ejecutable msgfmt.

	Raises:
		FileNotFoundError: Si no se encuentra msgfmt.
	"""
	try:
		resultado = subprocess.run(
			["msgfmt", "--version"], capture_output=True, text=True,
		)
		if resultado.returncode == 0:
			return "msgfmt"
	except FileNotFoundError:
		pass

	rutas_posibles = [
		os.path.join(os.environ.get("ProgramFiles", ""), "gettext", "bin", "msgfmt.exe"),
		os.path.join(os.environ.get("ProgramFiles(x86)", ""), "gettext", "bin", "msgfmt.exe"),
		os.path.join(os.environ.get("ProgramFiles", ""), "Git", "usr", "bin", "msgfmt.exe"),
		r"C:\msys64\usr\bin\msgfmt.exe",
	]

	for ruta in rutas_posibles:
		if os.path.exists(ruta):
			return ruta

	raise FileNotFoundError(
		"No se encontró 'msgfmt'. Instala gettext:\n"
		"  Windows: https://mlocati.github.io/articles/gettext-iconv-windows.html\n"
		"  Linux:   sudo apt-get install gettext\n"
		"  Mac:     brew install gettext"
	)


def compilarPO(ruta_po: str, ruta_mo: str, msgfmt: str = "msgfmt") -> bool:
	"""Compila un archivo .po a .mo."""
	os.makedirs(os.path.dirname(ruta_mo), exist_ok=True)
	try:
		r = subprocess.run([msgfmt, "-o", ruta_mo, ruta_po], capture_output=True, text=True)
		if r.returncode != 0:
			print(f"  ✗ Error: {r.stderr.strip()}")
			return False
		return True
	except Exception as e:
		print(f"  ✗ Excepción: {e}")
		return False


def hashDirectorio(directorio: str, extensiones: list) -> list:
	"""Calcula hashes SHA-256 de archivos filtrados por extensión."""
	resultados = []
	if not os.path.exists(directorio):
		return resultados
	for raiz, _, archivos in os.walk(directorio):
		for archivo in sorted(archivos):
			if any(archivo.endswith(ext) for ext in extensiones):
				ruta = os.path.join(raiz, archivo)
				h = hashlib.sha256(open(ruta, "rb").read()).hexdigest()
				rel = os.path.relpath(ruta, directorio).replace(os.sep, "/")
				resultados.append(f"{h}  {rel}")
	return resultados


def generarMetadatos(
	dir_locale: str = DIR_LOCALE,
	dir_doc: str = DIR_DOC,
	nombre: str = "",
	ext_idiomas: list = None,
	ext_docs: list = None,
) -> dict:
	"""
	Genera metadatos combinados de idiomas y documentación.

	Args:
		dir_locale: Directorio de locales.
		dir_doc: Directorio de documentación.
		nombre: Nombre del complemento.
		ext_idiomas: Extensiones de archivos de idiomas.
		ext_docs: Extensiones de archivos de documentación.

	Returns:
		dict con hash_combinado, fecha, idiomas_locale, idiomas_doc.
	"""
	if ext_idiomas is None:
		ext_idiomas = [".mo", ".ini"]
	if ext_docs is None:
		ext_docs = [".html", ".md", ".txt"]

	hashes = []
	idiomas_locale = set()
	idiomas_doc = set()

	# Archivos de idiomas
	for item in hashDirectorio(dir_locale, ext_idiomas):
		hashes.append(f"locale/{item.split('  ', 1)[1]}")
		hashes.append(item)
		partes = item.split("  ", 1)[1].split("/")
		if partes:
			idiomas_locale.add(partes[0])

	# Archivos de documentación
	for item in hashDirectorio(dir_doc, ext_docs):
		hashes.append(f"doc/{item.split('  ', 1)[1]}")
		hashes.append(item)
		partes = item.split("  ", 1)[1].split("/")
		if partes:
			idiomas_doc.add(partes[0])

	contenido = "\n".join(sorted(hashes))
	hash_total = hashlib.sha256(contenido.encode()).hexdigest() if hashes else ""

	return {
		"hash_combinado": hash_total,
		"fecha": datetime.now(timezone.utc).isoformat(),
		"complemento": nombre,
		"idiomas_locale": sorted(idiomas_locale),
		"idiomas_doc": sorted(idiomas_doc),
	}


def compilarRecursos(
	dir_locale: str = None,
	dir_doc: str = None,
	nombre: str = "",
	generar_info: bool = True,
	compilar_po: bool = True,
) -> tuple:
	"""
	Compila todos los .po a .mo y genera metadatos.

	Args:
		dir_locale: Directorio de locales (defecto: addon/locale).
		dir_doc: Directorio de documentación (defecto: addon/doc).
		nombre: Nombre del complemento para metadatos.
		generar_info: Si True, genera el archivo recursos_info.json.
		compilar_po: Si True, compila archivos .po a .mo.

	Returns:
		(compilados, errores): Conteo de resultados.
	"""
	if dir_locale is None:
		dir_locale = DIR_LOCALE
	if dir_doc is None:
		dir_doc = DIR_DOC

	print("=" * 60)
	print("  Compilación de recursos para complemento NVDA")
	print("=" * 60)

	compilados = 0
	errores = 0

	# Compilar .po a .mo
	if compilar_po and os.path.exists(dir_locale):
		try:
			msgfmt = buscarMsgfmt()
			print(f"\nUsando msgfmt: {msgfmt}")
		except FileNotFoundError as e:
			print(f"\nERROR: {e}")
			return (0, 1)

		print(f"Directorio de idiomas: {dir_locale}\n")

		for raiz, _, archivos in os.walk(dir_locale):
			for archivo in sorted(archivos):
				if archivo.endswith(".po"):
					ruta_po = os.path.join(raiz, archivo)
					ruta_mo = os.path.join(raiz, os.path.splitext(archivo)[0] + ".mo")
					rel = os.path.relpath(ruta_po, dir_locale)
					print(f"Compilando: {rel}")
					if compilarPO(ruta_po, ruta_mo, msgfmt):
						compilados += 1
						print(f"  ✓ OK ({os.path.getsize(ruta_mo):,} bytes)")
					else:
						errores += 1

	# Resumen de documentación
	if os.path.exists(dir_doc):
		n_docs = sum(
			1 for r, _, fs in os.walk(dir_doc)
			for f in fs if f.endswith((".html", ".md", ".txt"))
		)
		print(f"\nDocumentación encontrada: {n_docs} archivos")

	print(f"\n{'─' * 60}")
	print(f"Traducciones: {compilados} compiladas, {errores} errores")
	print(f"{'─' * 60}")

	# Generar metadatos
	if generar_info:
		print("\nGenerando metadatos...")
		meta = generarMetadatos(dir_locale, dir_doc, nombre)
		ruta_info = os.path.join(os.path.dirname(dir_locale), ARCHIVO_INFO)
		with open(ruta_info, "w", encoding="utf-8") as f:
			json.dump(meta, f, ensure_ascii=False, indent="\t")
		print(f"  Hash: {meta['hash_combinado']}")
		print(f"  Idiomas (locale): {', '.join(meta['idiomas_locale']) or 'ninguno'}")
		print(f"  Idiomas (doc): {', '.join(meta['idiomas_doc']) or 'ninguno'}")
		print(f"  Archivo: {ruta_info}")

	return (compilados, errores)


def integrarConSCons(env):
	"""
	Integra la compilación con SCons. Añadir al sconstruct:
		import scons_recursos
		scons_recursos.integrarConSCons(env)
	"""
	try:
		sys.path.insert(0, DIR_BASE)
		import buildVars
		nombre = buildVars.addon_info.get("addon_name", "")
	except ImportError:
		nombre = ""

	compilarRecursos(nombre=nombre)


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(
		description="Compilar recursos (.po → .mo) y generar metadatos",
	)
	parser.add_argument("--directorio-idiomas", "-i", default=DIR_LOCALE)
	parser.add_argument("--directorio-docs", "-d", default=DIR_DOC)
	parser.add_argument("--nombre", "-n", default="")
	parser.add_argument("--sin-info", action="store_true", help="No generar metadatos")
	parser.add_argument("--solo-idiomas", action="store_true", help="Solo compilar idiomas")
	parser.add_argument("--solo-docs", action="store_true", help="Solo listar documentación")

	args = parser.parse_args()

	compilados, errores = compilarRecursos(
		dir_locale=args.directorio_idiomas,
		dir_doc=args.directorio_docs,
		nombre=args.nombre,
		generar_info=not args.sin_info,
		compilar_po=not args.solo_docs,
	)

	sys.exit(1 if errores > 0 else 0)
