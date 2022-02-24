from django.test import TestCase
from django.db.models import Q
from itertools import chain


from . import models
from authentication import models as models_auth


# Create your tests here.
def get_users_relations(user):
    relations_users = models_auth.UserFollows.objects.filter(Q(user=user))
    return relations_users


def get_reviews_followed(user):
    relations_users = get_users_relations(user)
    reviews_followed = []
    for relation in relations_users:
        review = models.Review.objects.filter(Q(user=relation.followed_user))
        if len(review) != 0:
            if isinstance(reviews_followed, list) is True:
                reviews_followed = review
            else:
                reviews_followed = reviews_followed.union(review)

    # print(f"\nReviews_followed:\n{reviews_followed}\n")
    return reviews_followed


def get_reviews_answer_my_tickets(user):
    tickets_user = get_tickets_user(user)
    relations_users = get_users_relations(user)
    reviews_remaining = []
    for ticket in tickets_user:
        # Pour l'instant les critique ne sont pas unique à un ticket donc
        # reviews peut contenir plus d'un élèment.
        # get n'est pas utilisable car ne reviews non unique et ne renvoi pas
        # un QuerySet. J'ai besoin que tous soit des QuerySet pour le chain()
        reviews = models.Review.objects\
            .filter(Q(ticket=ticket.id))\
            .exclude(user=user)

        if len(reviews) != 0:
            for review in reviews:
                count = 0
                for relation in relations_users:
                    if review.user == relation.followed_user:
                        count += 1
                        break
                if count == 0:
                    if isinstance(reviews_remaining, list) is True:
                        reviews_remaining = \
                            models.Review.objects.filter(id=review.id)
                    else:
                        temp = \
                            models.Review.objects.filter(id=review.id)
                        reviews_remaining = reviews_remaining.union(temp)
    # print(f"\nReviews_remaining FINAL:\n{reviews_remaining}\n")
    return reviews_remaining


def get_users_viewable_reviews(user):
    # Mes critiques (un QuerySet)
    reviews_user = models.Review.objects.filter(Q(user=user))
    # Critiques de mes abonnements (un QuerySet)
    reviews_followed = get_reviews_followed(user)
    # Critiques en réponse à mes tickets (hors précédents) (un QuerySet)
    reviews_answer_my_tickets = get_reviews_answer_my_tickets(user)
    # Critiques en réponse aux tickets de mes abonnements (hors précédents)
    # Non demandé ??
    users_viewable_reviews = \
        chain(reviews_user, reviews_followed, reviews_answer_my_tickets)
    return users_viewable_reviews


def get_tickets_user(user):
    tickets_user = models.Ticket.objects.filter(Q(user=user))
    return tickets_user


def get_tickets_followed(user):
    relations_users = get_users_relations(user)
    tickets_followed = []
    for relation in relations_users:
        tickets = models.Ticket.objects.filter(Q(user=relation.followed_user))
        if len(tickets) != 0:
            if isinstance(tickets_followed, list) is True:
                tickets_followed = tickets
            else:
                tickets_followed = tickets_followed.union(tickets)

    # print(f"\nTicktes_followed:\n{tickets_followed}\n")
    # print(f"\ntype:\n{type(tickets_followed)}\n")
    return tickets_followed


def get_users_viewable_tickets(user):
    # Mes tickets (un QuerySet)
    tickets_user = get_tickets_user(user)
    # Ticktes de mes abonnements (un QuerySet)
    tickets_followed = get_tickets_followed(user)
    users_viewable_tickets = chain(tickets_user, tickets_followed)
    return users_viewable_tickets