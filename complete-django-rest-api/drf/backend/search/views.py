from products.models import Product
from products.serializers import ProductSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from . import client


class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user.username if request.user.is_authenticated else None
        query = request.GET.get("q")
        tag = request.GET.get("tag") or None
        public = str(request.GET.get("public")) != "0"
        if not query:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        results = client.perform_search(query, tags=tag, user=user, public=public)
        return Response(results)


class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get("q")
        if q is None:
            return Product.objects.none()

        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
        return qs.search(q, user=user)
