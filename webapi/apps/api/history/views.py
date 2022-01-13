from rest_framework import generics, permissions

from apps.api.history.models import HistoryLog
from apps.api.history.serializers import HistoryLogSerializer


class HistoryLogList(generics.ListAPIView):
  queryset = HistoryLog.objects.all()
  serializer_class = HistoryLogSerializer
  permission_classes = [permissions.AllowAny]

