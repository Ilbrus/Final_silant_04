from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import generics
from vehicles.models import Car
from service.models import Maintenance, Complaint
from service.forms import MaintenanceForm, ComplaintForm
from service.serializers import MaintenanceSerializer, ComplaintSerializer

class MaintenanceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'service.view_maintenance'
    model = Maintenance
    template_name = 'service/maintenance_list.html'

    def get_queryset(self):
        queryset = Maintenance.objects.all()
        if not self.request.user.is_staff:
            user = self.request.user
            try:
                profile = user.userprofile
                if profile.is_service:
                    queryset = Maintenance.objects.filter(service_company=profile.service_company)
                else:
                    queryset = Maintenance.objects.filter(car__client=user)
            except:
                pass
        return queryset

class MaintenanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'service.add_maintenance'
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'service/maintenance_create.html'
    success_url = reverse_lazy('maintenance_list')

class MaintenanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'service.change_maintenance'
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'service/maintenance_update.html'
    success_url = reverse_lazy('maintenance_list')

class MaintenanceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'service.delete_maintenance'
    model = Maintenance
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('maintenance_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'maintenance'
        return context

class ComplaintListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'service.view_complaint'
    model = Complaint
    template_name = 'service/complaint_list.html'

    def get_queryset(self):
        queryset = Complaint.objects.all()
        if not self.request.user.is_staff:
            user = self.request.user
            try:
                profile = user.userprofile
                if profile.is_service:
                    queryset = Complaint.objects.filter(service_company=profile.service_company)
                else:
                    queryset = Complaint.objects.filter(car__client=user)
            except:
                pass
        return queryset

class ComplaintCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'service.add_complaint'
    model = Complaint
    form_class = ComplaintForm
    template_name = 'service/complaint_create.html'
    success_url = reverse_lazy('complaint_list')

class ComplaintUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'service.change_complaint'
    model = Complaint
    form_class = ComplaintForm
    template_name = 'service/complaint_update.html'
    success_url = reverse_lazy('complaint_list')

class ComplaintDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'service.delete_complaint'
    model = Complaint
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('complaint_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'complaint'
        return context

class MaintenanceCarListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'service.view_maintenance'
    model = Maintenance
    template_name = 'service/maintenance_car.html'

    def get_queryset(self):
        car = get_object_or_404(Car, pk=self.kwargs["pk"])
        return Maintenance.objects.filter(car=car)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["car"] = get_object_or_404(Car, pk=self.kwargs["pk"])
        return context

class ComplaintCarListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'service.view_complaint'
    model = Complaint
    template_name = 'service/complaint_car.html'

    def get_queryset(self):
        car = get_object_or_404(Car, pk=self.kwargs["pk"])
        return Complaint.objects.filter(car=car)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["car"] = get_object_or_404(Car, pk=self.kwargs["pk"])
        return context

class MaintenanceDescriptionView(TemplateView):
    template_name = 'service/modal_description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maintenance = get_object_or_404(Maintenance, pk=self.kwargs["pk"])
        attribute = context['attribute']
        if attribute == 'type':
            context['attribute'] = maintenance.type
            context['description'] = maintenance.type.description
        elif attribute == 'service_company':
            context['attribute'] = maintenance.service_company
            context['description'] = maintenance.service_company.description
        return context

class ComplaintDescriptionView(TemplateView):
    template_name = 'service/modal_description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        complaint = get_object_or_404(Complaint, pk=self.kwargs["pk"])
        attribute = self.kwargs.get("attribute")  # Получите значение attribute из URL
        context['attribute'] = attribute  # Добавьте attribute в контекст
        if attribute == 'node_failure':
            context['description'] = complaint.node_failure.description
        elif attribute == 'method_recovery':
            context['description'] = complaint.method_recovery.description
        elif attribute == 'service_company':
            context['description'] = complaint.service_company.description
        return context

# API
class MaintenanceListAPI(generics.ListAPIView):
    serializer_class = MaintenanceSerializer
    queryset = Maintenance.objects.all()

class MaintenanceUserListAPI(generics.ListAPIView):
    serializer_class = MaintenanceSerializer

    def get_queryset(self):
        user = self.kwargs['user']
        if isinstance(user, int):
            return Maintenance.objects.filter(car__client=user)
        elif isinstance(user, str):
            return Maintenance.objects.filter(car__client__username=user)

class MaintenanceDetailAPI(generics.RetrieveAPIView):
    serializer_class = MaintenanceSerializer

    def get_object(self):
        return get_object_or_404(Maintenance, pk=self.kwargs['pk'])

class ComplaintListAPI(generics.ListAPIView):
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()

class ComplaintUserListAPI(generics.ListAPIView):
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        user = self.kwargs['user']
        if isinstance(user, int):
            return Complaint.objects.filter(car__client=user)
        elif isinstance(user, str):
            return Complaint.objects.filter(car__client__username=user)

class ComplaintDetailAPI(generics.RetrieveAPIView):
    serializer_class = ComplaintSerializer

    def get_object(self):
        return get_object_or_404(Complaint, pk=self.kwargs['pk'])
