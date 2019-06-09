from datetime import date, timedelta, datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

#import pdb; pdb.set_trace()


@login_required()
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


@login_required()
def voting_step1(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    context = {'election': election}
    return render(request, 'project/voting_step1.html', context)


@login_required()
def voting_step2(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = election.candidate_set.all()
    selection_range = list(
        range(1, election.election_type.candidate_selection_number + 1))
    context = {
        'election': election,
        'candidates': candidates,
        'selection_range': selection_range
    }
    return render(request, 'project/voting_step2.html', context)


@login_required()
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


def voter_login(request):
    if request.method == 'GET':
        return render(request, 'project/voter_login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('project:voter_homepage')
        else:
            return render(request, 'project/voter_login.html')


@login_required()
def voter_logout(request):
    logout(request)
    return redirect('project:voter_login')


@login_required()
def admin_elections(request):
    elections = Election.objects.all()
    context = {'elections': elections}
    return render(request, 'project/admin_elections.html', context)


@login_required()
def admin_result_config(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    if election.election_type.candidate_selection_number == 1:
        bunit = election.base_unit
        depth = 1
        if bunit.votingunit_set.exists():
            cunit = bunit
            while cunit.votingunit_set.exists():
                cunit = cunit.votingunit_set.first()
                depth = depth + 1

        selection_range = list(range(1, depth + 1))
        context = {'selection_range': selection_range, 'election': election}
        return render(request, 'project/admin_result_config.html', context)
    else:
        votes = Vote.objects.filter(election=election).all()
        choice_number = election.election_type.candidate_selection_number
        have_majority = False
        results = dict()
        result_history = []

        vote_count = 0
        for vote in votes:
            vote_count += vote.voter.voting_power
        for candidate in election.candidate_set.all():
            results[candidate] = 0
        while not have_majority:
            for candidate in results.keys():
                results[candidate] = 0
            for vote in votes:
                for val in range(1, choice_number + 1):
                    choice = vote.candidatechoice_set.filter(value=val).get()
                    if choice.candidate in results.keys():
                        results[choice.candidate] += 1
                        break
            result_history.append(results.copy())
            if max(results.values()) > 0.5 * float(vote_count):
                have_majority = True
            else:
                min_candidate = min(results, key=results.get)
                results.pop(min_candidate)
        
        context = {
            'result_history': result_history,
            'election': election
        }
        return render(request, 'project/alternative_results.html', context)
                
            



def get_unit_results(unit, election):
    # prepare ret_val
    ret_val = dict()
    for candidate in election.candidate_set.all():
        ret_val[candidate] = 0

    # do cool recursion stuff
    if unit.votingunit_set.exists():
        for subunit in unit.votingunit_set.all():
            tmp = get_unit_results(subunit, election)
            for candidate in tmp:
                ret_val[candidate] += tmp[candidate]
        return ret_val
    else:
        unit_voters = unit.voter_set.all()
        votes = Vote.objects.filter(election=election, voter__in=unit_voters)
        for vote in votes:
            choice = vote.candidatechoice_set.filter(value=1).get()
            ret_val[choice.candidate] += vote.voter.voting_power
        return ret_val


def unit_level_list(unit, level):
    ret_val = []
    if level <= 1:
        ret_val.append(unit)
        return ret_val
    else:
        for subunit in unit.votingunit_set.all():
            ret_val = ret_val + unit_level_list(subunit, level-1)
        return ret_val


def bottoms_up(unit_list):
    ret_val = []
    ret_val.append(unit_list)
    curr_list = unit_list
    while len(curr_list) > 1:
        tmp = []
        for unit in curr_list:
            if unit.parent_unit not in tmp:
                tmp.append(unit.parent_unit)
        ret_val.append(tmp)
        curr_list = tmp
    return ret_val


@login_required()
def admin_generate_results(request):
    election = get_object_or_404(Election, pk=request.POST.get("election_id"))
    level = int(request.POST.get("level_select"))
    chart_type = request.POST.get("chart_type")
    
    level_units = unit_level_list(election.base_unit, level)
    results = []
    for unit in level_units:
        results.append(get_unit_results(unit, election))
    complete_tree = bottoms_up(level_units)
    complete_tree.reverse()

    candidates = election.candidate_set.all()
    context = {
        'level_units': level_units,
        'results': results,
        'complete_tree': complete_tree,
        'candidates': candidates,
        'election': election,
        'chart_type': chart_type
    }
    return render(request, 'project/election_results.html', context)