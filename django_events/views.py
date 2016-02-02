from rest_framework import viewsets
from .serializers import *
from .models import *


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# TODO: приспособить api key к views
# class UserDetailView(APIView):
#     metadata_class = MinimalMetadata
#
#     def get(self, request, username, format=None):
#         try:
#             _api_key = request.GET.get('api_key', None)
#             ApiKey.objects.get(key=_api_key, is_active=True)
#         except ApiKey.DoesNotExist:
#             raise PermissionDenied
#
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             raise Http404
#
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
