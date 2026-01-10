from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        customer = self.get_object()
        orders = customer.orders.all()
        return Response({
            'customer': CustomerSerializer(customer).data,
            'orders_count': orders.count(),
            'total_spent': sum(order.final_amount for order in orders)
        })
    
    @action(detail=False, methods=['get'])
    def loyalty_members(self, request):
        members = Customer.objects.filter(customer_type='loyalty')
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data)