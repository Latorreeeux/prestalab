# PrestaLab · Taller de IA agéntica

PrestaLab registra préstamos de equipos de laboratorio. El caso reúne diseño, código y pruebas en un flujo coordinado con tres agentes especializados y cuatro habilidades reutilizables.

- [Informe del taller con OpenCode](docs/informe-opencode.md)
- [Diseño y criterios de aceptación](docs/diseno.md)
- [Resultados de la verificación](docs/verificacion.md)
- [Video explicativo](docs/prestalab.mp4)

## Probar el programa

Desde esta carpeta, con **Python 3.11 o posterior**. SQLite y las pruebas vienen en la biblioteca estándar.

```powershell
python prestalab.py registrar OSC-01 "Osciloscopio"
python prestalab.py prestar OSC-01 Ana --desde 2026-11-01 --hasta 2026-11-05
python prestalab.py listar --fecha 2026-11-05
python prestalab.py listar --fecha 2026-11-06
python prestalab.py devolver OSC-01 --fecha 2026-11-06
python prestalab.py listar --fecha 2026-11-06
python -B -m unittest discover -s tests -v
```

Las consultas muestran **Vigente** el 5 de noviembre, **Vencido** el 6 y una lista vacía después de la devolución. El programa guarda los datos en `prestalab.sqlite3`. Para probar desde cero en otra base, añade `--db otra.sqlite3` antes de cada subcomando.

## Ejecutar el flujo agentico con Codex

Abre esta carpeta como proyecto de confianza en Codex. El contexto está en `AGENTS.md`, los tres perfiles en `.codex/agents/` y las cuatro habilidades en `.agents/skills/`. Si usas la CLI, invoca `codex` desde esta carpeta.

Pega esta solicitud en una sesión nueva:

```text
Usa $coordinar-entrega para auditar PrestaLab. Delega en disenador, desarrollador
y verificador de forma secuencial. Pasa el resultado anterior a cada agente y
pídele que lea su skill. Ejecuta la suite en bases temporales, conserva el código
actual y reporta los criterios, los archivos revisados y los resultados reales.
```

Para encargar un cambio, reemplaza la solicitud de auditoría por el requisito. Por ejemplo, «agrega a `listar` la opción `--solo-vencidos` y comprueba que en la fecha límite el préstamo todavía no aparece». El flujo de `AGENTS.md` asigna la edición de la aplicación y las pruebas a sus respectivos perfiles.
