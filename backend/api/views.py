from rest_framework import viewsets

from .models import PersonsCount
from .serializers import PersonsCountSerializer


# Create your views here.


class PersonsCountSet(viewsets.ModelViewSet):
    queryset = PersonsCount.objects.all().order_by('-time')
    serializer_class = PersonsCountSerializer
    # permission_classes = [permissions.IsAuthenticated]
