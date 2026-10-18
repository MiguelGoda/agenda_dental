from datetime import date, time, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Patient


# Slots disponibles de lunes a viernes, 15:00 a 18:30 cada 30 min
SLOTS = [
    time(15, 0), time(15, 30),
    time(16, 0), time(16, 30),
    time(17, 0), time(17, 30),
    time(18, 0), time(18, 30),
]


def get_week_days(base_date):
    """Devuelve los 5 días hábiles de la semana que contiene base_date."""
    monday = base_date - timedelta(days=base_date.weekday())
    return [monday + timedelta(days=i) for i in range(5)]


def week_anchor():
    """Punto de partida para 'esta semana' (offset=0).

    Si hoy es sábado o domingo, la semana lunes-viernes que contiene hoy ya
    terminó o está por arrancar fuera de horario de atención, así que el
    ancla salta al próximo lunes en vez de mostrar una semana pasada.
    """
    today = date.today()
    if today.weekday() >= 5:  # 5 = sábado, 6 = domingo
        today += timedelta(days=7 - today.weekday())
    return today


def build_calendar(week_days):
    """Construye la grilla: para cada slot, qué días están ocupados."""
    # Traer todos los turnos de la semana de una sola query
    appointments = Appointment.objects.filter(
        date__in=week_days
    ).select_related("patient")

    # Indexar por (fecha, hora)
    occupied = {}
    for appt in appointments:
        occupied[(appt.date, appt.start_time)] = appt

    # Construir grilla
    calendar = []
    for slot in SLOTS:
        row = {"slot": slot, "days": []}
        for day in week_days:
            appt = occupied.get((day, slot))
            row["days"].append({
                "date": day,
                "appointment": appt,
                "is_available": appt is None,
            })
        calendar.append(row)

    return calendar


def calendario_publico(request):
    """Vista pública: solo muestra libre/ocupado, sin nombres."""
    today = date.today()

    # Navegación por semanas
    offset = int(request.GET.get("semana", 0))
    base_date = week_anchor() + timedelta(weeks=offset)
    week_days = get_week_days(base_date)

    calendar = build_calendar(week_days)

    return render(request, "agenda/calendario.html", {
        "calendar": calendar,
        "week_days": week_days,
        "offset": offset,
        "offset_prev": offset - 1,
        "offset_next": offset + 1,
        "today": today,
    })


@login_required
def calendario_staff(request):
    """Vista staff: muestra nombres de pacientes y botones de acción."""
    today = date.today()

    offset = int(request.GET.get("semana", 0))
    base_date = week_anchor() + timedelta(weeks=offset)
    week_days = get_week_days(base_date)

    calendar = build_calendar(week_days)

    return render(request, "agenda/staff_calendario.html", {
        "calendar": calendar,
        "week_days": week_days,
        "offset": offset,
        "offset_prev": offset - 1,
        "offset_next": offset + 1,
        "today": today,
    })


@login_required
def reservar(request):
    """Formulario para crear una reserva."""
    appt_date = request.GET.get("fecha")
    appt_time = request.GET.get("hora")

    # Verificar que el slot no esté ocupado
    if Appointment.objects.filter(date=appt_date, start_time=appt_time).exists():
        messages.error(request, "Ese turno ya está ocupado.")
        return redirect("staff_calendario")

    if request.method == "POST":
        # Buscar o crear paciente
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email", "")
        notes = request.POST.get("notes", "")
        patient_id = request.POST.get("patient_id")

        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
        else:
            patient = Patient.objects.create(name=name, phone=phone, email=email)

        Appointment.objects.create(
            patient=patient,
            date=request.POST.get("date"),
            start_time=request.POST.get("start_time"),
            notes=notes,
            created_by=request.user,
        )
        messages.success(request, f"Turno reservado para {patient.name}.")
        return redirect("staff_calendario")

    # Buscar pacientes existentes para autocompletar
    patients = Patient.objects.all()

    return render(request, "agenda/reservar.html", {
        "appt_date": appt_date,
        "appt_time": appt_time,
        "patients": patients,
    })


@login_required
def detalle_turno(request, appt_id):
    """Muestra los datos del paciente y el turno, con opción de cancelar."""
    appt = get_object_or_404(Appointment, id=appt_id)
    return render(request, "agenda/detalle_turno.html", {"appt": appt})


@login_required
def cancelar(request, appt_id):
    """Cancela (elimina) un turno."""
    appt = get_object_or_404(Appointment, id=appt_id)
    patient_name = appt.patient.name
    appt.delete()
    messages.success(request, f"Turno de {patient_name} cancelado.")
    return redirect("staff_calendario")
