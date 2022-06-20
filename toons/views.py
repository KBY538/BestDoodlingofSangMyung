from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView

from doodling.settings import MEDIA_ROOT, BASE_DIR
from wiki.models import Post
from .forms import UploadToonForm, UpdateToonForm, CommentForm
from .models import Toon, Category, Work, ToonImage

from psd_tools import PSDImage
from urllib.parse import unquote

# Create your views here.


class WorkList(ListView):
    model = Work
    ordering = '-pk'

    # get_context_data 오버라이드
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkList, self).get_context_data() # 이미 있는 애들 포함

        # 추가적으로 넘겨주고 싶은 context가 있을 때 많이 쓰는 패턴

        context['categories'] = Category.objects.all() # 모든 카테고리의 목록 싹다
        # 특정 필터의 object의 값들만 가져옴
        context['no_category_toon_count'] = Work.objects.filter(category=None).count()
        # 카테고리가 None인 애들을 찾아서 목록을 가져온다. 필터로넣어줄 조건은 카테고리가 None일 것.
        #목록을 가져온 다음에 view단에서 len할 수도 있고 그냥 숫자만 넘겨주려고 count를 할 수도 있고

        return context # 이렇게 변경한 context를 넘겨줘야 context가 넘어간다. return 꼭 해줘야

class WorkCreate(LoginRequiredMixin, CreateView):
    model = Work
    fields = ['title', 'slug', 'rep_thumbnail', 'description', 'category', 'display']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(WorkCreate, self).form_valid(form)
        else:
            return redirect('/toon')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_toon_count'] = Work.objects.filter(category=None).count()
        return context

def show_toon_episodes(request, slug):
    work = Work.objects.get(slug=slug)
    toons = Toon.objects.filter(work=work)

    context = {
        'categories': Category.objects.all(),
        'no_category_toon_count': Work.objects.filter(category=None).count(),
        'work': work,
        'toons': toons
    }

    if Post.objects.filter(work=work):
        context['toonwiki_url'] = Post.objects.get(work=work).get_absolute_url()

    return render(request, 'toons/toon_list.html', context)

def show_toon_episode(request, slug, episode):
    work = Work.objects.get(slug=slug)
    toon = Toon.objects.get(episode=episode, work=work)
    url_list = []

    if ToonImage.objects.filter(toon=toon) and 'psd' in ToonImage.objects.filter(toon=toon)[0].images.url:

        toon_images_psd_list = ToonImage.objects.filter(toon=toon)

        for toon_images_psd in toon_images_psd_list:
            old_url = MEDIA_ROOT+unquote(toon_images_psd.images.url).replace('/media','')
            new_url = old_url[:-4]+'.png'
            PSDImage.load(unquote(old_url)).as_PIL().save(new_url)

            new_url = new_url.replace(BASE_DIR, '')
            new_url = new_url.replace('\_', '/')
            url_list.append(new_url)

    else:
        for toon_images in ToonImage.objects.filter(toon=toon):
            url_list.append(toon_images.images.url)

    context = {
        'categories': Category.objects.all(),
        'no_category_toon_count': Work.objects.filter(category=None).count(),
        'work': work,
        'toon': toon,
        'toon_images': url_list,
        'toon_length': range(1, len(url_list)+2),
        'first': Toon.objects.filter(work=work).order_by('episode').first().episode,
        'last': Toon.objects.filter(work=work).order_by('episode').last().episode,
        'comment_form': CommentForm
    }
    if work.get_display_type() == '컷툰':
        return render(request, 'toons/toon_detail_cut.html', context)
    else:
        return render(request, 'toons/toon_detail_scroll.html', context)

def show_toon_category(request, slug):

    if slug=='no-category':
        category = '미분류'
        work_list = Work.objects.filter(category=None)

    else:
        category = Category.objects.get(slug=slug)
        work_list = Work.objects.filter(category=category)

    context = {
        'categories': Category.objects.all(),
        'no_category_toon_count': Work.objects.filter(category=None).count(),
        'category': category,
        'work_list': work_list
    }
    return render(request, 'toons/work_list.html', context)

def toon_create(request, slug):

    work = Work.objects.get(slug=slug)

    if request.method == 'GET':
        form = UploadToonForm()
        context = {
            'categories': Category.objects.all(),
            'no_category_toon_count': Work.objects.filter(category=None).count(),
            'work': work,
            'form': form
        }
        return render(request, 'toons/toon_form.html', context)

    elif request.method == 'POST':
        form = UploadToonForm(request.POST, request.FILES)
        if form.is_valid():
            toon = form.save(commit=False)
            toon.work = work
            toon.save()
            for afile in request.FILES.getlist("files"):
                toon_image = ToonImage()
                toon_image.toon = toon
                toon_image.images = afile
                toon_image.save()

            return redirect(work.get_absolute_url())
        else:
            raise PermissionDenied


def toon_update(request, slug, episode):
    work = Work.objects.get(slug=slug)
    toon = get_object_or_404(Toon, work=work, episode=episode)

    if request.method == 'GET':
        form = UpdateToonForm(instance=toon)
        context = {
            'categories': Category.objects.all(),
            'no_category_toon_count': Work.objects.filter(category=None).count(),
            'form': form
        }
        return render(request, 'toons/toon_form.html', context)

    elif request.method == 'POST':
        old_toon = Toon.objects.get(work=work, episode=episode)

        if request.POST['hook'] is not '' and 'thumbnail' in request.POST.keys():
            old_toon.hook = request.POST['hook']
            old_toon.save()

            return redirect(work.get_absolute_url())

        if request.FILES['thumbnail']:
            form = UpdateToonForm(request.POST, request.FILES, instance=old_toon)
            form.save()

        return redirect(work.get_absolute_url())

def add_comment(request, slug, episode):
    if request.user.is_authenticated:
        work = Work.objects.get(slug=slug)
        toon = get_object_or_404(Toon, work=work, episode=episode)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False) # False를 하면 바로 DB로 넘기지 않게 한다.
                # comment에 빠져있는 부분 채우기
                comment.toon = toon
                comment.author = request.user
                comment.save() # 커멘트를 DB에 보낸다.
                return redirect(comment.get_absolute_url()) # 원글로 돌려보내기
            else:
                return redirect(toon.get_absolute_url())
        else:
            raise PermissionDenied