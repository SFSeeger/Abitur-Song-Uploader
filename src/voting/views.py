from django.views.generic.edit import FormView
from django.shortcuts import redirect
from .forms import CreateForm, VoteForm
from .models import Vote, Option

class CreateFormView(FormView):
    template_name = 'create_option.html'
    form_class = CreateForm
    success_url = '/'
    
    def form_valid(self, form):
        if not Option.objects.filter(name=form.cleaned_data.get('name')):
            Option.objects.create(name=form.cleaned_data.get('name'))
        return super().form_valid(form)

class SubmitVoteFormView(FormView):
    template_name = 'vote.html'
    form_class = VoteForm
    success_url = '/'

    def form_valid(self, form: VoteForm):
        # Check if user has already submitted 
        user_votes = Vote.objects.filter(user=self.request.user)
        if user_votes.count() >= 5:
            return redirect('/')
        # else create Vote 
        for choice in form.cleaned_data.choices.choices:
            vote = Vote(user=self.request.user, option=choice)
            vote.save()
        return super().form_valid(form)