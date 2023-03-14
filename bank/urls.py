from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("create-account", views.create_account, name="create-account"),
    path("account/<int:id>", views.account_details, name="account-page"),
    path("account/<int:id>/transaction", views.new_transaction, name="new-transaction"),
    path("account/<int:id>/delete", views.delete_account, name="delete-account"),
]