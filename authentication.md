For this project I will be using the Token Based Authentication which is a django REST Framework authentication.

Steps to Implement Token Authentication with Django Rest Framework:
Install Django Rest Framework and Django Rest Framework Authtoken: First, you need to install DRF and rest_framework.authtoken.

Run:

bash/ console

pip install djangorestframework
pip install djangorestframework-simplejwt
Add rest_framework and rest_framework.authtoken to INSTALLED_APPS: Add these apps to your INSTALLED_APPS in settings.py.


INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    ...
]
Add Token Authentication to Settings: In settings.py, configure the Django Rest Framework to use token authentication by adding the following under the REST_FRAMEWORK settings.


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
Create a User Registration Endpoint: Add an endpoint for users to register and obtain a token.

In views.py, you can create a simple registration view.

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RegisterUserView(APIView):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['username', 'password', 'email']

    def post(self, request):
        serializer = self.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
URL Configuration: Add the URL pattern for the registration view.

from django.urls import path
from .views import RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('api-token-auth/', obtain_auth_token),  # Optional: For getting the token manually
]
Protect API Views with Token Authentication: Use the IsAuthenticated permission class to restrict access to authenticated users.


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class MovieListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        movies = Movie.objects.all()
        # Serialize and return movie data
        return Response({"movies": movies})
How to Test Authentication
Testing Token Authentication:

Step 1: Register a new user by sending a POST request to /register/ with the username, password, and email.
Step 2: Get the token from the response.
Step 3: Send a request to a protected API endpoint (e.g., /movies/) with the token in the Authorization header:
bash/Postman
GET /movies/
Authorization: Token <your_token>
Test with Postman or cURL: You can use tools like Postman or cURL to make requests to the API endpoints:

To get a token:
bash
Copy code
POST http://localhost:8000/register/
Content-Type: application/json
{
  "username": "testuser",
  "password": "password123",
  "email": "test@example.com"
}
To access a protected endpoint:
bash
Copy code
GET http://localhost:8000/movies/
Authorization: Token <your_token>
GitHub Repository
Please find the updated code with authentication on the GitHub Repository.

Markdown Explanation of the Authentication Setup:
markdown
Copy code
## Movie Review API Authentication Setup

This API uses token-based authentication for secure access to protected resources.

### Steps to Test Authentication:

1. **Register a New User**:
   - Send a `POST` request to `/register/` with `username`, `password`, and `email` to create a new user.

   Example request:
   ```bash
   POST /register/
   Content-Type: application/json
   {
     "username": "testuser",
     "password": "password123",
     "email": "test@example.com"
   }
Response will contain a token:

json
Copy code
{
  "token": "your_token_here"
}
Access a Protected Resource:

Use the received token to access protected resources.
Include the token in the Authorization header:
Example request:

bash
Copy code
GET /movies/
Authorization: Token your_token_here
Response:

json
Copy code
{
  "movies": [ ... ]
}