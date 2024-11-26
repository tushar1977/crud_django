from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.i18n import JsonResponse
from .models import Agent, Campaign, CampaignResult
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

@method_decorator(csrf_exempt, name='dispatch')
class AgentView(View):
    def get(self, request, agent_id=None):
        if agent_id:
            try:
                agent = Agent.objects.get(id=agent_id)
                print(agent)
                return JsonResponse(agent.to_dict(), safe=False)
            except Agent.DoesNotExist:
                return JsonResponse({'error': 'Agent not found'}, status=404)
        
        agent_data = list(Agent.objects.all().values())
        return JsonResponse(agent_data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)

            if Agent.objects.filter(agent_name=data['agent_name']).exists():
                return JsonResponse({'error': 'A Agent with this name already exists'}, status=400)
            agent = Agent.objects.create(
                agent_name=data['agent_name'],
                language=data['language'],
                voice_id=data['voice_id']
            )
            return JsonResponse(agent.to_dict(), status=201)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    def put(self, request, agent_id):
        try:
            agent = Agent.objects.get(id=agent_id)
            data = json.loads(request.body)
            
            agent.agent_name = data.get('agent_name', agent.agent_name)
            agent.language = data.get('language', agent.language)
            agent.voice_id = data.get('voice_id', agent.voice_id)
            
            agent.save()
            return JsonResponse(agent.to_dict())
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Agent not found'}, status=404)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, agent_id):
        try:
            agent = Agent.objects.get(id=agent_id)
            agent.delete()
            return JsonResponse({'message': 'Agent deleted successfully'})
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Agent not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class CampaignView(View):
    def get(self, request, campaign_id=None):
        if campaign_id:
            try:
                campaign = Campaign.objects.get(id=campaign_id)
                return JsonResponse(campaign.to_dict())
            except Campaign.DoesNotExist:
                return JsonResponse({'error': 'Campaign not found'}, status=404)
        
        campaigns = Campaign.objects.all()
        return JsonResponse({
            'campaigns': [campaign.to_dict() for campaign in campaigns]
        })

    def post(self, request):
        try:
            data = json.loads(request.body)
            agent = Agent.objects.get(id=data['agent_id'])
            
            if Campaign.objects.filter(campaign_name=data['campaign_name']).exists():
                return JsonResponse({'error': 'A campaign with this name already exists'}, status=400)

            campaign = Campaign.objects.create(
                campaign_name=data['campaign_name'],
                campaign_type=data['campaign_type'],
                phone_number=data['phone_number'],
                campaign_status=data.get('campaign_status', 'running'),
                agent=agent
            )


            return JsonResponse(campaign.to_dict(), status=201)
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Invalid agent ID'}, status=400)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            data = json.loads(request.body)
            
            # Update agent if provided
            if 'agent_id' in data:
                campaign.agent = Agent.objects.get(id=data['agent_id'])
            
            campaign.campaign_name = data.get('campaign_name', campaign.campaign_name)
            campaign.campaign_type = data.get('campaign_type', campaign.campaign_type)
            campaign.phone_number = data.get('phone_number', campaign.phone_number)
            campaign.campaign_status = data.get('campaign_status', campaign.campaign_status)
            
            campaign.save()
            return JsonResponse(campaign.to_dict())
        except Campaign.DoesNotExist:
            return JsonResponse({'error': 'Campaign not found'}, status=404)
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Invalid agent ID'}, status=400)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            campaign.delete()
            return JsonResponse({'message': 'Campaign deleted successfully'})
        except Campaign.DoesNotExist:
            return JsonResponse({'error': 'Campaign not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class CampaignResultView(View):
    def get(self, request, result_id=None):
        if result_id:
            try:
                result = CampaignResult.objects.get(id=result_id)
                return JsonResponse(result.to_dict())
            except CampaignResult.DoesNotExist:
                return JsonResponse({'error': 'Campaign Result not found'}, status=404)
        
        results = CampaignResult.objects.all()
        return JsonResponse({
            'campaign_results': [result.to_dict() for result in results]
        })

    def post(self, request):
        try:
            data = json.loads(request.body)
            campaign = Campaign.objects.get(id=data['campaign_id'])
            
            result = CampaignResult.objects.create(
                name=data['name'],
                type=data['type'],
                phone=data['phone'],
                cost=data['cost'],
                outcome=data['outcome'],
                call_duration=data['call_duration'],
                recording=data.get('recording', ''),
                summary=data.get('summary', ''),
                transcription=data.get('transcription', ''),
                campaign=campaign
            )
            return JsonResponse(result.to_dict(), status=201)
        except Campaign.DoesNotExist:
            return JsonResponse({'error': 'Invalid campaign ID'}, status=400)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, result_id):
        try:
            result = CampaignResult.objects.get(id=result_id)
            data = json.loads(request.body)
            
            if 'campaign_id' in data:
                result.campaign = Campaign.objects.get(id=data['campaign_id'])
            
            result.name = data.get('name', result.name)
            result.type = data.get('type', result.type)
            result.phone = data.get('phone', result.phone)
            result.cost = data.get('cost', result.cost)
            result.outcome = data.get('outcome', result.outcome)
            result.call_duration = data.get('call_duration', result.call_duration)
            result.recording = data.get('recording', result.recording)
            result.summary = data.get('summary', result.summary)
            result.transcription = data.get('transcription', result.transcription)
            
            result.save()
            return JsonResponse(result.to_dict())
        except CampaignResult.DoesNotExist:
            return JsonResponse({'error': 'Campaign Result not found'}, status=404)
        except Campaign.DoesNotExist:
            return JsonResponse({'error': 'Invalid campaign ID'}, status=400)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, result_id):
        try:
            result = CampaignResult.objects.get(id=result_id)
            result.delete()
            return JsonResponse({'message': 'Campaign Result deleted successfully'})
        except CampaignResult.DoesNotExist:
            return JsonResponse({'error': 'Campaign Result not found'}, status=404)
