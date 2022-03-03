from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from itertools import chain


from authentication.models import UserFollow
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review


MESSAGE_DENIED = "Accès refusé, car vous n'êtes pas l'auteur"
TAGS_DENIED = "alert alert-primary bs-perso-message"
MESSAGE_ALREADY_ANSWER = "Vous avez déjà publié une critique à ce ticket"


@login_required
def flux_user(request):
    """Flux visible par l'utilisateur."""
    tickets, reviews = get_users_viewable_posts(request.user)
    flux = sorted(chain(tickets, reviews),
                  key=lambda instance: instance.time_created,
                  reverse=True)
    return render(request, "reviews/flux.html",
                  context={"flux": flux, "option": "flux-user"})


def get_users_viewable_posts(user):
    """Retourne les tickets et reviews visibles par l'utilisateur."""
    relations_users = UserFollow.objects.filter(user=user)
    followed_user = [r.followed_user for r in relations_users]

    tickets_of_user = Ticket.objects.filter(user=user)
    tickets_of_followed = Ticket.objects.filter(user__in=followed_user)

    reviews_of_user = Review.objects.filter(user=user)
    reviews_of_followed = Review.objects.filter(user__in=followed_user)
    reviews_to_user = Review.objects.filter(ticket__in=tickets_of_user)
    reviews_to_followed = Review.objects.filter(ticket__in=tickets_of_followed)

    viewable_tickets = set(chain(tickets_of_user, tickets_of_followed))
    viewable_reviews = set(chain(reviews_of_user, reviews_of_followed,
                                 reviews_to_user, reviews_to_followed))
    return viewable_tickets, viewable_reviews


@login_required
def posts_user(request):
    """Les posts de l'utilisateur."""
    tickets_user = Ticket.objects.filter(user=request.user)
    reviews_user = Review.objects.filter(user=request.user)
    flux = sorted(chain(tickets_user, reviews_user),
                  key=lambda instance: instance.time_created,
                  reverse=True)
    return render(request, "reviews/flux.html",
                  context={"flux": flux, "option": "posts-user"})


@login_required
def ticked_upload(request):
    """Création d'un ticket."""
    form = TicketForm()
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("flux-user")
    return render(request, "reviews/ticket_form.html",
                  context={"form": form})


@login_required
def review_upload(request):
    """Création d'une review et d'un ticket en même temps."""
    form_review = ReviewForm()
    form_ticket = TicketForm()
    if request.method == "POST":
        form_review = ReviewForm(request.POST, request.FILES)
        form_ticket = TicketForm(request.POST, request.FILES)
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


def review_ticket_answer(request, ticket_id):
    """Création d'une review en réponse à un ticket existant."""
    form = ReviewForm()
    ticket = Ticket.objects.get(id=ticket_id)
    already_answer = Review.objects.filter(ticket=ticket)
    if len(already_answer) != 0:
        messages.error(request,
                      MESSAGE_ALREADY_ANSWER)
        return redirect("flux-user")

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("flux-user")
    return render(request, "reviews/ticket_answer.html",
                  context={"form": form,
                           "post": ticket})


@login_required
def ticket_edit(request, ticket_id):
    """Édition d'un de ses tickets."""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = TicketForm(instance=ticket)
    if ticket.user == request.user:
        if request.method == "POST":
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect("posts-user")
    else:
        messages.error(request, MESSAGE_DENIED,
                       extra_tags=TAGS_DENIED)
        return redirect("flux-user")
    return render(request, "reviews/ticket_form.html",
                  context={"form": form, "option": "edit"})


@login_required
def review_edit(request, review_id):
    """Édition d'une de ses reviews."""
    review = get_object_or_404(Review, id=review_id)
    form = ReviewForm(instance=review)
    ticket = Ticket.objects.get(id=review.ticket_id)
    if review.user == request.user:
        if request.method == "POST":
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                form.save()
                return redirect("posts-user")
    else:
        messages.error(request, MESSAGE_DENIED,
                       extra_tags=TAGS_DENIED)
        return redirect("flux-user")
    return render(request, "reviews/ticket_answer.html",
                  context={"form": form, "post": ticket, "option": "edit"})


@login_required
def ticket_delete(request, ticket_id):
    """Suppression d'un de ses tickets."""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user == request.user:
        if request.method == "POST":
            ticket.delete()
            return redirect("posts-user")
    else:
        messages.error(request, MESSAGE_DENIED,
                       extra_tags=TAGS_DENIED)
        return redirect("flux-user")
    return render(request, "reviews/delete_view.html",
                  context={"post": ticket, "delete": "ticket"})


@login_required
def review_delete(request, review_id):
    """Suppression d'une de ses reviews."""
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        if request.method == "POST":
            review.delete()
            return redirect("posts-user")
    else:
        messages.error(request, MESSAGE_DENIED,
                       extra_tags=TAGS_DENIED)
        return redirect("flux-user")
    return render(request, "reviews/delete_view.html",
                  context={"post": review, "delete": "critique"})
