from rest_framework import serializers

from .models import Account


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "profile_image",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = Account.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.profile_image = validated_data.get("profile_image", instance.profile_image)
        instance.save()
        return instance

    def validate_first_name(self, value):
        return value.title()

    def validate_last_name(self, value):
        return value.title()

    def validate_email(self, value):
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exist!")
        return value.strip().lower()

    def validate_gender(self, value):
        return value.title()

    def validate_password(self, value):
        return value.strip()

    def to_internal_value(self, data):
        if "gender" in data:
            data["gender"] = data["gender"].strip().title()
        return super().to_internal_value(data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate_email(self, value):
        return value.strip().lower()

    def validate_password(self, value):
        return value.strip()

    def validate(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        if not email and not password:
            raise serializers.ValidationError("Both fields are required!")
        return validated_data


class ReadAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "profile_image",
            "user_type",
            "account_status",
            "is_2fa_enabled",
            "is_email_verified",
            "is_admin_user",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def validate(self, validated_data):
        password = validated_data.get("password")
        confirm_password = validated_data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match!")
        return validated_data

class DeleteAccountSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=255, required=False)
    type_delete = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=100)

    def validate_type_delete(self, value):
        if value != "DELETE":
            raise serializers.ValidationError("Incorrect keyword 'DELETE'")
        return value


class SetasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=80)
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def validate(self, validated_data):
        token = validated_data.get("token")
        password = validated_data.get("password")
        confirm_password = validated_data.get("confirm_password")

        if not token:
            raise serializers.ValidationError("Token is required")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match!")
        return validated_data


class VerifyAccountSetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=100)

    def validate_token(self, value):
        if not value.strip():
            raise serializers.ValidationError("Token cannot be empty.")
        return value.strip().upper()

    def validate_password(self, value):
        if len(value.strip()) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters.")
        return value.strip()
