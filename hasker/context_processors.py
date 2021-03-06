from hasker.models import Question


def trending(request):
    return {
        'trending': Question.objects.order_by('-rating', '-date_create')[:10]
    }
