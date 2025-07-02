# from django.shortcuts import render, redirect
# from .forms import TicketForm
# from datetime import datetime
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from .models import Ticket
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from openpyxl.utils import get_column_letter
# from django.utils.timezone import localtime
# from django.views.decorators.csrf import csrf_exempt
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
# from django.core.mail import send_mail
# from django.core.mail import EmailMessage
# from reportlab.lib.styles import getSampleStyleSheet
# import openpyxl
# import base64
# from io import BytesIO

# def home(request):
#     return render(request, 'tickets/home.html', {'year': datetime.now().year})

# def crear_ticket(request):
#     if request.method == 'POST':
#         form = TicketForm(request.POST, request.FILES)
#         if form.is_valid():
#             ticket = form.save()
#             return render(request, 'tickets/ticket_exito.html', {'ticket_id': ticket.id})
#     else:
#         form = TicketForm()
#     return render(request, 'tickets/crear_ticket.html', {'form': form})

# def ticket_pdf(request, ticket_id):
#     ticket = Ticket.objects.get(id=ticket_id)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'


#     doc = SimpleDocTemplate(response, pagesize=letter)
#     elements = []
#     styles = getSampleStyleSheet()

#     # Título centrado
#     elements.append(Paragraph("<b>Solicitud de Servicio Correctivo</b>", styles['Title']))
#     elements.append(Spacer(1, 24))

#     # Datos en formato tabla
#     data = [
#         ["ID", ticket.id],
#         ["Estado", ticket.estado],
#         ["Solicitante", ticket.solicitante],
#         ["Correo electrónico", ticket.email],
#         ["Asignado", ticket.asignado],
#         ["Fecha esperada", ticket.fecha_esperada.strftime('%d/%m/%Y') if ticket.fecha_esperada else ""],
#         ["Prioridad", ticket.prioridad],
#         ["Etiqueta", ticket.etiqueta],
#         ["Título", ticket.titulo],
#         ["Descripción", ticket.descripcion],
#         ["Creado", ticket.creado.strftime('%d/%m/%Y %H:%M')],
#     ]

#     table = Table(data, colWidths=[120, 350])
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 0), (-1, -1), 11),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
#     ]))
#     elements.append(table)
    
#      # Agregar la firma si existe
#     if ticket.firma:
#         elements.append(Spacer(1, 24))
#         elements.append(Paragraph("<b>Firma del solicitante:</b>", styles['Normal']))
#         elements.append(Image(ticket.firma.path, width=200, height=60))

#     doc.build(elements)
#     return response

# def admin_login(request):
#     mensaje = ""
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None and user.is_staff:
#             login(request, user)
#             return redirect('admin_dashboard')
#         else:
#             mensaje = "Credenciales incorrectas o no autorizado."
#     return render(request, 'tickets/admin_login.html', {'mensaje': mensaje})

# @login_required
# def admin_dashboard(request):
#     tickets = Ticket.objects.all().order_by('-creado')
#     return render(request, 'tickets/admin_dashboard.html', {'tickets': tickets})

# @login_required
# def exportar_excel_todos(request):
#     from django.utils.timezone import localtime

#     wb = openpyxl.Workbook()
#     ws = wb.active
#     ws.title = "Tickets"

#     # Encabezados
#     headers = [
#         "ID", "Estado", "Solicitante", "Correo electrónico", "Asignado",
#         "Fecha esperada", "Prioridad", "Etiqueta", "Título", "Descripción", "Creado"
#     ]
#     ws.append(headers)

#     # Datos
#     for ticket in Ticket.objects.all().order_by('-creado'):
#         ws.append([
#             ticket.id,
#             ticket.estado,
#             ticket.solicitante,
#             ticket.email,
#             ticket.asignado,
#             ticket.fecha_esperada.strftime('%d/%m/%Y') if ticket.fecha_esperada else "",
#             ticket.prioridad,
#             ticket.etiqueta,
#             ticket.titulo,
#             ticket.descripcion,
#             localtime(ticket.creado).strftime('%d/%m/%Y %H:%M'),
#         ])

#     # Ajustar ancho de columnas
#     for i, column in enumerate(ws.columns, 1):
#         max_length = max(len(str(cell.value)) if cell.value else 0 for cell in column)
#         ws.column_dimensions[get_column_letter(i)].width = max_length + 2

#     # Respuesta HTTP
#     from django.http import HttpResponse
#     response = HttpResponse(
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )
#     response['Content-Disposition'] = 'attachment; filename="tickets.xlsx"'
#     wb.save(response)
#     return response

# @login_required
# def exportar_excel_mes(request):
#     mes = request.GET.get('mes')  # formato: 'YYYY-MM'
#     if not mes:
#         return HttpResponse("Debes seleccionar un mes.", status=400)

#     try:
#         year, month = map(int, mes.split('-'))
#     except Exception:
#         return HttpResponse("Formato de mes inválido.", status=400)

#     tickets = Ticket.objects.filter(
#         creado__year=year,
#         creado__month=month
#     ).order_by('-creado')

#     wb = openpyxl.Workbook()
#     ws = wb.active
#     ws.title = "Tickets"

#     headers = [
#         "ID", "Estado", "Solicitante", "Correo electrónico", "Asignado",
#         "Fecha esperada", "Prioridad", "Etiqueta", "Título", "Descripción", "Creado"
#     ]
#     ws.append(headers)

#     for ticket in tickets:
#         ws.append([
#             ticket.id,
#             ticket.estado,
#             ticket.solicitante,
#             ticket.email,
#             ticket.asignado,
#             ticket.fecha_esperada.strftime('%d/%m/%Y') if ticket.fecha_esperada else "",
#             ticket.prioridad,
#             ticket.etiqueta,
#             ticket.titulo,
#             ticket.descripcion,
#             localtime(ticket.creado).strftime('%d/%m/%Y %H:%M'),
#         ])

#     # Ajustar ancho de columnas
#     for i, column in enumerate(ws.columns, 1):
#         max_length = max(len(str(cell.value)) if cell.value else 0 for cell in column)
#         ws.column_dimensions[get_column_letter(i)].width = max_length + 2

#     response = HttpResponse(
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )
#     response['Content-Disposition'] = f'attachment; filename="tickets_{year}_{month:02d}.xlsx"'
#     wb.save(response)
#     return response

# @login_required
# @csrf_exempt
# def ticket_detalle(request, ticket_id):
#     ticket = Ticket.objects.get(id=ticket_id)
#     if request.method == "POST":
#         ticket.respuesta = request.POST.get("respuesta")
#         firma_data = request.POST.get("firma_data")
#         if firma_data:
#             format, imgstr = firma_data.split(';base64,')
#             ext = format.split('/')[-1]
#             filename = f"firma_ticket_{ticket.id}.{ext}"
#             from django.core.files.base import ContentFile
#             ticket.firma.save(filename, ContentFile(base64.b64decode(imgstr)), save=False)
#         ticket.estado = "Cerrado"
#         ticket.save()

#         # --- Generar PDF en memoria ---
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter)
#         elements = []
#         styles = getSampleStyleSheet()
#         elements.append(Paragraph("<b>Solicitud de Servicio Correctivo</b>", styles['Title']))
#         elements.append(Spacer(1, 24))
#         data = [
#             ["ID", ticket.id],
#             ["Estado", ticket.estado],
#             ["Solicitante", ticket.solicitante],
#             ["Correo electrónico", ticket.email],
#             ["Asignado", ticket.asignado],
#             ["Fecha esperada", ticket.fecha_esperada.strftime('%d/%m/%Y') if ticket.fecha_esperada else ""],
#             ["Prioridad", ticket.prioridad],
#             ["Etiqueta", ticket.etiqueta],
#             ["Título", ticket.titulo],
#             ["Descripción", ticket.descripcion],
#             ["Respuesta", ticket.respuesta],
#             ["Creado", ticket.creado.strftime('%d/%m/%Y %H:%M')],
#         ]
#         table = Table(data, colWidths=[120, 350])
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#             ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#             ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#             ('FONTSIZE', (0, 0), (-1, -1), 11),
#             ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
#         ]))
#         elements.append(table)
#         if ticket.firma:
#             elements.append(Spacer(1, 24))
#             elements.append(Paragraph("<b>Firma del solicitante:</b>", styles['Normal']))
#             elements.append(Image(ticket.firma.path, width=200, height=60))
#         doc.build(elements)
#         pdf = buffer.getvalue()
#         buffer.close()

#         # --- Enviar correo con PDF adjunto ---
#         email = EmailMessage(
#             subject='Tu ticket ha sido respondido',
#             body=f'Hola {ticket.solicitante},\n\nTu ticket "{ticket.titulo}" ha sido respondido:\n\n{ticket.respuesta}',
#             from_email='soporte@tusitio.com',
#             to=[ticket.email],
#         )
#         email.attach(f'ticket_{ticket.id}.pdf', pdf, 'application/pdf')
#         email.send(fail_silently=False)

#         return redirect('admin_dashboard')
#     return render(request, "tickets/ticket_detalle.html", {"ticket": ticket})



