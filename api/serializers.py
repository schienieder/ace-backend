from rest_framework import serializers
from api.models import (
    Account,
    Admin,
    AffiliationRequest,
    Chat,
    Client,
    BusinessPartner,
    EventBookings,
    Event,
    InterviewSchedule,
    Rating,
    ChatRoom,
    RoomMember,
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
            # CREATE ROOM FOR CLIENT
            client_room = ChatRoom.objects.create(
                room_name=f"{client.first_name} {client.last_name}",
                room_key=validated_data["username"],
            )
            client_room.save()
            # ADD CLIENT AS ROOM MEMBER
            room_member_client = RoomMember.objects.create(
                room=client_room, member=validated_data["username"]
            )
            room_member_client.save()
            # CREATE A CLIENT ROOM AFTER A CLIENT USERS REGISTERS
            # client_room = ClientRoom.objects.create(
            #     room_name=validated_data["username"], client=client
            # )
            # client_room.save()
        else:
            partner = BusinessPartner.objects.create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                mobile_number=request.data["mobile_number"],
                email=request.data["email"],
                account=account,
            )
            partner.save()
            # CREATE A ROOM FOR PARTNER
            partner_room = ChatRoom.objects.create(
                room_name=f"{partner.first_name} {partner.last_name}",
                room_key=validated_data["username"],
            )
            partner_room.save()
            # ADD PARTNER AS ROOM MEMBER
            room_member_partner = RoomMember.objects.create(
                room=partner_room, member=validated_data["username"]
            )
            room_member_partner.save()
            # CREATE A PARTNER ROOM AFTER A CLIENT USERS REGISTERS
            # partner_room = PartnerRoom.objects.create(
            #     room_name=validated_data["username"], partner=partner
            # )
            # partner_room.save()
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
            "permit_profile",
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
        extra_kwargs = {
            "id": {"read_only": True},
            "account": {"read_only": True},
        }

    def update(self, instance, validated_data):
        partner = instance
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


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBookings
        fields = ["event_month", "monthly_sales"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


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


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliationRequest
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class ChatMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class RoomMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMember
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username"]
        extra_kwargs = {"id": {"read_only": True}}


class ClientEmailMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "email", "mobile_number"]
        extra_kwargs = {"id": {"read_only": True}}


class PartnerEmailMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = ["id", "email", "mobile_number"]
        extra_kwargs = {"id": {"read_only": True}}
