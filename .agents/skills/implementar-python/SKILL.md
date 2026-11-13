---
name: implementar-python
description: Implementa o revisa cambios de PrestaLab en la consola Python y la persistencia SQLite.
---

# Implementar en Python

1. Conserva la interfaz de `prestalab.py` y concentra las reglas de negocio en `prestamos.py`.
2. Usa parámetros SQL para los datos de entrada. Mantén la restricción de préstamo activo en la base y la devolución condicionada a un préstamo abierto.
3. Expón los errores esperados como `ValueError` en la capa de negocio para que la consola responda con código 1. Entrega al coordinador los cambios y el comando que usaste para comprobarlos.
