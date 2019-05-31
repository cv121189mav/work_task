from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Post, Like, Comment
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.decorators import login_required


class AuthView(View):
    def get(self, request):
        return render(request, 'authoriztion.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'authoriztion.html')


@login_required(login_url='/signup/')
def comment(request):
    article = Post.objects.get(id=request.POST['article_id'])
    cm = Comment.objects.create(user=request.user, text=request.POST['text'])
    article.comments.add(cm)
    article.save()
    return HttpResponseRedirect(f'/article/{article.id}/')

@login_required(login_url='/signup/')
def home(request):
    paginator = Paginator(Post.objects.all(), 2)
    content = paginator.get_page(request.GET.get('page'))

    # Get count activate likes for article
    for i, item in enumerate(content):
        item.count = item.likes.filter(available=True).count()
        try:
            like = item.likes.get(user=request.user)
            user_like = like.available
        except Like.DoesNotExist:
            user_like = False

        item.user_like = user_like
    return render(request, 'blog.html', {
        'content': content,
    })

@login_required(login_url='/signup/')
def detail_article(request, pk):
    article = Post.objects.get(id=pk)

    paginator = Paginator(article.comments.all(), 2)
    content = paginator.get_page(request.GET.get('page'))

    return render(request, 'detail_article.html', {
        'article': article,
        'content': content
    })

@login_required()
def like(request, pk):
    if request.user.is_authenticated:
        article = Post.objects.get(id=pk)
        like = article.likes.filter(user=request.user).first()

        if like:
            like.available = not like.available
            like.save()
            count = article.likes.filter(available=True).count()

            return JsonResponse({
                'success': True,
                'like': like.available,
                'count': count
            })
        else:
            like = Like.objects.create(user=request.user, available=True)
            article.likes.add(like)
            article.save()

            count = article.likes.filter(available=True).count()

            return JsonResponse({
                'success': True,
                'like': like.available,
                'count': count
            })

    return JsonResponse({'success': False})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('includes/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
