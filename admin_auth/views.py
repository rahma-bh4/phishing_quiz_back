from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response



from rest_framework import status
from .models import Admin
from rest_framework.exceptions import APIException, AuthenticationFailed

import jwt,datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        # Recherche de l'utilisateur par email
        user = Admin.objects.filter(username=username).first()
      
        if user is None:
            raise AuthenticationFailed('Utilisateur introuvable!')
        if not user.check_password(password):
            raise AuthenticationFailed('Mot de passe incorrect!')

        # Création du payload pour le jeton JWT
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        
        # Génération du jeton JWT
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        # Envoi du jeton JWT dans les cookies
        response.set_cookie(key='jwt', value=token, httponly=True)

        # Ajout de l'ID de l'utilisateur dans la réponse
        response.data = {
            'jwt': token,
            'user_id': user.id  # Ajout de l'ID de l'utilisateur
        }
        return response
