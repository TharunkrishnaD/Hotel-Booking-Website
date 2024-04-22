from django.db import models

# Create your models here.
class NewCityListHotelCSV(models.Model):
    CITYID = models.IntegerField()
    DESTINATION = models.CharField(max_length=255)
    STATEPROVINCE = models.CharField(max_length=255)
    STATEPROVINCECODE = models.CharField(max_length=255)
    COUNTRY = models.CharField(max_length=255)
    COUNTRYCODE = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.DESTINATION}, {self.COUNTRY}, {self.CITYID} , {self.COUNTRYCODE}"