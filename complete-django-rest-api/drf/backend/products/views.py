from rest_framework import generics, mixins, permissions, authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer
from api.permissions import IsStaffEditorPermissions
from api.authentication import TokenAuthentication
from api.mixins import StaffEditorPermissionMixin, UserQuerysetMixin

# ListCreateAPIView allows both creating a product as well
# as getting the list of existing products


class ProductListCreateAPIView(
    UserQuerysetMixin, StaffEditorPermissionMixin, generics.ListCreateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # field used to identify an specific item
    # lookup_field = 'id'

    def perform_create(self, serializer):
        """Here it's possible to provide all the logic necessary for creating a new product"""
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=user)


# returns a single item
# similar to /api/product/{product_id}
class ProductDetailAPIView(
    UserQuerysetMixin, StaffEditorPermissionMixin, generics.RetrieveAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# field used to identify an specific item
# lookup_field = 'id'


class ProductAPIUpdateView(
    UserQuerysetMixin, StaffEditorPermissionMixin, generics.UpdateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        instance = serializer.save()
        if not serializer.content:
            instance.content = instance.title


class ProductAPIDeleteView(
    UserQuerysetMixin, StaffEditorPermissionMixin, generics.DestroyAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class ProductMixinView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    """
    Mixin views allow for more customization regarding the behavior of the API endpoints.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"  # only useful for RetrieveModelMixin

    def get(self, request, *args, **kwargs):
        """
        If pk is available as a query param then the product with such id will be returned.
        Otherwise the list of existing products will be returned
        """
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True)
        return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            serializer.save()
            return Response(serializer.data)
        return Response(dict(invalid="Not good data"))
