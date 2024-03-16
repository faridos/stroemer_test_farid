"""
File: views.py
Author: Farid Maghraoui
Description: This file contains views for generating and refreshing JWT tokens using the Django Rest Framework
             SimpleJWT library.
"""
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def generate_token(request):
    """
    Generate a JWT token pair (access token and refresh token) without associating it with any user.

    This view generates a JWT token pair (access token and refresh token) without associating it with any specific user.
    The access token is used for authentication, while the refresh token is used to obtain a new access token when the current one expires.

    Usage:
    ------
    POST request to generate a JWT token pair.
    No request data is required.

    Returns:
    --------
    A JSON response containing the generated JWT token pair (refresh token and access token).
        """
    token = RefreshToken()
    return Response({
        'refresh': str(token),
        'access': str(token.access_token),
    })


@api_view(['POST'])
def refresh_token(request):
    """
    Refresh the access token based on the provided refresh token.

    This view refreshes the access token based on the provided refresh token.
    If the refresh token is valid, it generates a new access token; otherwise, it returns an error response.

    Usage:
    ------
    POST request to refresh the access token.
    Request data should include the refresh token.

    Returns:
    --------
    A JSON response containing the new access token if the refresh token is valid;
    otherwise, an error response indicating an invalid refresh token.
    """
    refresh_token = request.data.get('refresh_token')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({'access_token': access_token})
        except TokenError as e:
            return Response({'error': 'Invalid refresh token'}, status=400)
    else:
        return Response({'error': 'Refresh token not provided'}, status=400)
