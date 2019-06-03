from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ElectionType)
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(VotingUnit)
admin.site.register(OversightBodyPermission)
admin.site.register(OversightBody)
admin.site.register(OversightMember)
admin.site.register(Voter)
admin.site.register(Vote)
admin.site.register(CandidateChoice)
