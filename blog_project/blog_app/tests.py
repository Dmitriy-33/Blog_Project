from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Comment, Post


def make_user(username="alice"):
    return User.objects.create_user(username, f"{username}@example.com", "S3cretPass!")


def make_post(user, status=Post.Status.PUBLISHED, title="Первый пост"):
    return Post.objects.create(title=title, body="Текст", author=user, status=status)


class PostModelTests(TestCase):
    def test_slug_auto_generated(self):
        post = make_post(make_user())
        self.assertEqual(post.slug, "первый-пост")


    def test_published_manager(self):
        user = make_user()
        published = make_post(user)
        make_post(user, status=Post.Status.DRAFT, title="Черновик")
        self.assertEqual(list(Post.published.all()), [published])


class PostViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other = make_user("bob")
        self.post = make_post(self.user)
        self.draft = make_post(self.user, status=Post.Status.DRAFT, title="Черновик")


    def get_detail_url(self, post):
        return reverse(
            "blog_app:post_detail",
            args=[post.created.year, post.created.month, post.slug],
        )


    def test_list_shows_only_published(self):
        response = self.client.get(reverse("blog_app:post_list"))
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, self.draft.title)


    def test_detail_published_accessible(self):
        response = self.client.get(self.get_detail_url(self.post))
        self.assertContains(response, self.post.body)


    def test_draft_hidden_from_anonymous(self):
        response = self.client.get(self.get_detail_url(self.draft))
        self.assertEqual(response.status_code, 404)


    def test_create_requires_login(self):
        response = self.client.get(reverse("blog_app:post_create"))
        self.assertEqual(response.status_code, 302)


    def test_create_sets_author(self):
        self.client.login(username="alice", password="S3cretPass!")
        response = self.client.post(
            reverse("blog_app:post_create"),
            {"title": "Новый", "body": "Тело", "status": "published"},
        )
        post = Post.objects.get(title="Новый")
        self.assertEqual(post.author, self.user)
        self.assertEqual(response.status_code, 302)


    def test_only_author_can_edit(self):
        other_user = User.objects.create_user(username="other", password="pass")
        self.client.force_login(other_user)
        url = reverse("blog_app:post_update", args=[
            self.post.created.year,
            self.post.created.month,
            self.post.slug,
        ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class CommentTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.post = make_post(self.user)
        self.url = reverse(
            "blog_app:add_comment",
            args=[self.post.created.year, self.post.created.month, self.post.slug],
        )


    def test_anonymous_cannot_comment(self):
        response = self.client.post(self.url, {"name": "x", "email": "x@x.com", "body": "Спам"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)


    def test_authenticated_user_can_comment(self):
        self.client.force_login(self.user)
        url = reverse("blog_app:add_comment", args=[self.post.created.year, self.post.created.month, self.post.slug])
        response = self.client.post(url, {
            "body": "Отличный пост!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, body="Отличный пост!").exists())


    def test_unapproved_hidden(self):
        Comment.objects.create(post=self.post, name="Гость", email="g@g.com", body="Тест", is_approved=False)
        self.client.login(username="alice", password="S3cretPass!")
        response = self.client.get(self.get_detail_url(self.post)) if False else self.client.get(
            reverse("blog_app:post_detail", args=[self.post.created.year, self.post.created.month, self.post.slug])
        )
        self.assertNotContains(response, "Тест")


    def get_detail_url(self, post):
        return reverse("blog_app:post_detail", args=[post.created.year, post.created.month, post.slug])
