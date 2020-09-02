from django.shortcuts import render
from django.views import generic as genr
from .models import Question, Answer
from django.contrib.auth import mixins as mxn
from django.urls import reverse_lazy

# Create your views here.


class HomePage(genr.TemplateView):
    template_name = 'core/home_page.html'


class QuestionListView(genr.ListView):
    model = Question


class QuestionDetailView(genr.DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answer_list'] = Answer.objects.all()
        return context


class QuestionCreateView(mxn.LoginRequiredMixin, genr.CreateView):
    model = Question
    fields = ['title', 'question', 'related_tag']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class AnswerCreateView(mxn.LoginRequiredMixin, genr.CreateView):
    model = Answer
    fields = ['answer', 'question']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class QuestionDeleteView(mxn.LoginRequiredMixin, genr.DeleteView):
    model = Question
    success_url = reverse_lazy("core:all-questions")


class QuestionEditView(mxn.LoginRequiredMixin, genr.UpdateView):
    model = Question
    fields = ['title', 'question', 'related_tag']
    template_name = 'core/question_update_form.html'


class AnswerEditView(mxn.LoginRequiredMixin, genr.UpdateView):
    model = Answer
    fields = ['answer', 'question']
    template_name = 'core/answer_update_form.html'


def question_search(request):
    query = request.GET.get('q')
    queryset = Question.objects.all()

    if query:
        queryset = queryset.filter(related_tag__icontains=query)

    return render(request, 'core/question_search.html', {'results': queryset})
