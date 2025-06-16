from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Comment 

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='password123')

        # Створюємо пост з автором
        self.post = Post.objects.create(
            content="Test post",
            author=self.user
        )

    def test_index_displays_posts(self):
        """
        Перевіряє, що головна сторінка відображає існуючі пости.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test post")

    def test_unauthenticated_user_cannot_comment(self):
        """
        Перевіряє, що неавторизований користувач не може залишити коментар.
        """
        response = self.client.post(reverse('index'), {
            'post_id': self.post.id,
            'comment_content': 'Unauth comment',
        })
        self.assertRedirects(response, reverse('login'))

    def test_authenticated_user_can_comment(self):
        """
        Перевіряє, що авторизований користувач може залишити коментар до поста.
        """
        self.client.login(username='tester', password='password123')
        response = self.client.post(reverse('index'), {
            'post_id': self.post.id,
            'comment_content': 'This is a comment',
        })
        self.assertRedirects(response, reverse('index'))

        # Перевірка, що коментар створено
        self.assertTrue(Comment.objects.filter(
            post=self.post,
            author=self.user,
            content='This is a comment'
        ).exists())
