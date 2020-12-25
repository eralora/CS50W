from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("products/<int:id>", views.product, name="products"),
    path("create", views.create, name="create"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("add_bid/<int:id>", views.add_bid, name="add_bid"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("close_bid/<int:id>", views.close_bid, name="close_bid"),
    path("categories", views.categories, name="categories"),
    path("category_page/<str:category>", views.category_page, name="category_page")
]
