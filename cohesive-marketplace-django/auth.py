import http

from cohesive.error import AuthenticationError
from django.http import HttpResponse
from cohesive.auth import validate_token


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the Authorization header
        authorization_header = request.headers['Authorization']
        if not authorization_header:
            return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

        # Get the token from the header
        token = authorization_header.replace('Bearer ', '')

        # Validate the token
        try:
            auth_details = validate_token(token)
        except AuthenticationError as e:
            return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

        # Set the auth details in the request
        request.auth_details = auth_details

        # Process the request
        return self.get_response(request)
