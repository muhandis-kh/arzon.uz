from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
  # Ro'yhatdan o'tish vaqtida parolni tekshirish uchun password2 maydoni yaratib olindi
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields = (
            "username",
            "password",
            "password2",
        )
    extra_kwargs={
      'password':{'write_only':True}
    }

  # parollarni validatsiyadan o'tkazish va bir biriga mosligini tekshirib chiqamiz
  def validate(self, attrs):
    print(attrs)
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Kiritilgan parollar birxil emas !!!")
    return attrs

  def create(self, validate_data):
      print(validate_data)
      try:
        return User.objects.create_user(username=validate_data['username'], password=validate_data['password'])
      except Exception as e:
          print(e)