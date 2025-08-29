from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views.generic import RedirectView

# Import schema consistently from myapp
from myapp.schema import schema  

# Health check endpoint
def health(request):
    return JsonResponse({"status": "ok"})

# Root endpoint
def root(request):
    return JsonResponse({"message": "Backend running 🚀"})

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # Health check
    path("health/", health, name="health"),

    # GraphQL endpoint
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                schema=schema,
                graphiql=True  # Enable GraphiQL interface
            )
        ),
        name="graphql"
    ),

    # Root URL
    path("", root, name="root"),

    # ✅ Handle favicon.ico request (fixes 400/404 errors)
    path("favicon.ico", lambda request: HttpResponse("", content_type="image/x-icon")),
]
