from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path('', views.voter_homepage, name="voter_homepage"),
    path('voting_step1/<int:election_id>', views.voting_step1, name="voting_step1"),
    path('voting_step2/<int:election_id>', views.voting_step2, name="voting_step2"),
    path('cast_vote/<int:election_id>', views.cast_vote, name="cast_vote"),
]