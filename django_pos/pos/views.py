import json
from datetime import date
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField, F, Count,Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from products.models import Product, Category
from sales.models import Sale, SaleDetail

@login_required(login_url="/accounts/login/")
def index(request):
    today = date.today()
    year = today.year
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = today_start + timedelta(days=1)

    # Calculate daily profit for the past 24 hours
    daily_profit = Sale.objects.filter(
        date_added__gte=today_start,
        date_added__lt=today_end
    ).annotate(
        total_cost=Coalesce(Sum(F('saledetail__product__buying_price') * F('saledetail__quantity')), Value(0), output_field=FloatField())
    ).aggregate(
        daily_profit=Coalesce(
            Sum(F('amount_payed') - F('total_cost')),
            Value(0.0),
            output_field=FloatField()
        )
    )['daily_profit']

    # Calculate weekly profit
    weekly_profit = Sale.objects.filter(
        date_added__week=today.isocalendar()[1],
        date_added__year=year
    ).annotate(
        total_cost=Coalesce(Sum(F('saledetail__product__buying_price') * F('saledetail__quantity')), Value(0), output_field=FloatField())
    ).aggregate(
        weekly_profit=Coalesce(
            Sum(F('amount_payed') - F('total_cost')),
            Value(0.0),
            output_field=FloatField()
        )
    )['weekly_profit']

    # Calculate monthly profit
    monthly_profit = Sale.objects.filter(
        date_added__year=year,
        date_added__month=today.month
    ).annotate(
        total_cost=Coalesce(Sum(F('saledetail__product__buying_price') * F('saledetail__quantity')), Value(0), output_field=FloatField())
    ).aggregate(
        monthly_profit=Coalesce(
            Sum(F('amount_payed') - F('total_cost')),
            Value(0.0),
            output_field=FloatField()
        )
    )['monthly_profit']


    # Calculate daily, weekly, and monthly quantity of products sold
    daily_products_sold = Sale.objects.filter(date_added__date=today).aggregate(
        daily_products_sold=Coalesce(Sum('saledetail__quantity'), 0)).get('daily_products_sold')
    weekly_products_sold = Sale.objects.filter(date_added__week=today.isocalendar()[1], date_added__year=year).aggregate(
        weekly_products_sold=Coalesce(Sum('saledetail__quantity'), 0)).get('weekly_products_sold')
    monthly_products_sold = Sale.objects.filter(date_added__year=year, date_added__month=today.month).aggregate(
        monthly_products_sold=Coalesce(Sum('saledetail__quantity'), 0)).get('monthly_products_sold')

    # Calculate earnings per month
    monthly_earnings = []
    for month in range(1, 13):
        earning = Sale.objects.filter(date_added__year=year, date_added__month=month).aggregate(
            total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
        monthly_earnings.append(earning)

    # Calculate annual earnings
    annual_earnings = Sale.objects.filter(date_added__year=year).aggregate(
        total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
    annual_earnings = format(annual_earnings, '.2f')

    # AVG per month
    avg_month = format(sum(monthly_earnings) / 12, '.2f')

    # Top-selling products
    top_products = Product.objects.annotate(quantity_sum=Sum(
        'saledetail__quantity')).order_by('-quantity_sum')[:3]

    top_products_names = []
    top_products_quantity = []

    for p in top_products:
        top_products_names.append(p.name)
        top_products_quantity.append(p.quantity_sum)

    context = {
        "active_icon": "dashboard",
        "products": Product.objects.all().count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "avg_month": avg_month,
        "top_products_names": json.dumps(top_products_names),
        "top_products_names_list": top_products_names,
        "top_products_quantity": json.dumps(top_products_quantity),
        "daily_profit": daily_profit,
        "weekly_profit": weekly_profit,
        "monthly_profit": monthly_profit,
        "daily_products_sold": daily_products_sold,
        "weekly_products_sold": weekly_products_sold,
        "monthly_products_sold": monthly_products_sold,
    }
    return render(request, "pos/index.html", context)
