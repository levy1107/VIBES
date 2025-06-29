# Protocolo de Comunicación Interna

Este documento define cómo se comunicarán las diferentes partes del sistema Gemini.

## Humano -> Gemini (Principal)

- **Canal:** Interfaz web (casilla de texto).
- **Formato:** Lenguaje natural.
- **Acción:** Las instrucciones se guardan en `new_instructions.md`. Gemini (Principal) es notificado para leer y procesar.

## Gemini (Principal) -> Gemini (Trabajadores/Ramas)

- **Canal:** Archivos de tareas en un directorio `tasks/`.
- **Formato:** Archivos Markdown (`.md`) con una estructura específica.
- **Estructura de Tarea (`tasks/task-ID.md`):**
    ```markdown
    **ID de Tarea:** 20250629-001
    **Rama Asignada:** backend
    **Descripción:** Crear la ruta de la API para leer el backlog.
    **Criterios de Aceptación:**
    - [ ] La ruta `/api/backlog` debe existir.
    - [ ] Debe devolver el contenido del archivo `backlog.md` en formato JSON.
    - [ ] Debe manejar el caso en que el archivo no exista.
    ```
- **Acción:**
    1. Gemini (Principal) crea un nuevo archivo de tarea.
    2. Cambia a la rama correspondiente (ej. `git checkout backend`).
    3. Implementa la tarea.
    4. Actualiza el archivo de la tarea marcando los criterios como completados.
    5. Hace commit de los cambios en la rama.
    6. Vuelve a la rama `main`.

## Gemini (Trabajadores/Ramas) -> Gemini (Principal)

- **Canal:** Commits de Git y actualización de los archivos de tarea.
- **Formato:** Mensajes de commit estandarizados.
- **Ejemplo de Mensaje de Commit:** `feat(backend): Implementa API de backlog - Tarea 20250629-001`
- **Acción:** Gemini (Principal) puede revisar el historial de commits de las ramas para ver el progreso y verificar las tareas completadas.
