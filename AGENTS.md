# Contexto de PrestaLab

PrestaLab registra los préstamos de equipos de un laboratorio. Lee `docs/diseno.md` para conocer las reglas del programa y ejecuta `python -m unittest discover -s tests -v` desde esta carpeta para verificarlo.

## Flujo de trabajo

Cuando se pida el flujo agentico completo, actúa como coordinador y delega explícitamente en estos tres agentes en orden. Espera y entrega el resultado de cada etapa a la siguiente.

1. `disenador` lee el requisito y el diseño y entrega reglas, criterios de aceptación y archivos afectados.
2. `desarrollador` recibe ese resultado y trabaja sobre el programa. Ajusta el diseño si cambió el contrato. Devuelve archivos modificados, decisiones y una comprobación inicial.
3. `verificador` recibe el diseño y los cambios, revisa las pruebas, agrega cobertura pertinente y ejecuta la suite. Devuelve comandos, resultados y defectos reproducibles. Si encuentra un defecto del programa, vuelve con el desarrollador y después pide una nueva verificación.

Usa `coordinar-entrega` para integrar las tres etapas. Si la solicitud es de auditoría, indica a los tres agentes que trabajen en lectura. Si se pide una implementación, asigna la edición del programa al desarrollador y la de las pruebas al verificador. Trabaja dentro de esta carpeta y usa bases temporales para las pruebas.
