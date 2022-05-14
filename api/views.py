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
    ChatRoomSerializer,
    ChatMessagesSerializer,
    RoomMemberSerializer,
    UsernameSerializer,
    ClientEmailMobileSerializer,
    PartnerEmailMobileSerializer,
    TransactionSerializer,
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
    ChatRoom,
    Chat,
    RoomMember,
    TransactionLog,
)
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg, Sum, Count
from django.db.models.functions import TruncMonth
from datetime import date
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render
from email.mime.image import MIMEImage
import os
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

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


class GetAccountUsernameView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UsernameSerializer
    queryset = Account.objects.all()
    lookup_field = "username"


class GetClientViaEmail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ClientEmailMobileSerializer
    queryset = Client.objects.all()
    lookup_field = "email"


class GetClientViaMobile(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ClientEmailMobileSerializer
    queryset = Client.objects.all()
    lookup_field = "mobile_number"


class GetPartnerViaEmail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PartnerEmailMobileSerializer
    queryset = BusinessPartner.objects.all()
    lookup_field = "email"


class GetPartnerViaMobile(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PartnerEmailMobileSerializer
    queryset = BusinessPartner.objects.all()
    lookup_field = "mobile_number"


class UpdateAccountView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            "client_name": client.first_name,
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


class UpdateInterviewSchedule(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSerializer
    queryset = InterviewSchedule.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)

        interview = InterviewSchedule.objects.get(pk=self.kwargs["pk"])
        client_id = interview.client.id
        client = Client.objects.get(pk=client_id)

        with open("media/Email Image.png", "rb") as img_file:
            my_img = MIMEImage(img_file.read())
            my_img.add_header("Content-ID", "<{name}>".format(name="email_img"))
            my_img.add_header("Content-Disposition", "inline", filename="email_img")
        context = {
            "my_img": my_img,
            "client_name": client.first_name,
            "date_schedule": request.data["date"],
            "time_schedule": request.data["time"],
            "location": request.data["location"],
        }

        subject = "Alas Creative Events Interview"
        template = render_to_string("api/update_email_template.html", context)

        email_from = settings.EMAIL_HOST_USER
        recipient = ["schieniezel@gmail.com"]

        my_email = EmailMultiAlternatives(subject, template, email_from, recipient)
        my_email.mixed_subtype = "related"
        my_email.attach_alternative(template, "text/html")
        my_email.attach(my_img)

        my_email.send(fail_silently=False)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class DashboardEvents(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.filter(
        date_schedule__range=[date.today(), date(date.today().year, 12, 31)]
    )[:5]


class DashboardEventsSummary(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        events_summary = (
            Event.objects.filter(
                date_schedule__range=[
                    date(date.today().year, 1, 31),
                    date(date.today().year, 12, 31),
                ]
            )
            .annotate(month=TruncMonth("date_schedule"))
            .values("month")
            .annotate(total=Count("pk"))
            .order_by("month")
        )
        json_events_summary = json.dumps(list(events_summary), cls=DjangoJSONEncoder)
        return Response(json_events_summary)


class PartnerDashboardEvents(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        partner = BusinessPartner.objects.get(account__id=request.user.id)
        partner_accepted_tasks = AffiliationRequest.objects.filter(
            partner=partner, status="Accepted"
        ).values_list("event")
        partner_events = Event.objects.filter(
            pk__in=partner_accepted_tasks,
            date_schedule__range=[date.today(), date(date.today().year, 12, 31)],
        )[:5]
        serializer = EventSerializer(partner_events, many=True)
        return Response(serializer.data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DashboardMonthlyEvents(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = EventSerializer
#     queryset = Event.objects.annotate(monthly_events=Count())


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


class ClientPayments(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.filter(
        date_schedule__range=[date.today(), date(date.today().year, 12, 30)]
    )


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


class GetIncuredEvents(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.filter(
        date_schedule__range=[date(date.today().year, 1, 1), date.today()]
    )


# PASS URL PARAM
# TO SOLVE SIR MARK REQUEST
class GetSalesYears(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sales_years = (
            TransactionLog.objects.filter(
                event__date_schedule__year__lte=date.today().year
            )
            .order_by("-event__date_schedule__year")
            .distinct("event__date_schedule__year")
            .values(transaction_year=F("event__date_schedule__year"))
        )

        json_sales_years = json.dumps(list(sales_years))

        return Response(json_sales_years)


# PASS URL PARAM
# TO SOLVE SIR MARK REQUEST
class GetMonthlySales(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_year):
        if int(transaction_year) == date.today().year:
            monthly_sales = (
                Event.objects.filter(
                    date_schedule__range=[
                        date(date.today().year, 1, 1),
                        date.today(),
                    ],
                )
                .annotate(month=TruncMonth("date_schedule"))
                .values("month")
                .annotate(total=Sum("package_cost"))
                .order_by("month")
            )
            json_monthly_sales = json.dumps(list(monthly_sales), cls=DjangoJSONEncoder)
            return Response(json_monthly_sales)
        else:
            monthly_sales = (
                Event.objects.filter(
                    date_schedule__range=[
                        date(int(transaction_year), 1, 1),
                        date(int(transaction_year), 12, 31),
                    ],
                )
                .annotate(month=TruncMonth("date_schedule"))
                .values("month")
                .annotate(total=Sum("package_cost"))
                .order_by("month")
            )
            json_monthly_sales = json.dumps(list(monthly_sales), cls=DjangoJSONEncoder)
            return Response(json_monthly_sales)


# PASS YEAR URL PARAM
# TO SOLVE SIR MARK REQUEST
class GetTotalSales(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_year):
        if int(transaction_year) == date.today().year:
            total_sales = Event.objects.filter(
                date_schedule__range=[date(date.today().year, 1, 1), date.today()]
            ).aggregate(total_sales=Sum("package_cost"))
            return Response(total_sales)
        else:
            total_sales = Event.objects.filter(
                date_schedule__range=[
                    date(int(transaction_year), 1, 1),
                    date(int(transaction_year), 12, 31),
                ]
            ).aggregate(total_sales=Sum("package_cost"))
            return Response(total_sales)


# class VenueSatisfactionForecast(views.APIView):
#     # INCLUDE ONLY THE COLUMNS THAT WE ARE INTERESTED IN
#     ratings = Rating.objects.exclude('event_name', 'catering_rate', 'styling_rate', 'mc_rate', 'presentation_rate', 'courtesy_rate')
#     # CONVERT THE QUERYSET INTO PANDAS DATAFRAME
#     ratings_df = pd.DataFrame(ratings)
#     # GROUP THE COLUMNS AND SUM THEM
#     ratings_df = ratings_df.groupby(['event_date', 'venue_rate'], as_index=False).sum()
#     # RENAME THE COLUMNS FOR X & Y TO ENABLE PROPHET TO RECOGNIZE THEM
#     ratings_df = ratings_df.rename(columns={'event_date' : 'ds', 'venue_rate' : 'y'})
#     # SINCE WE HAVE 2 YEARS WORTH DATA, MAKE A TRAINING & TESTING MODELS FOR EACH YEAR
#     training_model = ratings_df = [ratings_df['ds']<'2021-01-01']
#     testing_model = ratings_df = [ratings_df['ds']>='2021-01-01']
#     # INSTANTIATE PROPHET
#     m = Prophet()
#     # FIT THE TRAINING MODEL
#     m.fit(training_model)
#     # MAKE A FUTURISTIC DATAFRAME FOR THE NEXT 365 DAYS
#     future_ratings = m.make_future_dataframe(periods=365, freq='d')
#     # FINAL STEP IS TO PREDICT
#     venue_forecast = m.predict(future_ratings)

# AFFILIATION VIEWS
class CreateAffiliationView(views.APIView):
    permission_classes = [IsAuthenticated]
    global hasError

    def post(self, request):
        hasError = False
        partners = request.data.get("partners")
        for p in partners:
            serializer = AffiliationSerializer(
                data={"event": request.data.get("event"), "partner": p["value"]},
                partial=True,
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                hasError = True

        if hasError:
            return Response({"error": "400"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": "200"}, status=status.HTTP_200_OK)

        # serializer = RatingSerializer(data=rating_data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAffiliationView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationRequest.objects.all()


# class GetAllAffiliations(views.APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):

#         # GET THE ID OF THE OF THE EVENTS & USE IT FOR FILTERING
#         event_ids = Event.objects.filter(
#             date_schedule__range=[date.today(), date(date.today().year, 12, 31)]
#         ).values_list("id")
#         affiliations_list = AffiliationRequest.objects.filter(
#             event__in=event_ids
#         ).values(
#             "event__event_name", "partner__first_name", "partner__last_name", "status"
#         )

#         json_affiliations_list = json.dumps(
#             list(affiliations_list), cls=DjangoJSONEncoder
#         )

#         return Response(json_affiliations_list)


class DashboardAffiliations(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        # GET THE ID OF THE OF THE EVENTS & USE IT FOR FILTERING
        event_ids = Event.objects.filter(
            date_schedule__range=[date.today(), date(date.today().year, 12, 31)]
        ).values_list("id")
        affiliations_list = AffiliationRequest.objects.filter(
            event__in=event_ids
        ).values("partner__first_name", "partner__last_name", "status")[:5]

        json_affiliations_list = json.dumps(
            list(affiliations_list), cls=DjangoJSONEncoder
        )

        return Response(json_affiliations_list)


class PartnerDashboardAffiliations(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        partner = BusinessPartner.objects.get(account__id=request.user.id)
        partner_requests = AffiliationRequest.objects.filter(
            partner=partner,
            created_at__range=[date.today(), date(date.today().year, 12, 31)],
        )[:5]
        serializer = AffiliationSerializer(partner_requests, many=True)
        return Response(serializer.data)


class PartnerRequestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer

    def get_queryset(self):
        partner = BusinessPartner.objects.get(account__id=self.request.user.id)
        partner_requests = AffiliationRequest.objects.filter(
            partner=partner,
            created_at__range=[date.today(), date(date.today().year, 12, 31)],
            status="Pending",
        )
        return partner_requests


class PartnerTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer

    def get_queryset(self):
        partner = BusinessPartner.objects.get(account__id=self.request.user.id)
        partner_tasks = AffiliationRequest.objects.filter(
            partner=partner,
            created_at__range=[date.today(), date(date.today().year, 12, 31)],
            status="Accepted",
        )
        return partner_tasks


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


class DestroyRequestView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AffiliationSerializer
    queryset = AffiliationRequest.objects.all()


# RATING VIEWS
class CreateRatingView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CreateRatingView(views.APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, event_id):
#         event = Event.objects.get(pk=event_id)
#         rating_data = {
#             "event_name": event.event_name,
#             "event_date": event.date_schedule,
#             "venue_rate": request.data.get("venue_rate"),
#             "catering_rate": request.data.get("catering_rate"),
#             "styling_rate": request.data.get("styling_rate"),
#             "mc_rate": request.data.get("mc_rate"),
#             "presentation_rate": request.data.get("presentation_rate"),
#             "courtesy_rate": request.data.get("courtesy_rate"),
#         }
#         serializer = RatingSerializer(data=rating_data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# training_query = Rating.objects.filter(event_date__range=[date(2020, 1, 1), date(2020, 12, 31)]).values('event_date', 'venue_rate').order_by('event_date')
# training_df =  pd.DataFrame(training_query)
# training_df.index = pd.to_datetime(training_df['event_date'])
# del training_df['event_date']

# testing_query = Rating.objects.filter(event_date__range=[date(2021, 1, 1), date(2021, 12, 31)]).values('event_date', 'venue_rate').order_by('event_date')
# testing_df =  pd.DataFrame(testing_query)
# testing_df.index = pd.to_datetime(testing_df['event_date'])
# del testing_df['event_date']

# y = training_df['venue_rate']

# ARIMAmodel = ARIMA(y, order=(2,1,2))
# ARIMAmodel = ARIMAmodel.fit()
# y_pred = ARIMAmodel.get_forecast(len(testing_df.index))
# y_pred_df = y_pred.conf_int(alpha=0.05)
# y_pred_df["Predictions"] = ARIMAmodel.predict(start=y_pred_df.index[0], end=y_pred_df.index[-1])
# y_pred_df.index = testing_df.index
# y_pred_out = y_pred_df["Predictions"]

# dummy_dates = pd.date_range(end = datetime.today(), periods = 100)
# dummy_dates = pd.date_range(start="2022-01-01",end="2022-12-31").date
# dummy_dates = pd.date_range(start="2022-1-1", periods=203).date
# dummy_df = pd.DataFrame(dummy_dates)
# dummy_df["event_date"] = dummy_dates
# del dummy_df[0]
# dummy_df["forecast_venue_rate"] = y_pred_out
# json_df = dummy_df.to_dict("records")


class GetVenueForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        training_query = (
            Rating.objects.filter(
                event_date__range=[
                    date(date.today().year - 2, 1, 1),
                    date(date.today().year - 2, 12, 31),
                ]
            )
            .values("event_date", "venue_rate")
            .order_by("event_date")
        )
        training_df = pd.DataFrame(training_query)
        training_df.index = pd.to_datetime(training_df["event_date"])
        del training_df["event_date"]

        testing_query = (
            Rating.objects.filter(
                event_date__range=[
                    date(date.today().year - 1, 1, 1),
                    date(date.today().year - 1, 12, 31),
                ]
            )
            .values("event_date", "venue_rate")
            .order_by("event_date")
        )
        testing_df = pd.DataFrame(testing_query)
        testing_df.index = pd.to_datetime(testing_df["event_date"])
        del testing_df["event_date"]

        y = training_df["venue_rate"]

        ARIMAmodel = ARIMA(y, order=(2, 2, 2))
        ARIMAmodel = ARIMAmodel.fit()
        y_pred = ARIMAmodel.get_forecast(len(testing_df.index))
        y_pred_df = y_pred.conf_int(alpha=0.05)
        y_pred_df["Predictions"] = ARIMAmodel.predict(
            start=y_pred_df.index[0], end=y_pred_df.index[-1]
        )
        y_pred_df.index = testing_df.index
        y_pred_out = y_pred_df["Predictions"]

        forecast_dates = pd.date_range(
            start=f"{date.today().year}-01-01", periods=365
        ).date
        y_pred_out.index = forecast_dates
        forecast_df = pd.DataFrame(forecast_dates)
        forecast_df["event_date"] = forecast_dates
        del forecast_df[0]
        forecast_df.index = forecast_dates
        forecast_df["forecast_venue_rate"] = y_pred_out
        json_df = json.dumps(forecast_df.to_dict("records"), cls=DjangoJSONEncoder)

        return Response(json_df)


class GetCateringForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        training_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 2, 1, 1), date(date.today().year - 2, 12, 31)]
            )
            .values("event_date", "catering_rate")
            .order_by("event_date")
        )
        training_df = pd.DataFrame(training_query)
        training_df.index = pd.to_datetime(training_df["event_date"])
        del training_df["event_date"]

        testing_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 1, 1, 1), date(date.today().year - 1, 12, 31)]
            )
            .values("event_date", "catering_rate")
            .order_by("event_date")
        )
        testing_df = pd.DataFrame(testing_query)
        testing_df.index = pd.to_datetime(testing_df["event_date"])
        del testing_df["event_date"]

        y = training_df["catering_rate"]

        ARIMAmodel = ARIMA(y, order=(2, 2, 2))
        ARIMAmodel = ARIMAmodel.fit()
        y_pred = ARIMAmodel.get_forecast(len(testing_df.index))
        y_pred_df = y_pred.conf_int(alpha=0.05)
        y_pred_df["Predictions"] = ARIMAmodel.predict(
            start=y_pred_df.index[0], end=y_pred_df.index[-1]
        )
        y_pred_df.index = testing_df.index
        y_pred_out = y_pred_df["Predictions"]

        forecast_dates = pd.date_range(start=f'{date.today().year}-01-01', periods=365).date
        y_pred_out.index = forecast_dates
        forecast_df = pd.DataFrame(forecast_dates)
        forecast_df["event_date"] = forecast_dates
        del forecast_df[0]
        forecast_df.index = forecast_dates
        forecast_df["forecast_catering_rate"] = y_pred_out
        json_df = json.dumps(forecast_df.to_dict("records"), cls=DjangoJSONEncoder)

        return Response(json_df)


class GetStylingForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        training_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 2, 1, 1), date(date.today().year - 2, 12, 31)]
            )
            .values("event_date", "styling_rate")
            .order_by("event_date")
        )
        training_df = pd.DataFrame(training_query)
        training_df.index = pd.to_datetime(training_df["event_date"])
        del training_df["event_date"]

        testing_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 1, 1, 1), date(date.today().year - 1, 12, 31)]
            )
            .values("event_date", "styling_rate")
            .order_by("event_date")
        )
        testing_df = pd.DataFrame(testing_query)
        testing_df.index = pd.to_datetime(testing_df["event_date"])
        del testing_df["event_date"]

        y = training_df["styling_rate"]

        ARIMAmodel = ARIMA(y, order=(2, 2, 2))
        ARIMAmodel = ARIMAmodel.fit()
        y_pred = ARIMAmodel.get_forecast(len(testing_df.index))
        y_pred_df = y_pred.conf_int(alpha=0.05)
        y_pred_df["Predictions"] = ARIMAmodel.predict(
            start=y_pred_df.index[0], end=y_pred_df.index[-1]
        )
        y_pred_df.index = testing_df.index
        y_pred_out = y_pred_df["Predictions"]

        forecast_dates = pd.date_range(start=f"{date.today().year}-01-01", periods=365).date
        y_pred_out.index = forecast_dates
        forecast_df = pd.DataFrame(forecast_dates)
        forecast_df["event_date"] = forecast_dates
        del forecast_df[0]
        forecast_df.index = forecast_dates
        forecast_df["forecast_styling_rate"] = y_pred_out
        json_df = json.dumps(forecast_df.to_dict("records"), cls=DjangoJSONEncoder)

        return Response(json_df)


class GetMCForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        training_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 2, 1, 1), date(date.today().year - 2, 12, 31)]
            )
            .values("event_date", "mc_rate")
            .order_by("event_date")
        )
        training_df = pd.DataFrame(training_query)
        training_df.index = pd.to_datetime(training_df["event_date"])
        del training_df["event_date"]

        testing_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 1, 1, 1), date(date.today().year - 1, 12, 31)]
            )
            .values("event_date", "mc_rate")
            .order_by("event_date")
        )
        testing_df = pd.DataFrame(testing_query)
        testing_df.index = pd.to_datetime(testing_df["event_date"])
        del testing_df["event_date"]

        y = training_df["mc_rate"]

        ARIMAmodel = ARIMA(y, order=(2, 2, 2))
        ARIMAmodel = ARIMAmodel.fit()
        y_pred = ARIMAmodel.get_forecast(len(testing_df.index))
        y_pred_df = y_pred.conf_int(alpha=0.05)
        y_pred_df["Predictions"] = ARIMAmodel.predict(
            start=y_pred_df.index[0], end=y_pred_df.index[-1]
        )
        y_pred_df.index = testing_df.index
        y_pred_out = y_pred_df["Predictions"]

        forecast_dates = pd.date_range(start=f"{date.today().year}-01-01", periods=365).date
        y_pred_out.index = forecast_dates
        forecast_df = pd.DataFrame(forecast_dates)
        forecast_df["event_date"] = forecast_dates
        del forecast_df[0]
        forecast_df.index = forecast_dates
        forecast_df["forecast_mc_rate"] = y_pred_out
        json_df = json.dumps(forecast_df.to_dict("records"), cls=DjangoJSONEncoder)

        return Response(json_df)


class GetPresentationForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        training_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 2, 1, 1), date(date.today().year - 2, 12, 31)]
            )
            .values("event_date", "presentation_rate")
            .order_by("event_date")
        )
        training_df = pd.DataFrame(training_query)
        training_df.index = pd.to_datetime(training_df["event_date"])
        del training_df["event_date"]

        testing_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 1, 1, 1), date(date.today().year - 1, 12, 31)]
            )
            .values("event_date", "presentation_rate")
            .order_by("event_date")
        )
        testing_df = pd.DataFrame(testing_query)
        testing_df.index = pd.to_datetime(testing_df["event_date"])
        del testing_df["event_date"]

        y = training_df["presentation_rate"]

        ARIMAmodel = ARIMA(y, order=(2, 2, 2))
        ARIMAmodel = ARIMAmodel.fit()
        y_pred = ARIMAmodel.get_forecast(len(testing_df.index))
        y_pred_df = y_pred.conf_int(alpha=0.05)
        y_pred_df["Predictions"] = ARIMAmodel.predict(
            start=y_pred_df.index[0], end=y_pred_df.index[-1]
        )
        y_pred_df.index = testing_df.index
        y_pred_out = y_pred_df["Predictions"]

        forecast_dates = pd.date_range(start=f"{date.today().year}-01-01", periods=365).date
        y_pred_out.index = forecast_dates
        forecast_df = pd.DataFrame(forecast_dates)
        forecast_df["event_date"] = forecast_dates
        del forecast_df[0]
        forecast_df.index = forecast_dates
        forecast_df["forecast_presentation_rate"] = y_pred_out
        json_df = json.dumps(forecast_df.to_dict("records"), cls=DjangoJSONEncoder)

        return Response(json_df)


class GetCourtesyForecast(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        training_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 2, 1, 1), date(date.today().year - 2, 12, 31)]
            )
            .values("event_date", "courtesy_rate")
            .order_by("event_date")
        )
        training_df = pd.DataFrame(training_query)
        training_df.index = pd.to_datetime(training_df["event_date"])
        del training_df["event_date"]

        testing_query = (
            Rating.objects.filter(
                event_date__range=[date(date.today().year - 1, 1, 1), date(date.today().year - 1, 12, 31)]
            )
            .values("event_date", "courtesy_rate")
            .order_by("event_date")
        )
        testing_df = pd.DataFrame(testing_query)
        testing_df.index = pd.to_datetime(testing_df["event_date"])
        del testing_df["event_date"]

        y = training_df["courtesy_rate"]

        ARIMAmodel = ARIMA(y, order=(2, 2, 2))
        ARIMAmodel = ARIMAmodel.fit()
        y_pred = ARIMAmodel.get_forecast(len(testing_df.index))
        y_pred_df = y_pred.conf_int(alpha=0.05)
        y_pred_df["Predictions"] = ARIMAmodel.predict(
            start=y_pred_df.index[0], end=y_pred_df.index[-1]
        )
        y_pred_df.index = testing_df.index
        y_pred_out = y_pred_df["Predictions"]

        forecast_dates = pd.date_range(start=f"{date.today().year}-01-01", periods=365).date
        y_pred_out.index = forecast_dates
        forecast_df = pd.DataFrame(forecast_dates)
        forecast_df["event_date"] = forecast_dates
        del forecast_df[0]
        forecast_df.index = forecast_dates
        forecast_df["forecast_courtesy_rate"] = y_pred_out
        json_df = json.dumps(forecast_df.to_dict("records"), cls=DjangoJSONEncoder)

        return Response(json_df)


# CHAT ROOM VIEWS
class CreateChatRoom(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetChatRoom(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer
    lookup_field = "room_key"

    def get_queryset(self):
        room = ChatRoom.objects.filter(room_key=self.kwargs["room_key"])
        return room


class JoinChatRoom(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomMemberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMemberRooms(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        print(self.request.user.username)
        member = RoomMember.objects.filter(
            member=self.request.user.username
        ).values_list("room")
        member_rooms = ChatRoom.objects.filter(pk__in=member)
        print(member_rooms)
        return member_rooms


class DestroyChatRoom(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer
    lookup_field = "room_key"

    def destroy(self, request, *args, **kwargs):
        room = ChatRoom.objects.get(room_key=self.kwargs["room_key"])
        self.perform_destroy(room)
        return Response(
            {"message": "ChatRoom Deleted Successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


class PresentTransactions(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        # GET THE ID OF THE OF THE EVENTS & USE IT FOR FILTERING
        event_ids = Event.objects.filter(
            date_schedule__range=[date.today(), date(date.today().year, 12, 31)]
        ).values_list("id")
        transactions_list = (
            TransactionLog.objects.filter(event__in=event_ids)
            .values(
                "id",
                event_name=F("event__event_name"),
                date_schedule=F("event__date_schedule"),
                package_cost=F("event__package_cost"),
                client_payment=F("total_payment"),
                payment_status=F("status"),
                last_update=F("created_at"),
            )
            .order_by("created_at")
        )

        json_transactions_list = json.dumps(
            list(transactions_list), cls=DjangoJSONEncoder
        )

        return Response(json_transactions_list)


# PASS YEAR URL PARAM
# TO SOLVE SIR MARK REQUEST
class PastTransactions(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):

        if int(year) == date.today().year:
            transactions_list = (
                TransactionLog.objects.filter(
                    event__date_schedule__range=[
                        date(date.today().year, 1, 1),
                        date.today(),
                    ]
                )
                .values(
                    "id",
                    event_name=F("event__event_name"),
                    event_schedule=F("event__date_schedule"),
                    package_cost=F("event__package_cost"),
                    client_payment=F("total_payment"),
                    payment_status=F("status"),
                    last_update=F("created_at"),
                )
                .order_by("event_schedule")
            )

            json_transactions_list = json.dumps(
                list(transactions_list), cls=DjangoJSONEncoder
            )

            return Response(json_transactions_list)
        else:
            transactions_list = (
                TransactionLog.objects.filter(
                    event__date_schedule__range=[
                        date(int(year), 1, 1),
                        date(int(year), 12, 31),
                    ]
                )
                .values(
                    "id",
                    event_name=F("event__event_name"),
                    event_schedule=F("event__date_schedule"),
                    package_cost=F("event__package_cost"),
                    client_payment=F("total_payment"),
                    payment_status=F("status"),
                    last_update=F("created_at"),
                )
                .order_by("event_schedule")
            )

            json_transactions_list = json.dumps(
                list(transactions_list), cls=DjangoJSONEncoder
            )

            return Response(json_transactions_list)


class CreateTransaction(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    queryset = EventBookings.objects.filter(
        desired_date__range=[date.today(), date(date.today().year, 12, 31)]
    )


class AllEventsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.filter(
        date_schedule__range=[date.today(), date(date.today().year, 12, 31)]
    )


class AllInterviewsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSerializer
    queryset = InterviewSchedule.objects.filter(
        date__range=[date.today(), date(date.today().year, 12, 31)]
    )


class AllAffiliationsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        # GET THE ID OF THE OF THE EVENTS & USE IT FOR FILTERING
        event_ids = Event.objects.filter(
            date_schedule__range=[date.today(), date(date.today().year, 12, 31)]
        ).values_list("id")
        affiliations_list = AffiliationRequest.objects.filter(
            event__in=event_ids
        ).values(
            "id",
            "event__event_name",
            "partner__first_name",
            "partner__last_name",
            "status",
        )

        json_affiliations_list = json.dumps(
            list(affiliations_list), cls=DjangoJSONEncoder
        )

        return Response(json_affiliations_list)


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


class AllChatRooms(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all().order_by("-pk")


class AllRoomChatMessages(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessagesSerializer
    queryset = Chat.objects.all()

    def get_queryset(self):
        room_id = self.kwargs["pk"]
        return Chat.objects.filter(room__id=room_id)


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
