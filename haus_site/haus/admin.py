from django.contrib import admin
from models import HausUser, Device, Atom, Data, CurrentData, DailySummaryData

# Register your models here.
admin.site.register(HausUser)
admin.site.register(Device)
admin.site.register(Atom)
admin.site.register(Data)
admin.site.register(CurrentData)
admin.site.register(DailySummaryData)
