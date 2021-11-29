from rest_framework import serializers
from . import google, facebook
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer, ):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
            print(user_data['sub'])
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        from Full_Stack.settings import GOOGLE_CLIENT_ID
        if user_data['aud'] != GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')

        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, email=email, name=name)
