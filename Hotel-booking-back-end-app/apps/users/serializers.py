from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # authenticate tùy theo bạn dùng USERNAME_FIELD là 'email' hay 'username'
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("Email hoặc mật khẩu không đúng.")
        if not user.is_active:
            raise serializers.ValidationError("Tài khoản chưa được kích hoạt.")

        refresh = RefreshToken.for_user(user)
        attrs["user"] = user
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        return attrs

    def get_user(self, obj):
        user = obj.get("user")
        return {
            "id": user.id,
            "email": getattr(user, "email", None),
            "username": getattr(user, "username", None),
            # thêm trường khác nếu cần
        }
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user