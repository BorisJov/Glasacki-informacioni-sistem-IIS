from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path('login/', views.voter_login, name="voter_login"),
    path('logout/', views.voter_logout, name="voter_logout"),
    path('voter_homepage/', views.voter_homepage, name="voter_homepage"),
    path('voting_step1/<int:election_id>', views.voting_step1, name="voting_step1"),
    path('voting_step2/<int:election_id>', views.voting_step2, name="voting_step2"),
    path('cast_vote/<int:election_id>', views.cast_vote, name="cast_vote"),
    path('admin_elections/', views.admin_elections, name="admin_elections"),
    path('result_config/<int:election_id>', views.admin_result_config, name="admin_result_config"),
    path('generate_results/', views.admin_generate_results, name="admin_generate_results"),
]