"""
URL configuration for swishcoin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import get_chain, mine_block, post_question, post_answer, vote_answer, reward_best_answer, ask_question, \
    view_question, answer_question, blockchain_explorer, user_balances, transactions, home, signup_view, \
    profile_view, send_swishcoin, list_questions, user_list, logout_view, login_view

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('get_chain/', get_chain),
    path("mine_block/", mine_block, name="mine_block"),
    path("post_question/", post_question),
    path("question/<int:question_id>/answer/", post_answer, name="post_answer"),
    path("vote_answer/", vote_answer),
    path("question/<int:question_id>/reward_best_answer/", reward_best_answer, name="reward_best_answer"),
    path("questions/", list_questions, name="list_questions"),
    path("ask_question/", post_question, name="post_question"),
    path("question/<int:question_id>/", view_question, name="view_question"),
    path("answer_question/<int:question_id>/", answer_question),
    path("explorer/", blockchain_explorer, name="explorer"),
    path("user_balances/", user_balances, name="user_balances"),
    path("send_swishcoin/", send_swishcoin, name="send_swishcoin"),
    path("transactions/", transactions, name="transactions"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),  # Ensure this exists
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("users/", user_list, name="user_list"),

    # Password Reset URLs
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name="password_reset_complete"),
]
