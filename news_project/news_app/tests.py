from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post Title',
            content='This is the test content for the post.',
            author=self.user,
            publication_date=timezone.now()
        )

    def test_post_creation(self):
        """Test that a Post instance is created correctly."""
        self.assertEqual(self.post.title, 'Test Post Title')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(str(self.post), 'Test Post Title')

    def test_post_ordering(self):
        """Test that posts are ordered by publication_date descending."""
        post2 = Post.objects.create(
            title='Another Post',
            content='More content.',
            author=self.user,
            publication_date=timezone.now() + timezone.timedelta(days=1) # Published later
        )
        post3 = Post.objects.create(
            title='Older Post',
            content='Old content.',
            author=self.user,
            publication_date=timezone.now() - timezone.timedelta(days=1) # Published earlier
        )
        posts = Post.objects.all()
        self.assertEqual(posts[0], post2) # Newest post first
        self.assertEqual(posts[1], self.post)
        self.assertEqual(posts[2], post3) # Oldest post last

class NewsAppViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post1 = Post.objects.create(
            title='First Test Post',
            content='Content for first post.',
            author=self.user,
            publication_date=timezone.now()
        )
        self.post2 = Post.objects.create(
            title='Second Test Post',
            content='Content for second post.',
            author=self.user,
            publication_date=timezone.now() - timezone.timedelta(hours=1)
        )

    def test_post_list_view_status_code(self):
        """Test the post list view returns a 200 OK status."""
        response = self.client.get(reverse('news_app:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_uses_correct_template(self):
        """Test the post list view uses the correct template."""
        response = self.client.get(reverse('news_app:post_list'))
        self.assertTemplateUsed(response, 'news_app/post_list.html')
        self.assertTemplateUsed(response, 'news_app/base.html')

    def test_post_list_view_displays_posts(self):
        """Test that the post list view displays posts."""
        response = self.client.get(reverse('news_app:post_list'))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)

    def test_post_detail_view_status_code(self):
        """Test the post detail view returns a 200 OK status for an existing post."""
        response = self.client.get(reverse('news_app:post_detail', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_status_code_for_nonexistent_post(self):
        """Test the post detail view returns a 404 for a non-existent post."""
        non_existent_pk = self.post1.pk + 999
        response = self.client.get(reverse('news_app:post_detail', args=[non_existent_pk]))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_uses_correct_template(self):
        """Test the post detail view uses the correct template."""
        response = self.client.get(reverse('news_app:post_detail', args=[self.post1.pk]))
        self.assertTemplateUsed(response, 'news_app/post_detail.html')
        self.assertTemplateUsed(response, 'news_app/base.html')

    def test_post_detail_view_displays_post_content(self):
        """Test that the post detail view displays the post's content."""
        response = self.client.get(reverse('news_app:post_detail', args=[self.post1.pk]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.content)
        self.assertContains(response, self.user.username)

    def test_home_redirects_to_post_list(self):
        """
        Although not explicitly defined, if a root path for the app ('/news/') is hit,
        it should serve the post_list.
        """
        response = self.client.get('/news/') # Assuming '/news/' is the base for news_app urls
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_app/post_list.html')
