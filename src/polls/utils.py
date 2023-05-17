from polls.models import Poll, Question


def get_question(obj: Poll, curr_idx: int) -> Question | None:
    try:
        return obj.question_set.all()[curr_idx]
    except IndexError:
        return None
