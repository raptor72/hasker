from hasker.models import Question


def trending(req):
    return {
        'trending': Question.objects.order_by('-rating', '-date_create')[:20]
    }
