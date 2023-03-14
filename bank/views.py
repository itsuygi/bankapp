from django.shortcuts import render, redirect
from .models import Account, Transaction
from .forms import AccountModelForm, TransactionModelForm
from django.db.models import Q

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        accounts = Account.objects.filter(user=request.user)

        form = AccountModelForm()
        return render(request, "bank/index.html", {
            "accounts": accounts,
            "form": form
        })
    else:
        return render(request, "bank/homepage.html")
    
def account_details(request, id):
    if request.user.is_authenticated:
        account = Account.objects.get(id=id)
        if account.user == request.user:
            if request.method == 'POST':
                form = AccountModelForm(request.POST, instance=account)
                if form.is_valid():
                    form.save()
                    return redirect('home')
                
            form = AccountModelForm(instance=account)
            transactions = Transaction.objects.filter(Q(from_account=id) | Q(to_account=id))

            for transaction in transactions:
                if transaction.to_account == account:
                    transaction.type = "In"
                else:
                    transaction.type = "Out"
            
            return render(request, "bank/account-page.html", {
                "form": form,
                "account": account,
                "transactions": transactions,
                
            })
        else:
            return redirect("home")
    else:
        return render(request, "bank/homepage.html")
        
    
def create_account(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AccountModelForm(request.POST)
            if form.is_valid():
                formInst = form.save(commit=False)
                formInst.user = request.user
                formInst.save()
                return redirect('home')
        form = AccountModelForm()
        return render(request, "bank/new-account.html", {"form": form})
    else:
        return redirect('home')
    
def delete_account(request, id):
    if request.user.is_authenticated:
        account = Account.objects.get(id=id)
        if account.user == request.user:
            account.delete()
    
    return redirect("home")
        
def new_transaction(request, id):
    if request.user.is_authenticated:
        account = Account.objects.get(id=id)
        if account.user == request.user:
            if request.method == 'POST':
                form = TransactionModelForm(request.POST)
                if form.is_valid():
                    amount = form.cleaned_data["amount"]

                    if account.balance >= amount:
                        account.balance -= amount
                        account.save()

                        t_to_account = Account.objects.get(id=form.cleaned_data["to_account"].id)
                        t_to_account.balance += amount
                        t_to_account.save()

                        formInst = form.save(commit=False)
                        formInst.from_account = account
                        formInst.type = "Transfer"
                        formInst.save()

                        return redirect('home')
                    else:
                        form.add_error("amount", "Bakiyeniz yetersiz.")
                        
                return render(request, "bank/new-transaction.html", {
                    "form": form,
                    "account": account,
                    "error": form.errors.as_text
                }) 
                
            form = TransactionModelForm()
            return render(request, "bank/new-transaction.html", {
                "form": form,
                "account": account,
            })
        else:
            return redirect("home")
    else:
        return render(request, "bank/homepage.html")