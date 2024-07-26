from itertools import chain

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from platform_main.models import Campaign, Status


class CampaignsSerializer(ModelSerializer):
    source = SerializerMethodField('get_source')

    def get_source(self, instance: Campaign):
        return instance.source.system_id

    class Meta:
        model = Campaign
        fields = [
            'type',
            'format',
            'link',
            'platform',
            'os',
            'geo',
            'id',
            'source'
        ]


class ActiveCampaigns(APIView):
    @staticmethod
    def get(req: Request):
        active_campaigns = Campaign.objects.filter(current_status=Status.RUNNING.value)
        serializer = CampaignsSerializer(instance=active_campaigns, many=True)
        result = []
        for d in serializer.data:
            os_list = d['os']
            for _os in os_list:
                d['os'] = _os
                result.append(dict(d))
        return Response(result)
