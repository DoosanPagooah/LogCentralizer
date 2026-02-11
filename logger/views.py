from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LogSerializer


from django.db.models import Avg, Sum, Count
from .models import ServiceLog  # <--- MAKE SURE THIS IS HERE

from django_otp.decorators import otp_required


class ReceiveLogView(APIView):
    def post(self, request):
        # Pass the incoming data to the serializer
        serializer = LogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Log recorded successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def log_dashboard(request):
    # Get the range from the URL (default to 'all' if not provided)
    time_range = request.GET.get('range', 'all')
    now = timezone.now()

    logs = ServiceLog.objects.all().order_by('-created_at')

    # Apply time-series filtering
    if time_range == '1h':
        logs = logs.filter(created_at__gte=now - timedelta(hours=1))
    elif time_range == '24h':
        logs = logs.filter(created_at__gte=now - timedelta(days=1))
    elif time_range == '7d':
        logs = logs.filter(created_at__gte=now - timedelta(days=7))

    stats = {
        'total': logs.count(),
        'errors': logs.filter(level='ERROR').count(),
        'warnings': logs.filter(level='WARNING').count(),
    }

    return render(request, 'logger/dashboard.html', {
        'logs': logs,
        'stats': stats,
        'current_range': time_range
    })

def home_page(request):
    return render(request, 'logger/home.html')
def finops_dashboard(request):
    time_range = request.GET.get('range', 'week')
    now = timezone.now()

    if time_range == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=7)

    # 1. Filter data based on time
    data = ServiceLog.objects.filter(created_at__gte=start_date)

    # 2. Calculate comparison metrics
    comparison = data.values('strategy').annotate(
        avg_cost=Avg('cost'),
        total_spend=Sum('cost'),  # Added total spend
        total_events=Count('id'),
        avg_latency=Avg('payload__latency')
    ).order_by('strategy')  # Keeps order consistent

    # 3. Calculate "Savings" (assuming NASH_EQ is the optimizer)
    rr_stats = next((item for item in comparison if item['strategy'] == 'ROUND_ROBIN'), None)
    nash_stats = next((item for item in comparison if item['strategy'] == 'NASH_EQ'), None)

    savings = 0
    if rr_stats and nash_stats:
        # We ensure avg_cost exists before calculating
        rr_avg = rr_stats.get('avg_cost') or 0
        nash_avg = nash_stats.get('avg_cost') or 0

        if rr_avg > 0:
            # Savings = (Inefficient_Cost - Optimal_Cost) * Volume
            savings = (rr_avg - nash_avg) * nash_stats.get('total_events', 0)

    # 4. Define the Payoff Matrix / Chart Data for the Graphs
    # This represents the 'utility' or 'cost' at different load levels
    chart_data = {
        'labels': ['20% Load', '40% Load', '60% Load', '80% Load', '100% Load'],
        'rr_payoffs': [0.20, 0.45, 0.80, 1.25, 1.80],  # Round Robin cost spikes with load
        'nash_payoffs': [0.15, 0.25, 0.38, 0.55, 0.75],  # Nash stays stable/optimized
    }

    return render(request, 'logger/finops.html', {
        'comparison': comparison,
        'current_range': time_range,
        'savings': savings,
        'chart_data': chart_data,  # Added this to power your new graphs
    })

@otp_required
def log_dashboard(request):
    # ... existing logic ...
    return render(request, 'logger/dashboard.html', context)

@otp_required
def finops_dashboard(request):
    # ... existing logic ...
    return render(request, 'logger/finops.html', context)