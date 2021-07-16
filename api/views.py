from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from hasker.models import Question
from hasker.utils import fbv_paginator


@api_view(['GET'])
# @permission_classes(('IsAuthenticated'))
@permission_classes((AllowAny,))
# @permission_classes([IsModelingUser | IsAuthenticatedOrReadOnly])
def get_users(request):
    queryset = User.objects.all().order_by('-date_joined').values('username')
    return Response(queryset)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_index(request):
    """
    get site root / by pages like this:
    curl -H 'Accept: application/json' -u user:***  http://127.0.0.1:4354/api/get_index/?page=2
    :param request:
    :return:
    """
    queryset = Question.objects.all().order_by('-date_create').values('id', 'title', 'content', 'author', 'rating')
    paginated_response = fbv_paginator(request, queryset, 5, "page")
    page_number = paginated_response.get('page_obj').number
    response_content = paginated_response.get('page_obj').object_list
    num_pages = paginated_response.get('page_obj.paginator').num_pages
    return Response({
        'content': response_content,
        'page_number': page_number,
        'num_pages': num_pages,
    })




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


