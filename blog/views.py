from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .models import Blog, Tag, Comment, Like
from .forms import CommentForm 
from django.core.paginator import Paginator

from django.db import connection
from django.core.mail import send_mail
from django.conf import settings

from .forms import ShareByEmailForm

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        queryset = Blog.objects.order_by('-created_at')
        query = self.request.GET.get('q')
        
        if query:
            # Search in title, content, and tags
            queryset = queryset.filter(
                title__icontains=query
            ) | queryset.filter(
                content__icontains=query
            ) | queryset.filter(
                tags__name__icontains=query
            )
        
        return queryset.distinct()  # Ensure distinct results


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'  
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        context['comment_form'] = CommentForm()  
        return context

class BlogShareView(View):
    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        return render(request, 'blog/share_blog.html', {'blog': blog})

    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        email = request.POST.get('email')
        message = request.POST.get('message', '')

        # Validate the email address (basic validation)
        if not email or '@' not in email:
            return render(request, 'blog/share_blog.html', {
                'blog': blog,
                'error': 'Please enter a valid email address.'
            })

        # Prepare email content
        subject = f"Check out this blog: {blog.title}"
        body = f"""
        Hi,

        I thought you might be interested in this blog: "{blog.title}".

        {blog.content}

        Personal message from {request.user.username}:
        {message}

        You can read more about it here: {request.build_absolute_uri(blog.get_absolute_url())}
        """

        # Send the email
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('blog_list')  # Redirect to a success page or blog list
        except Exception as e:
            return render(request, 'blog/share_blog.html', {
                'blog': blog,
                'error': f'An error occurred while sending the email: {e}'
            })

def add_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('blog_detail', pk=pk)
    return redirect('blog_detail', pk=pk)


def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = Like.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()  
    return redirect('blog_detail', pk=comment.blog.pk)



def share_blog_by_email(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    
    if request.method == 'POST':
        form = ShareByEmailForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            message = form.cleaned_data['message']
            subject = f"Check out this blog: {blog.title}"
            body = f"Hi,\n\nI thought you might be interested in this blog post:\n\n{blog.title}\n\n{blog.content}\n\nMessage from the sender:\n{message}\n\nBest regards,\nYour Blog"
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient_email])
            return redirect('blog_detail', blog_id=blog.id)  # Redirect to the blog detail page
    
    else:
        form = ShareByEmailForm()
    
    return render(request, 'blog/share_by_email.html', {'form': form, 'blog': blog})
