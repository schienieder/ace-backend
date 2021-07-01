from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from api.serializers import CreateAccountSerializer

# Create your views here.
class CreateAccountView(generics.CreateAPIView):
    serializer_class = CreateAccountSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginAccountView(generics.RetrieveAPIView):
# serializer_class =
# permission_classes =
