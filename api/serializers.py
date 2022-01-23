from rest_framework import serializers
from api.models import (
    Account,
    Admin,
    Client,
    BusinessPartner,
    EventBookings,
    Event,
    InterviewSchedule,
)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "password", "role"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        account = Account.objects.create(
            username=validated_data["username"], role=validated_data["role"]
        )
        account.set_password(validated_data["password"])
        request = self.context["request"]
        if validated_data["role"] == "admin":
            admin = Admin.objects.create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                mobile_number=request.data["mobile_number"],
                email=request.data["email"],
                account=account,
            )
            admin.save()
        elif validated_data["role"] == "client":
            client = Client.objects.create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                mobile_number=request.data["mobile_number"],
                email=request.data["email"],
                account=account,
            )
            client.save()
        else:
            partner = BusinessPartner.objects.create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                mobile_number=request.data["mobile_number"],
                email=request.data["email"],
                account=account,
            )
            partner.save()
        account.save()
        print(request.data)
        return account


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "profile_image",
            "first_name",
            "last_name",
            "mobile_number",
            "email",
            "sex",
            "birthdate",
            "street_address",
            "city",
            "state_province",
            "postal_zip",
            "account",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "account": {"read_only": True},
        }

    def update(self, instance, validated_data):

        client = instance

        if getattr(client, "mobile_number") == validated_data["mobile_number"]:
            validated_data.pop("mobile_number")

        if getattr(client, "email") == validated_data["email"]:
            validated_data.pop("email")

        for (key, value) in validated_data.items():
            setattr(client, key, value)

        client.save()
        return client


class BusinessPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = [
            "id",
            "first_name",
            "last_name",
            "mobile_number",
            "email",
            "business_name",
            "type_of_business",
            "street_address",
            "city",
            "state_province",
            "postal_zip",
            "services_offered",
            "account",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def update(self, instance, validated_data):
        partner = BusinessPartner.objects.get(account=instance)
        print("Previous mobile number: ", getattr(partner, "mobile_number"))
        print("New mobile number: ", validated_data["mobile_number"])

        if getattr(partner, "mobile_number") == validated_data["mobile_number"]:
            validated_data.pop("mobile_number")

        if getattr(partner, "email") == validated_data["email"]:
            validated_data.pop("email")

        for (key, value) in validated_data.items():
            setattr(partner, key, value)

        partner.save()
        return partner


class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBookings
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        event = Event.objects.create(
            event_name=validated_data["event_name"],
            venue_name=validated_data["venue_name"],
            venue_lat=validated_data["venue_lat"],
            venue_long=validated_data["venue_long"],
            event_date=validated_data["event_date"],
            time_schedule=validated_data["time_schedule"],
            event_budget=validated_data["event_budget"],
            client=validated_data["client"],
        )
        event.save()
        return event


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSchedule
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        interview = InterviewSchedule.objects.create(
            location=validated_data["location"],
            date=validated_data["date"],
            time=validated_data["time"],
            client=validated_data["client"],
            booking=validated_data["booking"],
        )
        interview.save()
        return interview
