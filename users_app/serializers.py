
from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


# class donerSerialaizers(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(many=False)
#     blood_group = serializers.StringRelatedField(many=True)
#     class Meta:
#          model=models.doner
#          fields='__all__'




class donerSerialaizers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)  # For displaying user as string
    blood_group = serializers.StringRelatedField(many=False)  # For displaying blood group as string
    # Use PrimaryKeyRelatedField for write operations
    user_id = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all(), source='user')
    blood_group_id = serializers.PrimaryKeyRelatedField(queryset=models.BloodGroup.objects.all(), source='blood_group')

    class Meta:
        model = models.doner
        # fields = '__all__'
        fields = ['id', 'user', 'blood_group', 'Mobile_number', 'city', 'Street', 'other', 'date_bath', 'image', 'user_id', 'blood_group_id','age','last_donation_date','is_available']
        read_only_fields = ['user', 'blood_group'] 


class blood_group_Serialaizers(serializers.ModelSerializer):
   
   class Meta:
        model=models.BloodGroup
        fields='__all__'



class RegistrationSerialaizers(serializers.ModelSerializer):
   confirm_password = serializers.CharField(required=True)

   class Meta:
      model = User
      fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

   def save(self):
      # Retrieve validated data
      username = self.validated_data['username']
      first_name = self.validated_data['first_name']
      last_name = self.validated_data['last_name']
      email = self.validated_data['email']
      password = self.validated_data['password']
      confirm_password = self.validated_data['confirm_password']

      # Validate that the passwords match
      if password != confirm_password:
         raise serializers.ValidationError({'error': "Passwords don't match"})

      # Check if the email already exists
      if User.objects.filter(email=email).exists():
         raise serializers.ValidationError({'error': "Email already exists"})

      # Create the User instance, but don't pass confirm_password
      user = User(username=username, email=email, first_name=first_name, last_name=last_name)
      user.set_password(password)  # Ensure the password is hashed before saving
      user.is_active=False
      user.save()

      return user



class UserLogInSerializers(serializers.Serializer):
   username=serializers.CharField(required=True)
   password=serializers.CharField(required=True)



class BloodRequestSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = models.BloodRequest
        fields = '__all__'

   #  def create(self, validated_data):
   #      return  models.BloodRequest.objects.create(created_by=self.context['request'].user, **validated_data)
        

class BloodRequestAcceptanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BloodRequestAcceptance
        fields = ['blood_request', 'accepted_by']

    def validate(self, data):
        user = self.context['request'].user

        # Ensure only donors can accept requests
        if not models.doner.objects.filter(user=user).exists():
            raise serializers.ValidationError("Only registered donors can accept requests.")

        # Ensure request is not already completed
        if data['blood_request'].is_completed:
            raise serializers.ValidationError("This request has already been accepted.")

        # Ensure request is not accepted by the requester themselves
        if data['blood_request'].created_by == user:
            raise serializers.ValidationError("You cannot accept your own request.")

        return data

    def create(self, validated_data):
        blood_request = validated_data['blood_request']
        accepted_by = validated_data['accepted_by']

        # Mark request as completed
        blood_request.is_completed = True
        blood_request.save()

        # Save the acceptance
        return models.BloodRequestAcceptance.objects.create(
            blood_request=blood_request,
            accepted_by=accepted_by
        )

