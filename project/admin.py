from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class VoterInline(admin.StackedInline):
    model = Voter
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (VoterInline,)


class VoterAdmin(admin.ModelAdmin):
    list_display = ('user', 'unit', 'voting_power')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "unit":
            kwargs["queryset"] = VotingUnit.objects.filter(
                voters_can_be_added=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class VotingUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_unit', 'voters_can_be_added')


class ElectionTypeAdmin(admin.ModelAdmin):
    list_display = ('secrecy', 'candidate_selection_number', 'voter_equality')


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'election')


class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'election_type', 'base_unit', 'begin_datetime', 'end_datetime')
    

class VoteAdmin(admin.ModelAdmin):
    list_display = ('election', 'voter', 'timestamp')


class CandidateChoiceAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'value')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ElectionType, ElectionTypeAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(VotingUnit, VotingUnitAdmin)
admin.site.register(OversightBodyPermission)
admin.site.register(OversightBody)
admin.site.register(OversightMember)
admin.site.register(Voter, VoterAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(CandidateChoice, CandidateChoiceAdmin)
