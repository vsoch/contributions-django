from django.db import models


class Event(models.Model):
    """An example model that has a date. We can create entries and then
       a GitHub contributions graph to show latest entries
    """

    name = models.CharField(max_length=500, unique=True, blank=False, null=False,)
    date = models.DateTimeField()
    add_date = models.DateTimeField("date added", auto_now_add=True)
    modify_date = models.DateTimeField("date modified", auto_now=True)

    def get_label(self):
        return "event"

    class Meta:
        app_label = "main"
