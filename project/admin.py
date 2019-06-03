from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class VoterInline(admin.StackedInline):
    model = Voter
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (VoterInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
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
