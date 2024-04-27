from django.db import models

# Create your models here.
class AirportList(models.Model):
    AIRPORTCODE = models.CharField(max_length=3, unique=True)
    AIRPORTNAME = models.CharField(max_length=255)
    CITYCODE = models.CharField(max_length=3)
    CITYNAME = models.CharField(max_length=255)
    COUNTRYNAME = models.CharField(max_length=255)
    CURRENCYCODE = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.airport_code} - {self.airport_name}"
    

class Flightclientdetails(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    user_information = models.JSONField()
    datetime = models.DateTimeField(blank=True, null=True)
    published_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_flag = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=255)
    payed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_id = models.CharField(max_length=255, blank=True, null=True)
    booking_ref_no = models.CharField(max_length=255, blank=True, null=True)
    invoice_number = models.CharField(max_length=255, blank=True, null=True)
    confirmation_no = models.CharField(max_length=255, blank=True, null=True)
    booking_information = models.JSONField(blank=True, null=True)
    payment_information = models.JSONField(blank=True, null=True)
    is_price_changed = models.IntegerField(blank=True, null=True)
    is_cancellation_policy_changed = models.IntegerField(blank=True, null=True)
    is_price_changed_true = models.JSONField(blank=True, null=True)
    is_cancellation_policy_changed_true = models.JSONField(blank=True, null=True)
    changerequestid = models.CharField(db_column='ChangeRequestId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cancel_status = models.CharField(db_column='Cancel_status', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cancellation_details = models.JSONField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    contact_details = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flightclientdetails'
