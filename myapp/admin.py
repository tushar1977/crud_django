from django.contrib import admin
from .models import Agent, Campaign , CampaignResult
# Register your models here.
#
admin.site.register(Agent)
admin.site.register(Campaign)
admin.site.register(CampaignResult)
