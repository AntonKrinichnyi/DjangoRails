from django.db.models import F
from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet
from station.models import (TrainType,
                            Train,
                            Order,
                            Journey,
                            Crew,
                            Station,
                            Route)
from station.serializers import (JourneyListSerializer, RouteListSerializer, TrainListSerializer, TrainTypeSerializer,
                                 TrainSerializer,
                                 OrderListSerializer,
                                 OrderSerializer,
                                 JourneySerializer,
                                 RouteSerializer,
                                 StationSerializer,
                                 CrewSerializer)


class CrewViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = Route.objects.all().select_related()
    serializer_class = RouteSerializer
    
    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        
        queryset = self.queryset
        
        if source:
            source_id = int(self.source)
            queryset = queryset.filter(source__id=source_id)
        
        if destination:
            destination_id = int(self.destination)
            queryset = queryset.filter(destination__id=destination_id)
        
        return queryset.distinct()
        
    
    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer


class TrainTypeViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all().select_related("train_type")
    serializer_class = TrainSerializer
    
    def get_queryset(self):
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        return TrainSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = (Journey.objects.
                select_related())
    serializer_class = JourneySerializer
    
    def get_serializer_class(self):
        if self.action in ("list", "post"):
            return JourneyListSerializer
        return JourneySerializer
