from datetime import date, timedelta, datetime
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
#import pdb; pdb.set_trace()

def voter_homepage(request):
    user = request.user
    voter = user.voter
    vunit = voter.unit

    elections = []
    if vunit.parent_unit is None:
        elections = vunit.election_set.filter(
            begin_datetime__lte=datetime.now(), end_datetime__gte=datetime.now())
    else:
        while vunit is not None:
            els = vunit.election_set.filter(
                begin_datetime__lte=datetime.now(), end_datetime__gte=datetime.now())
            for el in els:
                elections.append(el)
            vunit = vunit.parent_unit

    tmp_elections = []
    for election in elections:
        if not election.vote_set.filter(voter=voter).exists():
            tmp_elections.append(election)
    elections = tmp_elections

    context = {'elections': elections}
    return render(request, 'project/voter_homepage.html', context)

def voting_step1(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    context = {'election': election}
    return render(request, 'project/voting_step1.html', context)
    

def voting_step2(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = election.candidate_set.all()
    selection_range = list(range(1, election.election_type.candidate_selection_number + 1))
    context = {
        'election': election,
        'candidates': candidates,
        'selection_range': selection_range
        }
    return render(request, 'project/voting_step2.html', context)


def cast_vote(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    sel_num = election.election_type.candidate_selection_number
    user = request.user
    vote = Vote()
    vote.voter = user.voter
    vote.timestamp = datetime.now()
    vote.election = election
    vote.save()

    dup_list = []
    dup_num = 0
    for i in range(1, sel_num + 1):
        candidate_id = request.POST.get('choice_' + str(i))
        candidate = get_object_or_404(Candidate, pk=candidate_id)

        if candidate_id not in dup_list:
            dup_list.append(candidate_id)
            cc = CandidateChoice()
            cc.vote = vote
            cc.candidate = candidate
            cc.value = i - dup_num
            cc.save()
        else:
            dup_num = dup_num + 1
    return render(request, 'project/finished_voting.html')
