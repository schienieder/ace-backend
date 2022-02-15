from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers import (
    AccountSerializer,
    AffiliationSerializer,
    ClientSerializer,
    BusinessPartnerSerializer,
    EventBookingSerializer,
    EventSerializer,
    InterviewSerializer,
    RatingSerializer,
    ClientRoomSerializer,
    PartnerRoomSerializer,
    GroupRoomSerializer,
    ClientGroupRoomSerializer,
    PartnerGroupRoomSerializer,
)
from api.models import (
    Account,
    Client,
    BusinessPartner,
    EventBookings,
    Event,
    InterviewSchedule,
    AffiliationRequest,
    Rating,
    ClientRoom,
    PartnerRoom,
    GroupRoom,
    ClientGroupRoom,
    PartnerGroupRoom,
)
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render
import base64
from email.mime.image import MIMEImage
import os

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


class UpdatePartnerProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        partner = BusinessPartner.objects.get(account__id=request.user.id)
        serializer = BusinessPartnerSerializer(partner, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdatePartnerProfileView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BusinessPartnerSerializer
#     queryset = BusinessPartner.objects.all()

#     def update(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             request.user, data=request.data, partial=True
#         )

#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class UpdateBookingView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventBookingSerializer
    queryset = EventBookings.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        client_id = request.data["client"]
        client = Client.objects.get(pk=client_id)

        with open("media/Email Image.png", "rb") as img_file:
            my_img = MIMEImage(img_file.read())
            my_img.add_header("Content-ID", "<{name}>".format(name="email_img"))
            my_img.add_header("Content-Disposition", "inline", filename="email_img")
        context = {
            "my_img": my_img,
            "client_name": client.first_name + " " + client.last_name,
            "date_schedule": request.data["date"],
            "time_schedule": request.data["time"],
            "location": request.data["location"],
        }

        subject = "Alas Creative Events Interview"
        template = render_to_string("api/email_template.html", context)

        email_from = settings.EMAIL_HOST_USER
        recipient = ["schieniezel@gmail.com"]

        my_email = EmailMultiAlternatives(subject, template, email_from, recipient)
        my_email.mixed_subtype = "related"
        my_email.attach_alternative(template, "text/html")
        my_email.attach(my_img)

        my_email.send(fail_silently=False)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetInterviewView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSerializer
    queryset = InterviewSchedule.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        my_obj = get_object_or_404(queryset, client__id=self.kwargs["pk"])
        return my_obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DestroyInterviewView(generics.DestroyAPIView):
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


class GetClientEventView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        client = Client.objects.get(account__id=self.request.user.id)
        my_obj = get_object_or_404(queryset, client=client)
        return my_obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateEventView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestroyEventView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


# AFFILIATION VIEWS
class CreateAffiliationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationRequest.objects.all()


class GetAffiliationView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationRequest.objects.all()


class UpdateRequestView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationRequest.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# RATING VIEWS
class CreateRatingView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()


class GetVenueRateForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        january_rates = Rating.objects.filter(event_date__month="01").aggregate(
            Avg("venue_rate")
        )
        february_rates = Rating.objects.filter(event_date__month="02").aggregate(
            Avg("venue_rate")
        )
        march_rates = Rating.objects.filter(event_date__month="03").aggregate(
            Avg("venue_rate")
        )
        april_rates = Rating.objects.filter(event_date__month="04").aggregate(
            Avg("venue_rate")
        )
        may_rates = Rating.objects.filter(event_date__month="05").aggregate(
            Avg("venue_rate")
        )
        june_rates = Rating.objects.filter(event_date__month="06").aggregate(
            Avg("venue_rate")
        )
        july_rates = Rating.objects.filter(event_date__month="07").aggregate(
            Avg("venue_rate")
        )
        august_rates = Rating.objects.filter(event_date__month="08").aggregate(
            Avg("venue_rate")
        )
        september_rates = Rating.objects.filter(event_date__month="09").aggregate(
            Avg("venue_rate")
        )
        october_rates = Rating.objects.filter(event_date__month="10").aggregate(
            Avg("venue_rate")
        )
        november_rates = Rating.objects.filter(event_date__month="11").aggregate(
            Avg("venue_rate")
        )
        december_rates = Rating.objects.filter(event_date__month="12").aggregate(
            Avg("venue_rate")
        )
        venue_rates = [
            {"month": "January", "venue": january_rates["venue_rate__avg"]},
            {"month": "February", "venue": february_rates["venue_rate__avg"]},
            {"month": "March", "venue": march_rates["venue_rate__avg"]},
            {"month": "April", "venue": april_rates["venue_rate__avg"]},
            {"month": "May", "venue": may_rates["venue_rate__avg"]},
            {"month": "June", "venue": june_rates["venue_rate__avg"]},
            {"month": "July", "venue": july_rates["venue_rate__avg"]},
            {"month": "August", "venue": august_rates["venue_rate__avg"]},
            {"month": "September", "venue": september_rates["venue_rate__avg"]},
            {"month": "October", "venue": october_rates["venue_rate__avg"]},
            {"month": "November", "venue": november_rates["venue_rate__avg"]},
            {"month": "December", "venue": december_rates["venue_rate__avg"]},
        ]
        return Response(venue_rates)


class GetCateringRateForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        january_rates = Rating.objects.filter(event_date__month="01").aggregate(
            Avg("catering_rate")
        )
        february_rates = Rating.objects.filter(event_date__month="02").aggregate(
            Avg("catering_rate")
        )
        march_rates = Rating.objects.filter(event_date__month="03").aggregate(
            Avg("catering_rate")
        )
        april_rates = Rating.objects.filter(event_date__month="04").aggregate(
            Avg("catering_rate")
        )
        may_rates = Rating.objects.filter(event_date__month="05").aggregate(
            Avg("catering_rate")
        )
        june_rates = Rating.objects.filter(event_date__month="06").aggregate(
            Avg("catering_rate")
        )
        july_rates = Rating.objects.filter(event_date__month="07").aggregate(
            Avg("catering_rate")
        )
        august_rates = Rating.objects.filter(event_date__month="08").aggregate(
            Avg("catering_rate")
        )
        september_rates = Rating.objects.filter(event_date__month="09").aggregate(
            Avg("catering_rate")
        )
        october_rates = Rating.objects.filter(event_date__month="10").aggregate(
            Avg("catering_rate")
        )
        november_rates = Rating.objects.filter(event_date__month="11").aggregate(
            Avg("catering_rate")
        )
        december_rates = Rating.objects.filter(event_date__month="12").aggregate(
            Avg("catering_rate")
        )
        catering_rates = [
            {"month": "January", "catering": january_rates["catering_rate__avg"]},
            {"month": "February", "catering": february_rates["catering_rate__avg"]},
            {"month": "March", "catering": march_rates["catering_rate__avg"]},
            {"month": "April", "catering": april_rates["catering_rate__avg"]},
            {"month": "May", "catering": may_rates["catering_rate__avg"]},
            {"month": "June", "catering": june_rates["catering_rate__avg"]},
            {"month": "July", "catering": july_rates["catering_rate__avg"]},
            {"month": "August", "catering": august_rates["catering_rate__avg"]},
            {"month": "September", "catering": september_rates["catering_rate__avg"]},
            {"month": "October", "catering": october_rates["catering_rate__avg"]},
            {"month": "November", "catering": november_rates["catering_rate__avg"]},
            {"month": "December", "catering": december_rates["catering_rate__avg"]},
        ]
        return Response(catering_rates)


class GetStylingRateForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        january_rates = Rating.objects.filter(event_date__month="01").aggregate(
            Avg("styling_rate")
        )
        february_rates = Rating.objects.filter(event_date__month="02").aggregate(
            Avg("styling_rate")
        )
        march_rates = Rating.objects.filter(event_date__month="03").aggregate(
            Avg("styling_rate")
        )
        april_rates = Rating.objects.filter(event_date__month="04").aggregate(
            Avg("styling_rate")
        )
        may_rates = Rating.objects.filter(event_date__month="05").aggregate(
            Avg("styling_rate")
        )
        june_rates = Rating.objects.filter(event_date__month="06").aggregate(
            Avg("styling_rate")
        )
        july_rates = Rating.objects.filter(event_date__month="07").aggregate(
            Avg("styling_rate")
        )
        august_rates = Rating.objects.filter(event_date__month="08").aggregate(
            Avg("styling_rate")
        )
        september_rates = Rating.objects.filter(event_date__month="09").aggregate(
            Avg("styling_rate")
        )
        october_rates = Rating.objects.filter(event_date__month="10").aggregate(
            Avg("styling_rate")
        )
        november_rates = Rating.objects.filter(event_date__month="11").aggregate(
            Avg("styling_rate")
        )
        december_rates = Rating.objects.filter(event_date__month="12").aggregate(
            Avg("styling_rate")
        )
        styling_rates = [
            {"month": "January", "styling": january_rates["styling_rate__avg"]},
            {"month": "February", "styling": february_rates["styling_rate__avg"]},
            {"month": "March", "styling": march_rates["styling_rate__avg"]},
            {"month": "April", "styling": april_rates["styling_rate__avg"]},
            {"month": "May", "styling": may_rates["styling_rate__avg"]},
            {"month": "June", "styling": june_rates["styling_rate__avg"]},
            {"month": "July", "styling": july_rates["styling_rate__avg"]},
            {"month": "August", "styling": august_rates["styling_rate__avg"]},
            {"month": "September", "styling": september_rates["styling_rate__avg"]},
            {"month": "October", "styling": october_rates["styling_rate__avg"]},
            {"month": "November", "styling": november_rates["styling_rate__avg"]},
            {"month": "December", "styling": december_rates["styling_rate__avg"]},
        ]
        return Response(styling_rates)


class GetMCRateForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        january_rates = Rating.objects.filter(event_date__month="01").aggregate(
            Avg("mc_rate")
        )
        february_rates = Rating.objects.filter(event_date__month="02").aggregate(
            Avg("mc_rate")
        )
        march_rates = Rating.objects.filter(event_date__month="03").aggregate(
            Avg("mc_rate")
        )
        april_rates = Rating.objects.filter(event_date__month="04").aggregate(
            Avg("mc_rate")
        )
        may_rates = Rating.objects.filter(event_date__month="05").aggregate(
            Avg("mc_rate")
        )
        june_rates = Rating.objects.filter(event_date__month="06").aggregate(
            Avg("mc_rate")
        )
        july_rates = Rating.objects.filter(event_date__month="07").aggregate(
            Avg("mc_rate")
        )
        august_rates = Rating.objects.filter(event_date__month="08").aggregate(
            Avg("mc_rate")
        )
        september_rates = Rating.objects.filter(event_date__month="09").aggregate(
            Avg("mc_rate")
        )
        october_rates = Rating.objects.filter(event_date__month="10").aggregate(
            Avg("mc_rate")
        )
        november_rates = Rating.objects.filter(event_date__month="11").aggregate(
            Avg("mc_rate")
        )
        december_rates = Rating.objects.filter(event_date__month="12").aggregate(
            Avg("mc_rate")
        )
        mc_rates = [
            {"month": "January", "mc": january_rates["mc_rate__avg"]},
            {"month": "February", "mc": february_rates["mc_rate__avg"]},
            {"month": "March", "mc": march_rates["mc_rate__avg"]},
            {"month": "April", "mc": april_rates["mc_rate__avg"]},
            {"month": "May", "mc": may_rates["mc_rate__avg"]},
            {"month": "June", "mc": june_rates["mc_rate__avg"]},
            {"month": "July", "mc": july_rates["mc_rate__avg"]},
            {"month": "August", "mc": august_rates["mc_rate__avg"]},
            {"month": "September", "mc": september_rates["mc_rate__avg"]},
            {"month": "October", "mc": october_rates["mc_rate__avg"]},
            {"month": "November", "mc": november_rates["mc_rate__avg"]},
            {"month": "December", "mc": december_rates["mc_rate__avg"]},
        ]
        return Response(mc_rates)


class GetPresentationRateForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        january_rates = Rating.objects.filter(event_date__month="01").aggregate(
            Avg("presentation_rate")
        )
        february_rates = Rating.objects.filter(event_date__month="02").aggregate(
            Avg("presentation_rate")
        )
        march_rates = Rating.objects.filter(event_date__month="03").aggregate(
            Avg("presentation_rate")
        )
        april_rates = Rating.objects.filter(event_date__month="04").aggregate(
            Avg("presentation_rate")
        )
        may_rates = Rating.objects.filter(event_date__month="05").aggregate(
            Avg("presentation_rate")
        )
        june_rates = Rating.objects.filter(event_date__month="06").aggregate(
            Avg("presentation_rate")
        )
        july_rates = Rating.objects.filter(event_date__month="07").aggregate(
            Avg("presentation_rate")
        )
        august_rates = Rating.objects.filter(event_date__month="08").aggregate(
            Avg("presentation_rate")
        )
        september_rates = Rating.objects.filter(event_date__month="09").aggregate(
            Avg("presentation_rate")
        )
        october_rates = Rating.objects.filter(event_date__month="10").aggregate(
            Avg("presentation_rate")
        )
        november_rates = Rating.objects.filter(event_date__month="11").aggregate(
            Avg("presentation_rate")
        )
        december_rates = Rating.objects.filter(event_date__month="12").aggregate(
            Avg("presentation_rate")
        )
        presentation_rates = [
            {
                "month": "January",
                "presentation": january_rates["presentation_rate__avg"],
            },
            {
                "month": "February",
                "presentation": february_rates["presentation_rate__avg"],
            },
            {"month": "March", "presentation": march_rates["presentation_rate__avg"]},
            {"month": "April", "presentation": april_rates["presentation_rate__avg"]},
            {"month": "May", "presentation": may_rates["presentation_rate__avg"]},
            {"month": "June", "presentation": june_rates["presentation_rate__avg"]},
            {"month": "July", "presentation": july_rates["presentation_rate__avg"]},
            {"month": "August", "presentation": august_rates["presentation_rate__avg"]},
            {
                "month": "September",
                "presentation": september_rates["presentation_rate__avg"],
            },
            {
                "month": "October",
                "presentation": october_rates["presentation_rate__avg"],
            },
            {
                "month": "November",
                "presentation": november_rates["presentation_rate__avg"],
            },
            {
                "month": "December",
                "presentation": december_rates["presentation_rate__avg"],
            },
        ]
        return Response(presentation_rates)


class GetCoutesyRateForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        january_rates = Rating.objects.filter(event_date__month="01").aggregate(
            Avg("courtesy_rate")
        )
        february_rates = Rating.objects.filter(event_date__month="02").aggregate(
            Avg("courtesy_rate")
        )
        march_rates = Rating.objects.filter(event_date__month="03").aggregate(
            Avg("courtesy_rate")
        )
        april_rates = Rating.objects.filter(event_date__month="04").aggregate(
            Avg("courtesy_rate")
        )
        may_rates = Rating.objects.filter(event_date__month="05").aggregate(
            Avg("courtesy_rate")
        )
        june_rates = Rating.objects.filter(event_date__month="06").aggregate(
            Avg("courtesy_rate")
        )
        july_rates = Rating.objects.filter(event_date__month="07").aggregate(
            Avg("courtesy_rate")
        )
        august_rates = Rating.objects.filter(event_date__month="08").aggregate(
            Avg("courtesy_rate")
        )
        september_rates = Rating.objects.filter(event_date__month="09").aggregate(
            Avg("courtesy_rate")
        )
        october_rates = Rating.objects.filter(event_date__month="10").aggregate(
            Avg("courtesy_rate")
        )
        november_rates = Rating.objects.filter(event_date__month="11").aggregate(
            Avg("courtesy_rate")
        )
        december_rates = Rating.objects.filter(event_date__month="12").aggregate(
            Avg("courtesy_rate")
        )
        courtesy_rates = [
            {
                "month": "January",
                "courtesy": january_rates["courtesy_rate__avg"],
            },
            {
                "month": "February",
                "courtesy": february_rates["courtesy_rate__avg"],
            },
            {"month": "March", "courtesy": march_rates["courtesy_rate__avg"]},
            {"month": "April", "courtesy": april_rates["courtesy_rate__avg"]},
            {"month": "May", "courtesy": may_rates["courtesy_rate__avg"]},
            {"month": "June", "courtesy": june_rates["courtesy_rate__avg"]},
            {"month": "July", "courtesy": july_rates["courtesy_rate__avg"]},
            {"month": "August", "courtesy": august_rates["courtesy_rate__avg"]},
            {
                "month": "September",
                "courtesy": september_rates["courtesy_rate__avg"],
            },
            {
                "month": "October",
                "courtesy": october_rates["courtesy_rate__avg"],
            },
            {
                "month": "November",
                "courtesy": november_rates["courtesy_rate__avg"],
            },
            {
                "month": "December",
                "courtesy": december_rates["courtesy_rate__avg"],
            },
        ]
        return Response(courtesy_rates)


# GROUP ROOM VIEWS
class CreateGroupRoom(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupRoomSerializer
    queryset = GroupRoom.objects.all()


class GetGroupRoom(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupRoomSerializer
    queryset = GroupRoom.objects.all()
    lookup_field = "room_key"


class CreateClientGroupRoom(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientGroupRoomSerializer
    queryset = ClientGroupRoom.objects.all()


class CreatePartnerGroupRoom(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PartnerGroupRoomSerializer
    queryset = PartnerGroupRoom.objects.all()


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


class AllInterviewsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSerializer
    queryset = InterviewSchedule.objects.all()


class AllAffiliationsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationRequest.objects.all()


class AllRequestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationRequest.objects.all()

    def get_queryset(self):
        partner_id = self.kwargs["pk"]
        return AffiliationRequest.objects.filter(
            partner__id=partner_id, status="Pending"
        )


class AllAcceptedTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationRequest.objects.all()

    def get_queryset(self):
        partner_id = self.kwargs["pk"]
        return AffiliationRequest.objects.filter(
            partner__id=partner_id, status="Accepted"
        )


class AllEventTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationSerializer

    def get_queryset(self):
        event_id = self.kwargs["pk"]
        return AffiliationRequest.objects.filter(event__id=event_id, status="Accepted")


class AllTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationSerializer

    def get_queryset(self):
        return AffiliationRequest.objects.filter(status="Accepted")


class AllCompletedTaskView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationRequest.objects.all()

    def get_queryset(self):
        return AffiliationRequest.objects.filter(
            status="Accepted", task_status="Completed"
        )


class AllClientRoomsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientRoomSerializer
    queryset = ClientRoom.objects.all()


class AllPartnerRoomsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PartnerRoomSerializer
    queryset = PartnerRoom.objects.all()


class AllGroupRooms(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupRoomSerializer
    queryset = GroupRoom.objects.all()


class AllClientGroups(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientGroupRoomSerializer
    queryset = ClientGroupRoom.objects.all()


class AllPartnerGroups(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PartnerGroupRoomSerializer
    queryset = PartnerGroupRoom.objects.all()


def email_view(request):
    img_dir = "media"
    image = "Email Image.png"
    file_path = os.path.join(img_dir, image)
    with open(file_path, "rb") as img_file:
        my_img = MIMEImage(img_file.read())
        my_img.add_header("Content-ID", "<{name}>".format(name=image))
        my_img.add_header("Content-Disposition", "inline", filename=image)
    # with open("media/Email Image.png", "rb") as img_file:
    #     encoded_img = base64.b64encode(img_file.read())
    # decoded_img = encoded_img.decode("utf-8")
    # print("The fvcking decoded base64 is: ", decoded_img)
    return render(request, "api/email_template2.html", {"my_img": my_img})
