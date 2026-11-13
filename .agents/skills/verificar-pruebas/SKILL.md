---
name: verificar-pruebas
description: Comprueba PrestaLab con unittest, SQLite temporal y comandos de consola reproducibles.
---

# Verificar pruebas

1. Vincula cada criterio relevante a una prueba. Para las transiciones, revisa el estado guardado además del mensaje de la consola.
2. Usa bases temporales y fechas explícitas. Ejecuta `python -B -m unittest discover -s tests -v` desde la carpeta del taller.
3. Informa cuántas pruebas ejecutaste y el resultado real. Ante un fallo, registra el comando o caso mínimo, el resultado esperado y el observado.
