from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.permissions import IsAdminUser


@api_view(['POST'])
def register_alumni(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAlumniAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, role='alumni')

            if user.is_verified:
                return Response({'message': 'User is already verified.'}, status=status.HTTP_200_OK)

            user.is_verified = True
            user.save()
            return Response({'message': 'Alumni user verified successfully.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Alumni user not found.'}, status=status.HTTP_404_NOT_FOUND)