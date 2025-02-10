from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet
from station.models import (TrainType,
                            Train,
                            Order,
                            Journey,
                            Crew,
                            Station,
                            Route)
from station.serializers import (TrainTypeSerializer,
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
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class TrainTypeViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer
