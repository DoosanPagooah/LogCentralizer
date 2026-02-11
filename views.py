from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random
from datetime import datetime, timedelta

@login_required
def dashboard_view(request):
    """Renders the FinOps dashboard page."""
    return render(request, 'finops/dashboard.html')

@login_required
def dashboard_data(request):
    """API endpoint to fetch dashboard data based on filters."""
    period = request.GET.get('period', 'week')
    
    if period == 'month':
        days = 30
        date_format = '%b %d'
    else:
        days = 7
        date_format = '%A'

    labels = []
    rr_costs = []
    nash_costs = []
    
    # Mock data generation
    # Round Robin: Standard distribution
    # Nash Equilibrium: Optimized distribution (lower cost, better stability)
    for i in range(days):
        date = datetime.now() - timedelta(days=days-1-i)
        labels.append(date.strftime(date_format))
        
        # Randomize mock data
        rr_val = random.uniform(100, 150)
        nash_val = rr_val * random.uniform(0.75, 0.90) # 10-25% savings
        
        rr_costs.append(round(rr_val, 2))
        nash_costs.append(round(nash_val, 2))

    data = {
        'labels': labels,
        'rr_costs': rr_costs,
        'nash_costs': nash_costs,
        'rr_total': round(sum(rr_costs), 2),
        'nash_total': round(sum(nash_costs), 2),
    }
    return JsonResponse(data)