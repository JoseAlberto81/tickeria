from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crear/', views.crear_ticket, name='crear_ticket'),
    path('ticket/<int:ticket_id>/pdf/', views.ticket_pdf, name='ticket_pdf'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('ticket/<int:ticket_id>/pdf/', views.ticket_pdf, name='ticket_pdf'),
    path('exportar-excel-mes/', views.exportar_excel_mes, name='exportar_excel_mes'),
    path('exportar-excel-todos/', views.exportar_excel_todos, name='exportar_excel_todos'),
    path('ticket/<int:ticket_id>/detalle/', views.ticket_detalle, name='ticket_detalle'),
]