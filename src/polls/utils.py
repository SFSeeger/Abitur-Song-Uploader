from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, F, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone

from polls.models import Poll, Question, Response


def get_question(obj: Poll, curr_idx: int) -> Question | None:
    try:
        return obj.question_set.all()[curr_idx]
    except IndexError:
        return None


def get_user_polls(user):
    polls = (
        Poll.objects.filter(end_date__gt=timezone.now().date())
        .annotate(num_questions=Count("question"))
        .annotate(
            num_answers=Coalesce(
                Subquery(
                    Response.objects.filter(poll=OuterRef("pk"), user=user)
                    .annotate(num_answers=Count("answer"))
                    .values("num_answers")
                    .order_by("num_answers")[:1]
                ),
                0,
            )
        )
        .exclude(num_questions=F("num_answers"), can_answered_multiple=False)
    )
    return polls


def get_poll_users(poll: Poll):
    User = get_user_model()
    x = (
        Response.objects.filter(poll=poll)
        .annotate(num_answers=Count("answer"))
        .filter(num_answers=poll.question_set.count())
    ).values_list("user", flat=True)
    return User.objects.all().exclude(id__in=x)
