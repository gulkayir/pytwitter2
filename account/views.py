from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Tweet
from main.serializers import TweetSerializer
from .utils import send_activation_mail
from account.serializers import RegisterSerializer, LoginSerializer, CreateNewPasswordSerializer, FollowSerializer, \
    UserSerializer, SearchSerializer

User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registrated!', status=status.HTTP_201_CREATED)
        return Response('Not valid', status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Your account successfully activated! ', status=status.HTTP_200_OK)



class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logget out', status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def get(self, request):
        email = email = request.query_params.get('email')
        User = get_user_model()
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_mail.delay(email=email, activation_code=str(user.activation_code))
        return Response('Activation code has been sent to your email', status=status.HTTP_200_OK)


class ResetComplete(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Password reseted successfully', status=200)

class ProfileView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]


class MyProfile(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None, pk=None):
        email = self.request.user.email
        query = get_user_model().objects.get(email=email)
        serializer = UserSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)



class SearchViewSet(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = SearchSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(email__icontains=search)
        return queryset


class FeedsView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None, pk=None):
        user = self.request.user
        followings = user.followings.all()
        print(followings)
        tweets = Tweet.objects.filter(author__in=followings)
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None, username=None):
        to_user = get_user_model().objects.get(username=username)
        from_user = self.request.user
        follow = None
        if from_user != to_user:
            if from_user in to_user.followers.all():
                follow = False
                from_user.followings.remove(to_user)
                to_user.followers.remove(from_user)

            else:
                follow = True
                from_user.followings.add(to_user)
                to_user.followers.add(from_user)
        else:
            raise Exception('You cant follow yourself')
        context = {'follow': follow}
        return Response(context)


class GetFollowersView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(username=username).followers.all()
        return queryset


class GetFollowingsView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(username=username).followings.all()
        return queryset
