"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path


from reviews.views import ticked_upload
from reviews.views import ticket_edit
from reviews.views import review_upload
from reviews.views import ticket_answer
from reviews.views import review_edit
from reviews.views import flux
from reviews.views import flux_user


urlpatterns = [
    path("", flux, name="flux"),
    path("flux_user", flux_user, name="flux-user"),
    path("ticket_upload", ticked_upload, name="ticket-upload"),
    path("tickets/<int:ticket_id>", ticket_edit, name="ticket-edit"),
    path("review_upload", review_upload, name="review-upload"),
    path("review_upload/ticket/<int:ticket_id>", ticket_answer,
         name="ticket-answer"),
    path("reviews/<int:review_id>", review_edit, name="review-edit"),
]
