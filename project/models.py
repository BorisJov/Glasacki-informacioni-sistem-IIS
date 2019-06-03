from django.db import models
from django.contrib.auth.models import User


class ElectionType(models.Model):
    secrecy = models.BooleanField()
    candidate_selection_number = models.IntegerField()
    voter_equality = models.BooleanField()


class VotingUnit(models.Model):
    parent_unit = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Election(models.Model):
    election_type = models.ForeignKey(ElectionType, on_delete=models.CASCADE)
    base_unit = models.ForeignKey(VotingUnit, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    begin_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return self.title


class Candidate(models.Model):
    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class OversightBodyPermission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OversightBody(models.Model):
    unit = models.ForeignKey(VotingUnit, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(OversightBodyPermission)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class OversightMember(models.Model):
    units = models.ManyToManyField(OversightBody)


class Voter(models.Model):
    unit = models.ForeignKey(VotingUnit, on_delete=models.CASCADE)


class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = (('election', 'voter'),)


class CandidateChoice(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    value = models.IntegerField(blank=True)

    class Meta:
        unique_together = (('vote', 'candidate'),)
