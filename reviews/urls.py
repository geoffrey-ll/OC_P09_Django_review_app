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


from .views import flux_user, posts_user
from .views import ticked_upload, ticket_edit, ticket_delete
from .views import review_upload, review_edit, review_delete, \
    review_ticket_answer


urlpatterns = [
    path("flux_user", flux_user, name="flux-user"),
    path("posts_user", posts_user, name="posts-user"),
    path("ticket_upload", ticked_upload, name="ticket-upload"),
    path("tickets/<int:ticket_id>", ticket_edit, name="ticket-edit"),
    path("tickets/<int:ticket_id>/delete", ticket_delete, name="ticket-delete"),
    path("review_upload", review_upload, name="review-upload"),
    path("review_upload/ticket/<int:ticket_id>",
         review_ticket_answer, name="ticket-answer"),
    path("reviews/<int:review_id>", review_edit, name="review-edit"),
    path("reviews/<int:review_id>/delete", review_delete, name="review-delete")
]
