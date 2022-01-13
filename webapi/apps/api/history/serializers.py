from rest_framework import serializers
from .models import *
import json


class HistoryLogSerializer(serializers.ModelSerializer):
    input_data = serializers.SerializerMethodField()
    output_data = serializers.SerializerMethodField()

    class Meta:
        model = HistoryLog
        fields = [
            'grade',
            'created_at',
            'input_data',
            'output_data'
        ]

    def get_input_data(self, object):
        return json.loads(object.input_data)

    def get_output_data(self, object):
        return json.loads(object.output_data)
