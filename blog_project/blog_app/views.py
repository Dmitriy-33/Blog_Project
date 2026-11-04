from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)
from .forms import CommentForm, PostForm
from .models import Post


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.author == self.request.user


class PostListView(ListView):
    model = Post
    template_name = "blog_app/post_list.html"
    context_object_name = "posts"
    paginate_by = 10


    def get_queryset(self):
        return Post.published.select_related("author")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog_app/post_detail.html"


    def get_queryset(self):
        qs = Post.objects.select_related("author")
        if self.request.user.is_authenticated:
            return qs
        return Post.published.select_related("author")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(is_approved=True)
        context["comment_form"] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog_app/post_form.html"


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog_app/post_form.html"


class PostDeleteView(AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "blog_app/post_confirm_delete.html"
    success_url = "/"


def add_comment(request, year, month, slug):
    post = get_object_or_404(Post, created__year=year, created__month=month, slug=slug)
    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.name = request.user.get_username()
            comment.email = request.user.email or "no-reply@example.com"
            comment.save()
    return redirect(post.get_absolute_url())
