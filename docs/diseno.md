# Diseño de PrestaLab

El encargado de un laboratorio puede registrar equipos, prestar uno a una persona, devolverlo y consultar los préstamos que siguen abiertos. Cada préstamo registra su fecha de inicio y la fecha límite acordada.

| Acción | Criterio de aceptación |
| --- | --- |
| Registrar | Un código identifica un solo equipo. Se recortan espacios y el código se guarda en mayúsculas. El código, nombre y responsable son obligatorios donde corresponden. |
| Prestar | El equipo debe existir y estar disponible. Solo puede tener un préstamo abierto. El límite puede coincidir con la fecha de inicio o ser posterior. |
| Devolver | La devolución cierra el préstamo activo y conserva el historial. La fecha de devolución debe ser igual o posterior al inicio. Se puede prestar nuevamente el mismo equipo. |
| Listar | Aparecen solo préstamos abiertos, ordenados por fecha límite y código. En la fecha límite el préstamo está vigente y al día siguiente queda vencido. |

Las fechas ingresadas siguen el formato `AAAA-MM-DD`. Si se omite la fecha de inicio, devolución o consulta, se usa la fecha local. Las fechas explícitas permiten introducir registros históricos o reproducir una demostración.

## Estructura

- `prestalab.py` recibe los comandos con `argparse` y muestra resultados. Los errores de negocio o de acceso a SQLite devuelven código 1. Los argumentos inválidos devuelven código 2.
- `prestamos.py` contiene las transiciones y usa SQLite. Una clave primaria protege los códigos y un índice único parcial impide dos préstamos abiertos para el mismo equipo. La devolución actualiza únicamente la fila que sigue abierta y cumple la fecha.
- `tests/test_prestamos.py` comprueba las reglas de negocio y un recorrido real por la consola con bases temporales.

Al usar `Prestamos` desde Python, inicializa el registro con una conexión sin transacciones activas. SQLite solo permite activar la validación de claves foráneas fuera de una transacción.

Los préstamos cerrados permanecen en SQLite. La consulta de la consola muestra los activos.
