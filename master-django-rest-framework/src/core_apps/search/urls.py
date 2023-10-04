from django.urls import path

from .views import ArticleElasticSearchView

urlpatterns = [
    path(
        "search/",
        view=ArticleElasticSearchView.as_view({"get": "list"}),
        name="article_search",
    )
]
