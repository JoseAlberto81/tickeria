from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from tickets.models import Ticket
import base64
from io import BytesIO

@login_required
@csrf_exempt
def ticket_detalle(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        ticket.respuesta = request.POST.get("respuesta")
        firma_data = request.POST.get("firma_data")
        if firma_data:
            format, imgstr = firma_data.split(';base64,')
            ext = format.split('/')[-1]
            filename = f"firma_ticket_{ticket.id}.{ext}"
            from django.core.files.base import ContentFile
            ticket.firma.save(filename, ContentFile(base64.b64decode(imgstr)), save=False)
        ticket.estado = "Cerrado"
        ticket.save()

        # --- Generar PDF en memoria ---
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph("<b>Solicitud de Servicio Correctivo</b>", styles['Title']))
        elements.append(Spacer(1, 24))
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
            ["Respuesta", ticket.respuesta],
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
        if ticket.firma:
            elements.append(Spacer(1, 24))
            elements.append(Paragraph("<b>Firma del solicitante:</b>", styles['Normal']))
            elements.append(Image(ticket.firma.path, width=200, height=60))
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        # --- Enviar correo con PDF adjunto ---
        email = EmailMessage(
            subject='Tu ticket ha sido respondido',
            body=f'Hola {ticket.solicitante},\n\nTu ticket "{ticket.titulo}" ha sido respondido:\n\n{ticket.respuesta}',
            from_email='soporte@tusitio.com',
            to=[ticket.email],
        )
        email.attach(f'ticket_{ticket.id}.pdf', pdf, 'application/pdf')
        email.send(fail_silently=False)

        return redirect('admin_dashboard')
    return render(request, "tickets/ticket_detalle.html", {"ticket": ticket})