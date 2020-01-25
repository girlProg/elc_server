from django.contrib import admin
from django.db import models as django_models
from salaryapp import models
# Register your models here
import inspect


for name,obj in inspect.getmembers(models):
    if inspect.isclass(obj) and issubclass(obj,django_models.Model) and obj._meta.abstract is not True and name not in ['User']:
        class Admin(admin.ModelAdmin):
            def get_list_display(self,request):
                return [t.name for t in self.model._meta.fields if t.editable]
            class Meta:
                model = obj
        admin.site.register(obj,Admin)


