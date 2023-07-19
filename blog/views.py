from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post


# Create your views here.

def post_list(request):
	post_list = Post.published.all()
	# 페이지당 3개의 게시물로
	paginator = Paginator(post_list, 5)
	page_number = request.GET.get('page', 1)
	try:
		posts = paginator.page(page_number)
	except EmptyPage:
		# page_number가 범위를 벗어난 경우 결과릐 마지막 페이지 제공
		posts = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		# page_number가 정수가 아닌 경우 첫번째 페이지 제공
		posts = paginator.page(1)
	return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
	post = get_object_or_404(
		Post,
		status=Post.Status.PUBLISHED,
		slug=post,
		publish__year=year,
		publish__month=month,
		publish__day=day,
	)
	return render(request, 'blog/post/detail.html', {'post': post})


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 5
	template_name = 'blog/post/list.html'

