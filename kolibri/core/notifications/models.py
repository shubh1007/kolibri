"""
This is the model used to create notifications that are calculated based
on the information different logs provide.

If using sqlite, all the information is saved in a separate database to avoid
performance problems due to the locks on the main database.

None of these models will have Morango synchronization
"""
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from morango.models import UUIDField

from kolibri.core.fields import DateTimeTzField
from kolibri.core.fields import JSONField
from kolibri.deployment.default.sqlite_db_names import NOTIFICATIONS
from kolibri.utils.data import ChoicesEnum
from kolibri.utils.time_utils import local_now

# Remove NotificationsRouter if sqlite is not being used:
if settings.DATABASES["default"]["ENGINE"] != "django.db.backends.sqlite3":
    ROUTER_ID = "kolibri.core.notifications.models.NotificationsRouter"
    if ROUTER_ID in settings.DATABASE_ROUTERS:
        settings.DATABASE_ROUTERS = tuple(
            filter(lambda x: x != ROUTER_ID, settings.DATABASE_ROUTERS)
        )


class NotificationsRouter(object):
    """
    Determine how to route database calls for the Notifications app.
    All other models will be routed to the default database.
    """

    def db_for_read(self, model, **hints):
        """Send all read operations on Notifications app models to NOTIFICATIONS."""
        if model._meta.app_label == "notifications":
            return NOTIFICATIONS
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on Notifications app models to NOTIFICATIONS."""
        if model._meta.app_label == "notifications":
            return NOTIFICATIONS
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        # Allow any relation between two models that are both in the Notifications app.
        if (
            obj1._meta.app_label == "notifications"
            and obj2._meta.app_label == "notifications"
        ):
            return True
        # No opinion if neither object is in the Notifications app (defer to default or other routers).
        elif "notifications" not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Block relationship if one object is in the Notifications app and the other isn't.
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the Notifications app's models get created on the right database."""
        if app_label == "notifications":
            # The Notifications app should be migrated only on the NOTIFICATIONS database.
            return db == NOTIFICATIONS
        elif db == NOTIFICATIONS:
            # Ensure that all other apps don't get migrated on the NOTIFICATIONS database.
            return False

        # No opinion for all other scenarios
        return None


class NotificationObjectType(ChoicesEnum):
    Resource = "Resource"
    Quiz = "Quiz"
    Help = "Help"
    Lesson = "Lesson"


class NotificationEventType(ChoicesEnum):
    Started = "Started"
    Completed = "Completed"
    Help = "HelpNeeded"
    Answered = "Answered"


class HelpReason(ChoicesEnum):
    Multiple = "MultipleUnsuccessfulAttempts"


class LearnerProgressNotification(models.Model):
    id = (
        models.AutoField(
            auto_created=True, primary_key=True, serialize=True, verbose_name="ID"
        ),
    )
    notification_object = models.CharField(
        max_length=200, choices=NotificationObjectType.choices(), blank=True
    )
    notification_event = models.CharField(
        max_length=200, choices=NotificationEventType.choices(), blank=True
    )
    user_id = UUIDField()
    classroom_id = UUIDField()  # This is a Classroom id
    assignment_collections = JSONField(null=True, default=[])
    contentnode_id = UUIDField(null=True)
    lesson_id = UUIDField(null=True)
    quiz_id = UUIDField(null=True)
    quiz_num_correct = models.IntegerField(null=True)
    quiz_num_answered = models.IntegerField(null=True)
    reason = models.CharField(max_length=200, choices=HelpReason.choices(), blank=True)
    timestamp = DateTimeTzField(default=local_now)

    def __str__(self):
        return "{object} - {event}".format(
            object=self.notification_object, event=self.notification_event
        )

    class Meta:
        app_label = "notifications"


class NotificationsLog(models.Model):
    id = (
        models.AutoField(
            auto_created=True, primary_key=True, serialize=True, verbose_name="ID"
        ),
    )
    coach_id = UUIDField()
    timestamp = DateTimeTzField(default=local_now)

    def __str__(self):
        return self.coach_id

    class Meta:
        app_label = "notifications"
