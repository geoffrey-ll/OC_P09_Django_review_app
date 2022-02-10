from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from itertools import chain


from . import forms, models


@login_required
def flux(request):
    # Pourquoi ce soulignement ?
    # Pourtant cela marche…
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    flux = sorted(chain(tickets, reviews),
                  key=lambda instance: instance.time_created, reverse=True)
    return render(request, "reviews/flux.html", context={"flux": flux})


@login_required
def flux_user(request):
    tickets_user = models.Ticket.objects.filter(Q(user=request.user))
    reviews_user = models.Review.objects.filter(Q(user=request.user))
    flux = sorted(chain(tickets_user, reviews_user),
                  key=lambda instance: instance.time_created, reverse=True)
    return render(request, "reviews/flux.html", context={"flux": flux})


@login_required
def ticked_upload(request):
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect("flux")
    return render(request, "reviews/ticket_upload.html",
                  context={"form": form})


@login_required
def review_upload(request):
    form = forms.ReviewForm()
    if request.method == "POST":
        form = forms.ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("flux")
    return render(request, "reviews/review_upload.html",
                  context={"form": form})


# Un décorateur pour permettre l'accès qu'a son auteur ?
# Ajouter {% if perms.reviews.change_ticket %} dans le HTML, là où doit
# apparaître le boutton de modification.
@login_required
@permission_required("reviews.change_ticket", raise_exception=True)
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.TicketForm(instance=ticket)
    # Un if pour vérifier que user est l'auteur du ticket ?
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("flux")
    return render(request, "reviews/ticket_edit.html",
                  context={"form": form})


# Un décorateur pour permettre l'accès qu'a son auteur ?
# Ajouter {% if perms.reviews.change_review %} dans le HTML, là où doit
# apparaître le boutton de modification.
@login_required
@permission_required("reviews.change_review", raise_exception=True)
def review_edit(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    form = forms.ReviewForm(instance=review)
    # Un if pour vérifier que user est l'auteur de la review ?
    if request.method == "POST":
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("flux")
    return render(request, "reviews/review_edit.html",
                  context={"form": form})
