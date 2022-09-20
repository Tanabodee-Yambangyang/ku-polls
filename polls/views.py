from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """The view of Index page."""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """The view of Detail page."""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """If someone navigates to a poll detail page when voting is not allowed,
        redirect them to the polls index page and show an error message on the page.
        """
        question_id = kwargs["pk"]
        question = get_object_or_404(Question, pk=question_id)
        user = request.user

        if not question.can_vote():
            messages.error(request, f"Error!!! >>> Question: {question} is not available.")
            return redirect("polls:index")
        else:
            try:
                vote = Vote.objects.get(user=user, choice__question=question)
                voted_choice = vote.choice.choice_text
            except (Vote.DoesNotExist, TypeError):
                voted_choice = ""
        return render(request, self.template_name, {"question": question, "vote": voted_choice})


class ResultsView(generic.DetailView):
    """The view of Results page."""
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        """If someone navigates to a poll detail page when voting is not allowed,
        redirect them to the polls index page and show an error message on the page.
        """
        question_id = kwargs["pk"]
        question = get_object_or_404(Question, pk=question_id)

        if not question.can_vote():
            messages.error(request, f"Error!!! >>> Question: {question} is not available.")
            return redirect("polls:index")
        else:
            return render(request, self.template_name, {"question": question})


@login_required
def vote(request, question_id):
    """View for voting.
    Parameters:
        question_id : The ID of the question
    """
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            vote = Vote.objects.get(user=user, choice__question=question)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(user=user, choice=selected_choice)
            vote.save()
        else:
            vote.choice = selected_choice
            vote.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


