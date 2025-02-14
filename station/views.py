from datetime import datetime
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
from station.serializers import (JourneyCreateSerializer, JourneyDetailSerializer, JourneyListSerializer, RouteListSerializer, TrainListSerializer, TrainTypeSerializer,
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
    queryset = (Route.objects.all().
                select_related("train", "route__sorce__name", "route__destination__name"))
    serializer_class = RouteSerializer
    
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
                select_related("train", "route__source", "route__destination"))
    serializer_class = JourneySerializer
    
    def get_queryset(self):
        departure_date = self.request.query_params.get("date")
        route_id_str = self.request.query_params.get("route")

        queryset = self.queryset

        if departure_date:
            departure_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
            queryset = queryset.filter(departure__date=departure_date)

        if route_id_str:
            queryset = queryset.filter(route_id=int(route_id_str))

        return queryset
    
    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        if self.action == "post":
            return JourneyCreateSerializer
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return JourneySerializer
