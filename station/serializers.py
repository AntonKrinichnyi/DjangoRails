from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError
from station.models import (Train,
                            TrainType,
                            Ticket,
                            Journey,
                            Station,
                            Route,
                            Crew,
                            Order)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = "name"
    )
    destination = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = "name"
    )
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id",
                  "name",
                  "cargo_num",
                  "places_in_cargo",
                  "train_type",
                  "capacity")


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ("id",
                  "route",
                  "train",
                  "departure_time",
                  "arrival_time")


class JourneyListSerializer(JourneySerializer):
    route = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="full_route"
    )
    train = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )
    class Meta:
        model = Journey
        fields = ("id",
                  "route",
                  "train",
                  "departure_time",
                  "arrival_time")


class JourneyCreateSerializer(JourneySerializer):
    class Meta:
        model=Journey
        fields=("route",
                "train",
                "departure_time",
                "arrival_time")


class JourneyDetailSerializer(JourneySerializer):
    train = TrainSerializer()
    route = RouteListSerializer()
    class Meta:
        model=Journey
        fields=("route",
                "train",
                "departure_time",
                "arrival_time")


class TrainListSerializer(TrainSerializer):
    train_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )
    class Meta:
        model = Train
        fields = ("id",
                  "name",
                  "cargo_num",
                  "places_in_cargo",
                  "train_type",
                  "capacity")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey", "order")


class TicketListSerializer(TicketSerializer):
    journey = JourneyListSerializer(many=True, read_only=True)



class OrderSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(many=True, read_only=False, allow_empty=False)
    class Meta:
        model = Order
        fields = ("id", "created_at", "user")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
    