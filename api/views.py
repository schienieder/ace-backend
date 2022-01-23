from django.db.models import query
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from api.serializers import (
    AccountSerializer,
    ClientSerializer,
    BusinessPartnerSerializer,
    EventBookingSerializer,
    EventSerializer,
    InterviewSerializer,
)
from api.models import (
    Account,
    Client,
    BusinessPartner,
    EventBookings,
    Event,
    InterviewSchedule,
)
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
class CreateAccountView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAccountView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


# CLIENT VIEWS
class AdminGetClientView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        pid = self.kwargs["pk"]
        queryset = get_object_or_404(Client, pk=pid)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GetClientProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        queryset = Client.objects.get(account__id=self.request.user.id)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateClientProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        client = Client.objects.get(account__id=request.user.id)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdateClientProfileView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = ClientSerializer
#     queryset = Client.objects.all()

#     def update(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             request.user, data=request.data, partial=True
#         )

#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestroyClientProfileView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = Client.objects.filter(pk=self.kwargs["pk"])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Client Deleted Successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


# PARTNER  VIEWS
class AdminGetPartnerView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessPartnerSerializer
    queryset = BusinessPartner.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        pid = self.kwargs["pk"]
        queryset = get_object_or_404(BusinessPartner, pk=pid)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GetPartnerProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessPartnerSerializer
    queryset = BusinessPartner.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        queryset = BusinessPartner.objects.get(account__id=self.request.user.id)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdatePartnerProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessPartnerSerializer
    queryset = BusinessPartner.objects.all()

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestroyPartnerProfileView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessPartnerSerializer

    def get_queryset(self):
        queryset = BusinessPartner.objects.filter(pk=self.kwargs["pk"])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Partner Deleted Successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


# BOOKING VIEWS
class CreateBookingView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventBookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBookingView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventBookingSerializer
    queryset = EventBookings.objects.all()


class GetClientBookingView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventBookingSerializer
    queryset = EventBookings.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        client = Client.objects.get(account__id=self.request.user.id)
        my_obj = get_object_or_404(queryset, booked_by=client)
        return my_obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DestroyEventBookingView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventBookingSerializer

    def get_queryset(self):
        queryset = EventBookings.objects.filter(pk=self.kwargs["pk"])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Booking Deleted Successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


# INTERVIEW SCHEDULE VIEWS
class CreateInterviewView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSerializer
    queryset = InterviewSchedule.objects.all()


# EVENT VIEWS
class CreateEventView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetEventView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class DestroyEventView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


# LIST VIEWS
class AllBusinessPartnersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessPartnerSerializer
    queryset = BusinessPartner.objects.all()


class AllClientsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessPartnerSerializer
    queryset = Client.objects.all()


class AllClientBookingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventBookingSerializer
    queryset = EventBookings.objects.all()


class AllEventsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
