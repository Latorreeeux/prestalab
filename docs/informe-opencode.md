# Taller de IA agéntica con OpenCode

Este informe presenta el montaje equivalente en OpenCode 2 para el caso PrestaLab. La implementación y la validación de esta entrega se hicieron con Codex y Python. La guía describe cómo reproducir el flujo en OpenCode.

## Problema y solución

El laboratorio necesita saber quién tiene cada equipo y detectar retrasos. PrestaLab ofrece cuatro comandos para registrar, prestar, devolver y listar. Guarda los movimientos en SQLite para que cada ejecución vea los cambios de la anterior.

La restricción central impide abrir dos préstamos del mismo equipo. Al devolverlo, el registro conserva la fecha de devolución y el equipo queda disponible de nuevo. [Diseño y criterios de aceptación](diseno.md).

## Agentes y habilidades

| Agente | Responsabilidad | Habilidad que carga | Salida de la etapa |
| --- | --- | --- | --- |
| `coordinador` | Enlaza las etapas y devuelve defectos a desarrollo. | `coordinar-entrega` | Resumen con resultados observados. |
| `disenador` | Define reglas y criterios comprobables. | `disenar-requisitos` | Diseño y criterios de aceptación. |
| `desarrollador` | Implementa la lógica SQLite y los comandos. | `implementar-python` | Código y comprobación inicial. |
| `verificador` | Ejecuta la suite y reproduce defectos. | `verificar-pruebas` | Casos comprobados y salida de las pruebas. |

El arnés incluye el contexto del proyecto en `AGENTS.md`, los perfiles, los archivos `SKILL.md`, el modelo seleccionado y las herramientas de lectura, edición, consola y delegación. Cada subagente recibe el resultado de la etapa anterior. Cuando una prueba detecta un defecto del código, el coordinador pasa el caso a desarrollo y pide una nueva verificación.

## Montaje propuesto en OpenCode 2

1. Copia las cuatro carpetas de `.agents/skills/` a `.opencode/skills/` dentro del proyecto. Cada carpeta conserva su `SKILL.md`. OpenCode también admite la ruta de compatibilidad `.agents/skills/`; conserva una sola copia por habilidad si preparas un repositorio dedicado a OpenCode.
2. En `.opencode/agents/` crea `coordinador.md` con `mode: primary` y los tres especialistas con `mode: subagent`. Usa los perfiles en `.codex/agents/` como referencia para el contenido. En los cuerpos, indica a cada agente que cargue su habilidad mediante la herramienta `skill` usando el identificador de la tabla.
3. Abre `opencode` en la carpeta del proyecto, selecciona el agente principal `coordinador` y un modelo con herramientas. Pídele que siga el flujo de `AGENTS.md` y delegue en los especialistas. Usa el siguiente perfil para habilitar la delegación a los tres agentes del taller.

```markdown
---
description: Coordina el diseño, la implementación y las pruebas de PrestaLab.
mode: primary
permissions:
  - action: subagent
    resource: "*"
    effect: deny
  - action: subagent
    resource: disenador
    effect: allow
  - action: subagent
    resource: desarrollador
    effect: allow
  - action: subagent
    resource: verificador
    effect: allow
---

Carga la habilidad coordinar-entrega con la herramienta skill.
Sigue el orden de AGENTS.md y pasa el resultado de cada etapa a la siguiente.
Entrega los resultados y la salida observada de las pruebas.
```

Por ejemplo, `verificador.md` usa `description: Comprueba los criterios de aceptación de PrestaLab.` y `mode: subagent` en el encabezado. El cuerpo indica que cargue `verificar-pruebas`, reciba los criterios del coordinador, ejecute `python -B -m unittest discover -s tests -v` e informe el resultado. `disenador.md` y `desarrollador.md` siguen la misma estructura con las responsabilidades de la tabla.

## Evidencia

El [registro de verificación](verificacion.md) contiene la salida de las pruebas de Python y el estado de la ejecución del flujo. El [video](prestalab.mp4) presenta el diseño y muestra la secuencia de comandos del programa.

[Agentes en OpenCode](https://opencode.ai/docs/agents/) · [Habilidades en OpenCode](https://opencode.ai/docs/skills/) · [Subagentes en Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Habilidades de Codex](https://learn.chatgpt.com/docs/build-skills).
