import csv
from django.db.models import Sum, Avg, Max
from django.db.models.functions import TruncMonth, TruncYear
from django import forms
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponse
from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import ExpenseForm, BudgetForm
from .models import Category, Expense, MonthlyBudget

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})



@login_required
def dashboard(request):
    today = timezone.localdate()

    # Get current month's expenses
    expenses = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    )

    # Calculate total spending
    total = expenses.aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    # Get this month's budget
    month_start = today.replace(day=1)

    budget = MonthlyBudget.objects.filter(
        user=request.user,
        month=month_start
    ).first()

    budget_amount = (
        budget.amount if budget
        else Decimal("0.00")
    )

    # Calculate remaining balance
    remaining = budget_amount - total
    if budget_amount > 0:
     usage_percentage = float((total / budget_amount) * 100)
    else:
     usage_percentage = 0

    if usage_percentage >= 100:
     budget_alert = "You have exceeded your monthly budget!"
    elif usage_percentage >= 80:
     budget_alert = "Warning! You have used 80% or more of your budget."
    else:
     budget_alert = ""

    # Calculate budget usage percentage
    if budget_amount > 0:
        percentage = float(
            (total / budget_amount) * 100
        )
        percentage = min(percentage, 100)
    else:
        percentage = 0

    # Count monthly transactions
    transaction_count = expenses.count()

    # Category-wise spending
    category_totals = (
        expenses
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
        
    )
    chart_labels = [
    item["category__name"] or "Uncategorized"
    for item in category_totals
    ]

    chart_values = [
    float(item["total"])
    for item in category_totals
    ]
    monthly_totals = (
    Expense.objects.filter(user=request.user)
    .annotate(month=TruncMonth("date"))
    .values("month")
    .annotate(total=Sum("amount"))
    .order_by("month")
     )

    monthly_labels = [
    item["month"].strftime("%b %Y")
    for item in monthly_totals
    ]

    monthly_values = [
    float(item["total"])
    for item in monthly_totals
    ]

    # Get recent transactions
    recent = Expense.objects.filter(
        user=request.user
    ).select_related("category")[:5]

    context = {
        "total": total,
        "budget": budget,
        "budget_amount": budget_amount,
        "remaining": remaining,
        "percentage": percentage,
        "transaction_count": transaction_count,
        "recent": recent,
        "category_totals": category_totals,
        "month_name": today.strftime("%B %Y"),
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "monthly_labels": monthly_labels,
        "monthly_values": monthly_values,
        "budget_alert": budget_alert,
    }

    return render(
        request,
        "tracker/dashboard.html",
        context
    )



@login_required
def expense_list(request):
    items = Expense.objects.filter(
        user=request.user
    ).select_related("category").order_by("-date")

    # Search by title
    search = request.GET.get("search", "")
    if search:
        items = items.filter(title__icontains=search)

    # Filter by category
    category_id = request.GET.get("category", "")
    if category_id:
        items = items.filter(category_id=category_id)

    # Filter by minimum amount
    min_amount = request.GET.get("min_amount", "")
    if min_amount:
        items = items.filter(amount__gte=min_amount)

    # Filter by maximum amount
    max_amount = request.GET.get("max_amount", "")
    if max_amount:
        items = items.filter(amount__lte=max_amount)

    # Filter by date range
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    if start_date:
        items = items.filter(date__gte=start_date)

    if end_date:
        items = items.filter(date__lte=end_date)

    # Pagination
    paginator = Paginator(items, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "expenses": page_obj,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "search": search,
        "selected_category": category_id,
        "min_amount": min_amount,
        "max_amount": max_amount,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(
        request,
        "tracker/expense_list.html",
        context
    )



@login_required
def expense_create(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, "Expense added successfully.")
        return redirect("expense_list")
    return render(request, "tracker/expense_form.html", {"form": form, "heading": "Add expense"})

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        messages.success(request, "Expense updated.")
        return redirect("expense_list")
    return render(request, "tracker/expense_form.html", {"form": form, "heading": "Edit expense"})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted.")
        return redirect("expense_list")
    return render(request, "tracker/expense_confirm_delete.html", {"expense": expense})

@login_required
def budget_set(request):
    month_start = timezone.localdate().replace(day=1)
    budget, _ = MonthlyBudget.objects.get_or_create(user=request.user, month=month_start, defaults={"amount": 0})
    form = BudgetForm(request.POST or None, instance=budget)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.month = month_start
        obj.save()
        messages.success(request, "Monthly budget saved.")
        return redirect("dashboard")
    return render(request, "tracker/budget_form.html", {"form": form, "month_name": month_start.strftime("%B %Y")})

@login_required
def export_expenses(request):
    expenses = Expense.objects.filter(
        user=request.user
    ).select_related("category")

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="spendwise_expenses.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Title",
        "Amount",
        "Category",
        "Date",
        "Note"
    ])

    for expense in expenses:
        writer.writerow([
            expense.title,
            expense.amount,
            expense.category.name if expense.category else "",
            expense.date,
            expense.note
        ])

    return response
@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(
        request,
        "tracker/profile.html",
        {"user": request.user, "form": form}
    )
@login_required
def change_password(request):
    return PasswordChangeView.as_view(
        template_name="registration/password_change.html",
        success_url=reverse_lazy("profile")
    )(request)


@login_required
def expense_reports(request):

    # Get all expenses of the logged-in user
    expenses = Expense.objects.filter(user=request.user)

    # Total expenses
    total_expenses = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    # Monthly spending
    monthly_reports = (
        expenses
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("-month")
    )

    # Yearly spending
    yearly_reports = (
        expenses
        .annotate(year=TruncYear("date"))
        .values("year")
        .annotate(total=Sum("amount"))
        .order_by("-year")
    )

    # Highest spending category
    highest_category = (
        expenses
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
        .first()
    )

    # Average monthly spending
    monthly_average = (
        expenses
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .aggregate(average=Avg("total"))["average"]
    ) or 0

    context = {
        "total_expenses": total_expenses,
        "monthly_reports": monthly_reports,
        "yearly_reports": yearly_reports,
        "highest_category": highest_category,
        "monthly_average": monthly_average,
    }

    return render(
        request,
        "tracker/expense_reports.html",
        context
    )
