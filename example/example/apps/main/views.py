# -*- coding: utf-8 -*-

from .models import Event

from contributions_django.graphs import generate_contributors_graph
from django.shortcuts import render


def events_view(request):
    """Generate a papers graph using all Events dates
    """
    # A single list of timestamps
    dates = Event.objects.values_list("date", flat=True)

    # Context is namespaced by contributions_django so you don't need to worry
    # about overriding your existing context, if merging two.
    context = generate_contributors_graph(dates)
    return render(request, "events/index.html", context)
