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


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    train_type_name = serializers.CharField(source="train_type.name",
                                            read_only=True)
    crew = CrewSerializer(many=True, read_only=True)
    class Meta:
        model = Train
        fields = ("id",
                  "name",
                  "crew",
                  "cargo_num",
                  "places_in_cargo",
                  "train_type_name",
                  "capacity")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey", "order")


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ("id",
                  "route",
                  "train",
                  "departure_time",
                  "arrival_time")


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
    pass
    