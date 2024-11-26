"""
URL configuration for crud_apis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import AgentView, CampaignView , CampaignResultView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('agents/', AgentView.as_view(), name='agent_list'),
    path('agents/<int:agent_id>/', AgentView.as_view(), name='agent_detail'),
    path('campaigns/', CampaignView.as_view(), name='campaign_list'),
    path('campaigns/<int:campaign_id>/', CampaignView.as_view(), name='campaign_detail'),

    path('campaign-results/', CampaignResultView.as_view(), name='campaign_result_list'),
    path('campaign-results/<int:result_id>/', CampaignResultView.as_view(), name='campaign_result_detail'),
]
