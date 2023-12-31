from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from vehicles.models import Car, UserProfile

class CommonFields(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True

class TypeMaintenance(CommonFields):
    class Meta:
        verbose_name = 'Вид технического обслуживания'
        verbose_name_plural = 'Виды технических обслуживаний'

class Failure(CommonFields):
    class Meta:
        verbose_name = 'Узел отказа'
        verbose_name_plural = 'Узлы отказа'

class RecoveryMethod(CommonFields):
    class Meta:
        verbose_name = 'Способ восстановления'
        verbose_name_plural = 'Способы восстановления'

class ServiceCompany(CommonFields):
    class Meta:
        verbose_name = 'Сервисная компания'
        verbose_name_plural = 'Сервисные компании'

class CommonMaintenanceFields(models.Model):
    date = models.DateField(default=datetime.now, verbose_name='Дата')
    operating_time = models.PositiveIntegerField(default=0, verbose_name='Наработка, м/час')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')

    class Meta:
        abstract = True

class Service(models.Model):
    order_number = models.CharField(max_length=20, verbose_name='№ заказ-наряда')
    order_date = models.DateField(default=datetime.now, verbose_name='Дата заказ-наряда')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Организация, проводившая ТО', null=True, blank=True)

    class Meta:
        abstract = True

class Maintenance(CommonMaintenanceFields, Service):
    type = models.ForeignKey(TypeMaintenance, on_delete=models.CASCADE, verbose_name='Вид ТО')

    def __str__(self):
        return f'{self.date} {self.car}'

    class Meta:
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Технические обслуживания'

class Complaint(CommonMaintenanceFields):
    date_failure = models.DateField(default=datetime.now, verbose_name='Дата отказа')
    node_failure = models.ForeignKey(Failure, on_delete=models.CASCADE, verbose_name='Узел отказа')
    description_failure = models.TextField(blank=True, null=True, verbose_name='Описание отказа')
    method_recovery = models.ForeignKey(RecoveryMethod, on_delete=models.CASCADE, verbose_name='Способ восстановления')
    repair_parts = models.TextField(blank=True, null=True, verbose_name='Используемые запасные части')
    date_recovery = models.DateField(default=datetime.now, verbose_name='Дата восстановления')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания', null=True, blank=True)

    def __str__(self):
        return f'{self.date_failure} {self.car}'

    def downtime(self):
        delta_time = self.date_recovery - self.date_failure
        return delta_time.days

    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'
