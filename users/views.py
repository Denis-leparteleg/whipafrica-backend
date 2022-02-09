from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User, ArtistData
import jwt, datetime
from django.shortcuts import  render
import requests
import json

from django.core import serializers
# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'email':email,
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
class StatsView(APIView):
    def get(self, request):
        
        url = "https://songstats.p.rapidapi.com/artists/stats"
        
        querystring = {"source":"all","spotify_artist_id":"5nnVpORg4Aha9aWRTZA5No"}
        
        headers = {
            'x-rapidapi-host': "songstats.p.rapidapi.com",
            
            'x-rapidapi-key': ""
            }
        
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        
        result=response["result"]
        
        stats=response["stats"]
        
        source=stats[0]["source"]
        
        info = response["artist_info"]
     
        name = info["name"]
        
        image = info["avatar"]
      
        data=stats[0]["data"]
        
        artist = ArtistData.objects.create(name=name, image=image, stats=data)
        
        artist.save()
        
        print(artist)
        
        return Response(data)
    
    
class PopularView(APIView):
    
    def get(self, request):

        artist = ArtistData.objects.all()
       
        artist_list = serializers.serialize('json', artist)
        
        print(artist_list)
        
        return Response(artist_list)    

