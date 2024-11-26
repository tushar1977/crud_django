from django.db import models
import uuid

from django.utils.timezone import now

class Agent(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
    ]

    id=models.AutoField(primary_key=True)
    agent_name = models.CharField(max_length=255)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    voice_id = models.CharField(max_length=100, unique=True)
    updated = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            'id': str(self.id),
            'agent_name': self.agent_name,
            'language': self.language,
            'voice_id': self.voice_id,
            'updated': self.updated.isoformat()
        }

class Campaign(models.Model):
    CAMPAIGN_TYPE_CHOICES = [
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ]

    CAMPAIGN_STATUS_CHOICES = [
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]

    id=models.AutoField(primary_key=True)
    campaign_name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=50, choices=CAMPAIGN_TYPE_CHOICES, default='Outbound')
    phone_number = models.CharField(max_length=15)
    campaign_status = models.CharField(max_length=50, choices=CAMPAIGN_STATUS_CHOICES, default='running')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='campaigns')
    created_at = models.DateTimeField( default=now)

    def to_dict(self):
        return {
            'id': str(self.id),
            'campaign_name': self.campaign_name,
            'campaign_type': self.campaign_type,
            'phone_number': self.phone_number,
            'campaign_status': self.campaign_status,
            'agent_id': str(self.agent.id),
            'created_at': self.created_at.isoformat()
        }

class CampaignResult(models.Model):
    RESULT_TYPE_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('no_answer', 'No Answer'),
    ]
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=RESULT_TYPE_CHOICES)
    phone = models.CharField(max_length=15)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    outcome = models.CharField(max_length=255)
    call_duration = models.FloatField()
    recording = models.URLField(max_length=500, blank=True, null=True)
    summary = models.TextField(blank=True)
    transcription = models.TextField(blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='results')
    created_at = models.DateTimeField(default=now)

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'type': self.type,
            'phone': self.phone,
            'cost': float(self.cost),
            'outcome': self.outcome,
            'call_duration': self.call_duration,
            'recording': self.recording,
            'summary': self.summary,
            'transcription': self.transcription,
            'campaign_id': str(self.campaign.id),
            'created_at': self.created_at.isoformat()
        }
