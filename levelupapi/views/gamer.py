from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Gamer

class GamerView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        gamer = Gamer.objects.get(pk=pk)
        serializer = GamerSerializer(gamer)
        return Response(serializer.data)

    def list(self, request):
        gamers = Gamer.objects.all()
        serializer = GamerSerializer(gamers, many=True)
        return Response(serializer.data)
    
    def create(self, request):

        gamer = Gamer.objects.create(
            uid=request.data["uid"],
            bio=request.data["bio"],
        )
        serializer = GamerSerializer(gamer)
        return Response(serializer.data)
    
    def update(self, request, pk):

        gamer = Gamer.objects.get(pk=pk)
        gamer.uid = request.data["uid"]
        gamer.bio = request.data["bio"]
        gamer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Gamer
        fields = ('uid', 'bio')