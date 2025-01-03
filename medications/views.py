from rest_framework import generics
from medications.models import Medication, MedicationLog
from medications.serializers import MedicationSerializer, MedicationLogSerializer


class MedicationListCreateView(generics.ListCreateAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer


class MedicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer


class MedicationLogListCreateView(generics.ListCreateAPIView):
    queryset = MedicationLog.objects.all()
    serializer_class = MedicationLogSerializer


class MedicationLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicationLog.objects.all()
    serializer_class = MedicationLogSerializer
