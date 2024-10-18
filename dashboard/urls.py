from django.urls import path


from django.urls import path
from .views import dashboard_view, generate_podcast_view

urlpatterns = [
    path('', dashboard_view, name='podcast_dashboard'),  # Dashboard home page
    path('generate-podcast/', generate_podcast_view, name='generate_podcast_view'),  # URL for podcast generation
]

