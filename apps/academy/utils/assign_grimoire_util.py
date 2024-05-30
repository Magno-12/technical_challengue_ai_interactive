import random

from apps.academy.models.grimoire import Grimoire
from apps.academy.models.assignment import Assignment

def assign_grimoire_to_application(application):
    if application.status == 'approved':
        available_grimoires = Grimoire.objects.filter(assignment=None)

        if available_grimoires.exists():
            grimoire = random.choice(available_grimoires)
            Assignment.objects.create(application=application, grimoire=grimoire)
