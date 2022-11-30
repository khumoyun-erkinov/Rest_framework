from django.contrib.auth.models import User
from rest_framework import generics
from snippets.serializers import UserSerializer
from rest_framework import permissions
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers


# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


@api_view(['GET'])
def api_root(request,format=None):
    return Response({
        'user':reverse('user-list',request=request,format=format),
        'snippets':reverse('snippets-list',request=request,format=format)
    })
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]
    def get(self,request,*args,**kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)








