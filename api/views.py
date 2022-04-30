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
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder

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


class GetSalesPerMonth(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        monthly_sales = Event.objects.raw(
            """SELECT EXTRACT(MONTH FROM date_schedule) as extracted_month,
                SUM(package_cost) as monthly_sales FROM api_event
                GROUP BY extracted_month ORDER BY extracted_month ASC"""
        )
        data = serializers.serialize("json", monthly_sales)
        print(data)
        return Response(data)


# PASS URL PARAM
# TO SOLVE SIR MARK REQUEST
class GetMonthlySales(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
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


# PASS YEAR URL PARAM
# TO SOLVE SIR MARK REQUEST
class GetTotalSales(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_sales = Event.objects.filter(
            date_schedule__range=[date(date.today().year, 1, 1), date.today()]
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
        )
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
class CreateRatingView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        rating_data = {
            "event_name": event.event_name,
            "event_date": event.date_schedule,
            "venue_rate": request.data.get("venue_rate"),
            "catering_rate": request.data.get("catering_rate"),
            "styling_rate": request.data.get("styling_rate"),
            "mc_rate": request.data.get("mc_rate"),
            "presentation_rate": request.data.get("presentation_rate"),
            "courtesy_rate": request.data.get("courtesy_rate"),
        }
        serializer = RatingSerializer(data=rating_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        member = RoomMember.objects.filter(
            member=self.request.user.username
        ).values_list("room")
        member_rooms = ChatRoom.objects.filter(pk__in=member)
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
                "event__event_name",
                "event__date_schedule",
                "event__package_cost",
                "payment",
                "status",
            )
            .order_by("event__date_schedule")
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

        transactions_list = (
            TransactionLog.objects.filter(date_schedule__year=year)
            .values(
                "id",
                "event__event_name",
                "event__date_schedule",
                "event__package_cost",
                "payment",
                "status",
            )
            .order_by("event__date_schedule")
        )

        json_transactions_list = json.dumps(
            list(transactions_list), cls=DjangoJSONEncoder
        )

        return Response(json_transactions_list)


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
    queryset = ChatRoom.objects.all().order_by("pk")


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
