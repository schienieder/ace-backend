from rest_framework import serializers
from api.models import Account, Admin, Client, BusinessPartner


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
        account.save()
        request = self.context["request"]
        if validated_data["role"] == "admin":
            admin = Admin.objects.create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                mobile_number=request.data["last_name"],
                email=request.data["email"],
                account=account,
            )
            admin.save()
        elif validated_data["role"] == "client":
            client = Client.objects.create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                mobile_number=request.data["mobile_number"],
                account=account,
            )
            client.save()
        else:
            partner = BusinessPartner.objects.create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                mobile_number=request.data["mobile_number"],
                account=account,
            )
            partner.save()
        print(request.data)
        return account


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
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
        extra_kwargs = {"id": {"read_only": True}}

    def update(self, instance, validated_data):
        client = Client.objects.get(account=instance)
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
            "account",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def update(self, instance, validated_data):
        # mobile_number = validated_data.pop("mobile_number")
        # email = validated_data.pop("email")
        partner = BusinessPartner.objects.get(account=instance)
        for (key, value) in validated_data.items():
            setattr(partner, key, value)
        partner.save()
        # if partner["mobile_number"] != mobile_number:
        #     partner.setattr(partner, "mobile_number", mobile_number)
        #     partner.save()
        # if partner["email"] != email:
        #     partner.setattr(partner, "email", email)
        #     partner.save()
        return partner
