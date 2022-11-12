import json
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from channels.layers import get_channel_layer
from patients.models import Appointment, Patient, Wallet
from kavenegar import *
from core.tasks import send_SMS_task


channel_layer = get_channel_layer()


@receiver(post_save, sender=Appointment)
def appointment_action(sender, instance, created, **kwargs):
    if created or instance.status_reservation == 'free':
        data = model_to_dict(instance)
        data.update({'action': 'add'})
        async_to_sync(channel_layer.group_send)(
            'doctor_id', {'type': 'send_action_appointment', 'text': json.dumps(data, indent=4, sort_keys=True, default=str)})

    elif instance.status_reservation == 'reserve':
        data = model_to_dict(instance)
        data.update({'action': 'remove'})
        async_to_sync(channel_layer.group_send)(
            'doctor_id', {'type': 'send_action_appointment', 'text': json.dumps(data, indent=4, sort_keys=True, default=str)})


@receiver(post_save, sender=Patient)
def create_first_obj_appointment(sender, instance, created, **kwargs):
    """
    signal for create wallet for patient after create account
    """
    if created:
        Wallet.objects.create(user=instance)
        return True


@receiver(post_save, sender=Appointment)
def send_sms_for_reserve_appointment_by_patient(sender, instance, created, **kwargs):
    """
    signal for sending SMS to patient after reresve appointment
    """
    if instance.status_reservation == 'reserve' and instance.payment == True:
        phone_number_of_patient = '0'+str(instance.user.phone_number)[2:]
        patient_name = instance.user.full_name
        doctor_name = instance.doctor.full_name
        date_of_appointment = instance.date_of_visit
        time_of_appointment = instance.start_visit_time

        text = f'{patient_name} aziz nobat show az doctor {doctor_name} dar tarikh {str(date_of_appointment)} va saat {time_of_appointment} sabt shod '
        # send sms by kavenegar
        send_SMS_task.delay(phone_number_of_patient, text)
        return True
