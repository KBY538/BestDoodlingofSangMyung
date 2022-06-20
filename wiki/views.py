from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404  # 템플릿을 클라이언트에 뿌려주는 흔히 쓰는 함수
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from toons.models import Work, Category
from .models import Post

# Create your views here.


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView): # Mixin이 로그인 안 된 사람을 로그인 페이지로 보냄
    model = Post
    fields = ['title', 'work', 'content']

    def test_func(self): # 뷰에 접근할 때 테스트
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form): # 데이터 보낼 때, 폼에서 포스트할 때, 한 번 더 검증(get 통한 건 처리못함)
        current_user = self.request.user # 리퀘스트 안에 들어 있는 유저 정보 가져오기

        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user # author 자리에 집어 넣는다.
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/wiki/') # 권한 없으면

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post # post 모델에 대해서 업데이트
    fields = ['title', 'work', 'content'] # 어떤 값들이 업데이트 가능?
    template_name = 'wiki/post_form_update.html'

    def dispatch(self, request, *args, **kwargs): # GET으로 들어오든 POST로 들어오든 뷰에 접근할 때 처리
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data() # 이미 있는 애들 포함

        # 추가적으로 넘겨주고 싶은 context가 있을 때 많이 쓰는 패턴

        context['categories'] = Category.objects.all() # 모든 카테고리의 목록 싹다
        context['no_category_post_count'] = Work.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Work.objects.filter(category=None).count()
        return context
