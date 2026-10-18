---
name: dental-agenda-frontend
description: Use this skill whenever improving, polishing, or redesigning the frontend of this project (a Django dental-clinic scheduling app) — the Tailwind-based templates in agenda/templates/agenda/ (base.html, calendario.html, staff_calendario.html, reservar.html, login.html). Trigger on requests like "mejorá el diseño", "hacé esto más profesional/elegante", "rediseñá el calendario", "mejorá el frontend", "la página se ve fea/básica", or any styling/UI/UX change to the public calendar, staff panel, booking form, or login page. Also use it proactively when adding a new template to this project, to keep it visually consistent with the rest of the app.
---

# Frontend elegante para agenda-dental

Este proyecto es una agenda de turnos para una clínica dental chica: los pacientes miran
un calendario público (solo libre/ocupado, sin login) y el staff (asistente/dentista)
gestiona las reservas desde un panel con login. El objetivo de diseño es que se sienta
como el sitio de una clínica real y prolija — no como un tutorial de Django por defecto.

## Dónde están los archivos

- `agenda/templates/agenda/base.html` — layout base, navbar, mensajes flash (todo lo
  demás extiende de aquí vía `{% block content %}`)
- `agenda/templates/agenda/calendario.html` — calendario público (solo badges libre/ocupado)
- `agenda/templates/agenda/staff_calendario.html` — panel staff (nombres de pacientes,
  cancelar, link a reservar)
- `agenda/templates/agenda/reservar.html` — formulario de reserva de turno
- `agenda/templates/agenda/login.html` — login del staff

El proyecto usa **Tailwind vía CDN** (cargado en `base.html`), sin build step ni npm.
Mantenelo así — el deploy a PythonAnywhere depende de que no haya paso de compilación.

## Principios de diseño a aplicar

1. **Paleta propia, no "azul de tutorial".** Reemplazar el `bg-blue-700` genérico por
   una paleta más sofisticada y consistente en los 5 templates — por ejemplo un
   azul-petróleo/teal como primario (transmite salud y confianza) y un acento cálido
   para las acciones principales. Definila una vez y reusala en todos los templates,
   no inventes colores nuevos por página.
2. **Tipografía con jerarquía real.** La fuente del sistema (`Segoe UI`) es aceptable
   para texto de cuerpo, pero los títulos se benefician de una fuente con más carácter
   (ej. Inter o similar vía Google Fonts) y de una escala de tamaños clara entre
   `h1`, subtítulos y texto de tabla.
3. **Aire y espaciado.** Las cards y la grilla del calendario no deben sentirse
   apretadas — subí paddings, separá secciones, dejá que el diseño respire.
4. **Estados visuales premium, no saturados.** Los badges de libre/ocupado deben tener
   buen contraste sin gritar — tonos suaves de verde/rojo (o un esquema alternativo)
   con un ícono sutil, en vez de solo texto en mayúsculas.
5. **Micro-interacciones consistentes.** Transiciones suaves en hover, sombras suaves
   con profundidad (no sombras duras tipo Material viejo), radios de borde consistentes
   en todos los componentes (cards, botones, inputs, badges).
6. **Mobile-first para el calendario.** Los pacientes probablemente miran la disponibilidad
   desde el celular. La grilla semanal (5 días × 8 horarios) tiene que seguir siendo
   legible en una pantalla chica — con scroll horizontal elegante, o reflow si hace falta.
7. **Un solo sistema de componentes.** Botones, badges, inputs y cards deben verse igual
   en los 5 templates. Si cambiás el estilo de un botón en `reservar.html`, aplicá el
   mismo estilo en `login.html` y `staff_calendario.html`.

## Qué NO tocar

- No metas un framework de build (webpack, Vite, npm, PostCSS). El proyecto depende de
  no tener build step para el deploy simple a PythonAnywiene.
- No cambies `views.py`, `models.py`, `urls.py` ni los nombres de variables de contexto
  que ya consumen los templates (`calendar`, `week_days`, `offset_prev`, `cell.is_available`,
  etc.), salvo que el usuario pida explícitamente un cambio de comportamiento.
- No rompas los `{% block content %}`, `{% url %}` ni los `name=` de los inputs de
  formularios (los lee `views.py` por ese nombre).

## Flujo de trabajo

1. Leé el/los templates relevantes antes de editar — no asumas su contenido actual.
2. Aplicá los cambios directamente con tu herramienta de edición (no hace falta proponer
   un boceto antes de tocar los archivos — este proyecto prefiere ver el resultado real).
3. Después de editar, activá el venv del proyecto y corré `python manage.py check` para
   detectar errores obvios. Los errores de sintaxis de un template de Django solo
   aparecen al renderizar, así que si es posible, levantá `runserver` y hacé un `curl`
   (o abrí la página) a las vistas que tocaste para confirmar que cargan sin tracebacks.
4. Contale al usuario qué cambiaste y por qué (paleta elegida, tipografía, qué templates
   quedaron consistentes) — no alcanza con decir "mejoré el diseño".
