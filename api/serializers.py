from rest_framework import serializers
from api.models import Account, Profile, BusinessPartner


class CreateAccountSerializer(serializers.ModelSerializer):
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
        if validated_data["role"] != "partner":
            profile = Profile.objects.create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                mobile_number=request.data["mobile_number"],
                account=account,
            )
            profile.save()
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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
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
        profile = Profile.objects.get(account=instance)
        for (key, value) in validated_data.items():
            setattr(profile, key, value)
        profile.save()


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "mobile_number",
            "email",
            "account",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def update(self, instance, validated_data):
        partner = BusinessPartner.objects.get(account=instance)
        for (key, value) in validated_data.items():
            setattr(partner, key, value)
        partner.save()
