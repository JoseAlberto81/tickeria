from django.shortcuts import render
from tickets.forms import TicketForm
from tickets.models import Ticket
from datetime import datetime
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def home(request):
    return render(request, 'tickets/home.html', {'year': datetime.now().year})

def crear_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save()
            return render(request, 'tickets/ticket_exito.html', {'ticket_id': ticket.id})
    else:
        form = TicketForm()
    return render(request, 'tickets/crear_ticket.html', {'form': form})

def ticket_pdf(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'


    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título centrado
    elements.append(Paragraph("<b>Solicitud de Servicio Correctivo</b>", styles['Title']))
    elements.append(Spacer(1, 24))

    # Datos en formato tabla
    data = [
        ["ID", ticket.id],
        ["Estado", ticket.estado],
        ["Solicitante", ticket.solicitante],
        ["Correo electrónico", ticket.email],
        ["Asignado", ticket.asignado],
        ["Fecha esperada", ticket.fecha_esperada.strftime('%d/%m/%Y') if ticket.fecha_esperada else ""],
        ["Prioridad", ticket.prioridad],
        ["Etiqueta", ticket.etiqueta],
        ["Título", ticket.titulo],
        ["Descripción", ticket.descripcion],
        ["Creado", ticket.creado.strftime('%d/%m/%Y %H:%M')],
    ]

    table = Table(data, colWidths=[120, 350])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)
    
     # Agregar la firma si existe
    if ticket.firma:
        elements.append(Spacer(1, 24))
        elements.append(Paragraph("<b>Firma del solicitante:</b>", styles['Normal']))
        elements.append(Image(ticket.firma.path, width=200, height=60))

    doc.build(elements)
    return response