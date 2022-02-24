from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from itertools import chain


from . import forms, models, tests
from authentication import models as models_auth


MESSAGE_DENIED = "Accès refusé, car vous n'êtes pas l'auteur"
MESSAGE_EXTRA_TAGS = "alert alert-primary bs-perso-message"


@login_required
def flux_user(request):
    # Ses posts + posts des user suivis + reviews à ses tickets même si l'user
    # n'est pas suivi
    tickets = tests.get_users_viewable_tickets(request.user)
    reviews = tests.get_users_viewable_reviews(request.user)
    flux = sorted(chain(tickets, reviews),
                  key=lambda instance: instance.time_created, reverse=True)
    return render(request, "reviews/flux.html",
                  context={"flux": flux, "option": "flux-user"})


@login_required
def posts_user(request):
    tickets_user = models.Ticket.objects.filter(Q(user=request.user))
    reviews_user = models.Review.objects.filter(Q(user=request.user))
    flux = sorted(chain(tickets_user, reviews_user),
                  key=lambda instance: instance.time_created, reverse=True)
    return render(request, "reviews/flux.html",
                  context={"flux": flux, "option": "posts-user"})


@login_required
def ticked_upload(request):
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("flux-user")
    return render(request, "reviews/ticket_form.html",
                  context={"form": form})


@login_required
def review_upload(request):
    form_review = forms.ReviewForm()
    form_ticket= forms.TicketForm()
    if request.method == "POST":
        form_review = forms.ReviewForm(request.POST, request.FILES)
        form_ticket = forms.TicketForm(request.POST, request.FILES)
        if form_review.is_valid() and form_ticket.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            ticket.save()
            review.save()
            return redirect("flux-user")
    return render(request, "reviews/review_upload.html",
                  context={"form_review": form_review,
                           "form_ticket": form_ticket})


def ticket_answer(request, ticket_id):
    form = forms.ReviewForm()
    ticket = models.Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        form = forms.ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("flux-user")
    return render(request, "reviews/ticket_answer.html",
                  context={"form": form,
                           "post": ticket})


# Un décorateur pour permettre l'accès qu'a son auteur ?
# Ajouter {% if perms.reviews.change_ticket %} dans le HTML, là où doit
# apparaître le boutton de modification.
@login_required
# @permission_required("reviews.change_ticket", raise_exception=True)
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.TicketForm(instance=ticket)
    if ticket.user == request.user:
        if request.method == "POST":
            form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect("posts-user")
    else:
        messages.error(request, MESSAGE_DENIED,
                       extra_tags=MESSAGE_EXTRA_TAGS)
        return redirect("flux-user")
    return render(request, "reviews/ticket_form.html",
                  context={"form": form, "option": "edit"})


# Un décorateur pour permettre l'accès qu'a son auteur ?
# Ajouter {% if perms.reviews.change_review %} dans le HTML, là où doit
# apparaître le boutton de modification.
@login_required
# @permission_required("reviews.change_review", raise_exception=True)
def review_edit(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    form = forms.ReviewForm(instance=review)
    ticket = models.Ticket.objects.get(id=review.ticket_id)
    # Un if pour vérifier que user est l'auteur de la review ?
    if review.user == request.user:
        if request.method == "POST":
            form = forms.ReviewForm(request.POST, request.FILES,
                                    instance=review)
            if form.is_valid():
                form.save()
                return redirect("posts-user")
    else:
        messages.error(request, MESSAGE_DENIED,
                       extra_tags=MESSAGE_EXTRA_TAGS)
        return redirect("flux-user")
    return render(request, "reviews/ticket_answer.html",
                  context={"form": form, "post": ticket, "option": "edit"})


@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if ticket.user == request.user:
        if request.method == "POST":
            ticket.delete()
            return redirect("posts-user")
    else:
        messages.error(request, MESSAGE_DENIED,
                       extra_tags=MESSAGE_EXTRA_TAGS)
        return redirect("flux-user")
    return render(request, "reviews/delete_view.html",
                  context={"post": ticket, "delete": "ticket"})


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if review.user == request.user:
        if request.method == "POST":
            review.delete()
            return redirect("posts-user")
    else:
        messages.error(request, MESSAGE_DENIED,
                       extra_tags=MESSAGE_EXTRA_TAGS)
        return redirect("flux-user")
    return render(request, "reviews/delete_view.html",
                  context={"post": review, "delete": "critique"})
