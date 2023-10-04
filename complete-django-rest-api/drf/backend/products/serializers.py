from api.serializers import UserPublicSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", lookup_field="pk", read_only=True
    )
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user", read_only=True)
    sale_price = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    related_products = ProductInlineSerializer(
        source="user.product_set.all", read_only=True, many=True
    )

    # Another alternative for for field validation is
    # to create a validation function and use the validators parameter in either the
    # correspondent serializer or model class
    # e.g.
    # title = serializers.CharField(validators=[validate_title])
    # Here, validate_title is a custom validation function
    # declared somewhere else

    class Meta:
        model = Product
        fields = [
            "owner",
            "title",
            "content",
            "price",
            "sale_price",
            "url",
            "related_products",
            "public",
        ]

    def get_sale_price(self, obj: Product):
        return obj.get_sale_price()

    def get_url(self, obj: Product):
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("product-detail", kwargs={"pk": obj.pk}, request=request)

    # def validate_title(self, value):
    #     """
    #     Custom validation of a field (In this case, the field is title)
    #     The structure of a validation function is as follows:

    #     def validate_<field_name>(self, value):

    #     it should return the validated value or raise an exception

    #     Args:
    #         value (Any): The value to be validated

    #     Raises:
    #         serializers.ValidationError: _description_

    #     Returns:
    #         Any: The validated value
    #     """
    #     request = self.context.get("request")
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError("f{value} already exists")
    #     return value
