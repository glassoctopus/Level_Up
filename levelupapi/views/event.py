"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer, Event_gamer
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed

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
            
        uid = request.META.get('HTTP_AUTHORIZATION')
    
        if uid is None:
            raise AuthenticationFailed('Authorization header not found')

        try:
            gamer = Gamer.objects.get(uid=uid)
        except Gamer.DoesNotExist:
            raise AuthenticationFailed('Gamer not found')

        for event in events:
            # Check to see if there is a row in the Event Games table that has the passed in gamer and event
            event.joined = len(Event_gamer.objects.filter(
                gamer=gamer, event=event)) > 0

        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations, Returns: Response -- JSON serialized game instance"""
        gamer = Gamer.objects.get(uid=request.data["uid"])
        game = Game.objects.get(title=request.data["title"])

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
        try:
            game = Game.objects.get(pk=request.data["title"])
            gamer = Gamer.objects.get(pk=request.data["uid"])
        except KeyError:
            return Response({"error": "ID not provided in request."}, status=status.HTTP_400_BAD_REQUEST)

        event = Event.objects.get(pk=pk)
        event.game = game
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.organizer = gamer

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Event.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(pk=request.data["uid"])
        event = Event.objects.get(pk=pk)
        attendee = Event_gamer.objects.create(
            gamer=gamer,
            event=event
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to sign out of an event"""
        try:
            # Ensure the uid is being accessed correctly
            if 'uid' not in request.data:
                return Response({'error': 'uid is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            gamer = Gamer.objects.get(pk=request.data["uid"])
            event = Event.objects.get(pk=pk)
            attendee = Event_gamer.objects.get(gamer=gamer, event=event)
            attendee.delete()
            return Response({'message': 'Gamer removed from event'}, status=status.HTTP_204_NO_CONTENT)
        except Gamer.DoesNotExist:
            return Response({'error': 'Gamer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except Event_gamer.DoesNotExist:
            return Response({'error': 'Gamer is not signed up for this event'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({'error': f'Missing field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        fields = ('game', 'description', 'date', 'time', 'organizer', 'id', 'joined')
