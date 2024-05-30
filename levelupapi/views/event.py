"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        events = Event.objects.all()
        event_game = request.query_params.get('game', None)
        if event_game is not None:
            events = events.filter(game_id=event_game)
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations, Returns: Response -- JSON serialized game instance"""
        gamer = Gamer.objects.get(pk=request.data["id"])
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            game = game,
            description = request.data["description"],
            date = request.data["date"],
            time = request.data["time"],
            organizer = gamer,
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def update(self, request, pk):
        
        game = Game.objects.get(pk=request.data["game"])
        gamer = Gamer.objects.get(pk=request.data["uid"])

        event = Event.objects.get(pk=pk)
        event.game = game
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.organizer = gamer

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = '__all__'

class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    class Meta:
        model = Gamer
        fields = '__all__'
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    game = GameSerializer()
    organizer = GamerSerializer()

    class Meta:
        model = Event
        fields = ('game', 'description', 'date', 'time', 'organizer')
