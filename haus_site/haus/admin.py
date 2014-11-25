from django.contrib import admin
from models import Device, Atom, Data, CurrentData, DailySummaryData

# Register your models here.
admin.site.register(Device)
admin.site.register(Atom)
admin.site.register(Data)
admin.site.register(CurrentData)
admin.site.register(DailySummaryData)
