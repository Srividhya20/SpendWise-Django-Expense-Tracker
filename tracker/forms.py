from django import forms
from .models import Expense, MonthlyBudget

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "date", "note"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"}), "note": forms.Textarea(attrs={"rows": 3})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "field"})

class BudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = ["month", "amount"]
        widgets = {"month": forms.DateInput(attrs={"type": "date"})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "field"})
