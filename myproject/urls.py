from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from django.http import HttpResponse  # ADD THIS IMPORT

from myproject.schema import schema  # Project-level GraphQL schema

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # Health check endpoint - ADD THIS TEMPORARILY
    path("health/", lambda request: HttpResponse("OK"), name="health"),

    # GraphQL endpoint for React frontend - CSRF COMPLETELY DISABLED for testing
    path(
        "graphql/",
        csrf_exempt(  # ✅ This should completely disable CSRF for GraphQL
            GraphQLView.as_view(
                schema=schema,
                graphiql=True  # Enable GraphiQL interface
            )
        ),
        name="graphql"
    ),

    # Redirect root URL to admin login page
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
]