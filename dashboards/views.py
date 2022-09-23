from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dashboard
from .serializers import DashboardSerializer
from suppliers.models import Supplier

import ipdb


class RegisterDashboardView(APIView):
    def post(self, request):
        serializer = DashboardSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        find_dashboard_url = Dashboard.objects.filter(url=serializer.validated_data['url']).exists()
        if find_dashboard_url is True:
            return Response({"message": "Dashboard já registrada!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # dashboard = Dashboard.objects.create(**serializer.validated_data)

        user = Supplier.objects.filter(cnpj = serializer.validated_data['supplier_owner'])
        if user.exists() is False:
            return Response({"message": "Fornecedor não encontrado! Verificar dados."}, status=status.HTTP_404_NOT_FOUND)

        new_dashboard = user[0].dashboards.create(**serializer.validated_data)
        user[0].save()
        # ipdb.set_trace()

        serializer = DashboardSerializer(new_dashboard)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        all_dashboards = Dashboard.objects.all()
        serializer = DashboardSerializer(all_dashboards, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DashboardByIdView(APIView):
    def get(self, request, dashboard_id=''):
        print(dashboard_id)
        # if type(dashboard_id) is int:
        try:
            dashboard = Dashboard.objects.get(id=dashboard_id)
            serialized = DashboardSerializer(dashboard)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except Dashboard.DoesNotExist:
            return Response({"message": "Dashboard não registrado!"}, status=status.HTTP_404_NOT_FOUND)

    # def patch(self, request, dashboard_id=''):

    def delete(self, request, dashboard_id=''):
        try:
            dashboard = Dashboard.objects.get(id=dashboard_id)
            # ipdb.set_trace()

            dashboard.delete()
            # Dashboard.remove()??

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Dashboard.DoesNotExist:
            return Response({"message": "Dashboard não registrado!"}, status=status.HTTP_404_NOT_FOUND)


class DashboardByCategoryView(APIView):
    def get(self, request, dashboard_category=''):
        try:
            adjusted_query = dashboard_category.strip().lower()
            print(adjusted_query)
            dashboard = Dashboard.objects.get(category=adjusted_query)
            serialized = DashboardSerializer(dashboard)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except Dashboard.DoesNotExist:
            return Response({"message": "Dashboard não registrado!"}, status=status.HTTP_404_NOT_FOUND)

