from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView

from myproject.schema import schema  # Project-level GraphQL schema

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # GraphQL endpoint for React frontend
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                schema=schema,
                graphiql=True  # ✅ CHANGE TO True - This enables proper request handling
            )
        ),
        name="graphql"
    ),

    # Redirect root URL to admin login page
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
]