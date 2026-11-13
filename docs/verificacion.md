# Verificación de PrestaLab

## Pruebas del programa

La suite se ejecutó con Python 3.12 desde la carpeta del taller:

```powershell
python -B -m unittest discover -s tests -v
```

```text
Ran 10 tests
OK
```

La línea de duración se omite en el extracto porque varía entre ejecuciones.

| Pruebas | Comportamiento observado |
| --- | --- |
| Registro | El código se normaliza. Se rechazan códigos duplicados y campos vacíos. |
| Préstamo | Se rechazan equipos inexistentes y segundos préstamos activos. Se acepta un límite igual a la fecha de inicio. |
| Consulta | El préstamo permanece vigente hasta la fecha límite. Cambia a vencido al día siguiente y se ordena por fecha y código. |
| Devolución | Una fecha anterior al inicio se rechaza. La devolución válida conserva el historial y permite volver a prestar el equipo. |
| Consola | Los datos persisten entre procesos. Los errores de negocio y formato devuelven códigos de salida distintos. |

## Recorrido mostrado en el video

Con una base temporal, se registró `OSC-01` y se prestó a Ana hasta el 5 de noviembre de 2026. La consulta del día 5 mostró `Vigente` y la del 6 mostró `Vencido`. Un segundo préstamo recibió el error `El equipo OSC-01 ya tiene un préstamo activo.` Después de devolverlo, la consulta mostró `No hay préstamos activos.`

## Flujo de agentes

Se verificaron tres perfiles TOML y cuatro encabezados `SKILL.md`. La primera revisión detectó que SQLite ignora la activación de claves foráneas si la conexión ya tiene una transacción abierta. Se corrigió la inicialización para rechazar ese caso y se añadió una comprobación a la suite.

La auditoría de Codex CLI completó el flujo `disenador` → `desarrollador` → `verificador`. Diseño revisó la unicidad de los préstamos activos, las fechas y el historial. Desarrollo contrastó esos criterios con la implementación. Verificación ejecutó 10 pruebas en 2.407 segundos, con resultado `OK` y código de salida 0. La revisión también identificó la diferencia entre los códigos 1 y 2 de la consola, incorporada después al diseño.

El [informe de OpenCode](informe-opencode.md) presenta el montaje equivalente como guía de reproducción.
