from django.shortcuts import render, redirect
from django.template import loader
# from django import forms
from .models import *
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
import random
import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.conf import settings

# Create your views here.
def post_list(request):
    context = {'somestuff'}
    context = [1,2,3]
    return render(request, 'myapp/post_list.html', {'context':context})

def success(request):
    return render(request, 'myapp/success.html')

def llogin(request):
    return render(request, 'myapp/login.html')

def dologin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('success')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')

def signup(request):
    return render(request, 'myapp/signup.html')

def dosignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name'] # 사실은 전체 이름
        email = request.POST['email']
        password = request.POST['password']
        is_owner = request.POST.get('is_owner', False)
        print(is_owner)

        # new_user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, is_owner=is_owner)
        new_user = UserInfo(username=username, first_name=first_name, email=email, is_owner=is_owner)
        new_user.set_password(password)
        new_user.is_active = False
        new_user.last_name = randstr(50)
            
        print("회원가입을 합니다.")

        mail = EmailMessage('BobView 사용자 인증', '안녕하세요 BobView입니다.\n사용자 인증은 위해서 아래 링크에 접속하시기 바랍니다.\n감사합니다.\n\n' 
                                                    + 'http://127.0.0.1:8000/active/' + new_user.last_name, to=[email])
        mail.content_subtype = "html"
        mail.send()

        message = new_user.first_name + "님께서 입력하신 메일로 인증 링크를 발송했습니다."

        new_user.save()
        
    return redirect('login')

def randstr(length):
    rstr = "0123456789abcdefghijklnmopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ"
    rstr_len = len(rstr) - 1
    result = ""
    for i in range(length):
        result += rstr[random.randint(0, rstr_len)]
    return result

def user_active(request, token):
    user = get_object_or_404(UserInfo, last_name=token)
    if user.date_joined < timezone.now() - datetime.timedelta(days=7): # 일주일 지나면 만료
        user.delete()
        message = "만료된 링크입니다. 다시 가입을 신청하세요."
    else:
        user.is_active = True
        user.last_name = ''
        user.save()
        message = "이메일이 인증되었습니다."
    return render(request, 'myapp/success.html', {'message':message })


def mypage(request):
    pass

def rest_image_regi(request):
    pass

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        current_user = request.user
        rest_info = get_object_or_404(RestaurantInfo, owner=current_user.id)
        myfile = request.FILES['myfile']
        print(myfile.name)
        print(myfile)
        rest_info.restaurant_image = myfile.name

        fs = FileSystemStorage()
        uploaded_file_url = fs.url(filename)

        rest_info.save()
        filename = fs.save(myfile.name, myfile)
        return render(request, 'myapp/restaurant.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return HttpResponse('파일 업로드 실패. 다시 시도 해보세요.')

# class UserRegistrationView(CreateView):
#     model = get_user_model()
#     form_class = UserRegistrationForm
#     success_url = '/user/login/'
#     verify_url = '/user/verify/'
#     token_generator = default_token_generator

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         if form.instance:
#             self.send_verification_email(form.instance)
#         return response

#     def send_verification_email(self, user):
#         token = self.token_generator.make_token(user)
#         user.email_user('회원가입을 축하드립니다.', '다음 주소로 이동하셔서 인증하세요. {}'.format(self.build_verification_link(user, token)), from_email=settings.EMAIL_HOST_USER)
#         messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')

#     def build_verification_link(self, user, token):
#         return '{}/user/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)

# class UserVerificationView(TemplateView):

#     model = get_user_model()
#     redirect_url = '/user/login/'
#     token_generator = default_token_generator

#     def get(self, request, *args, **kwargs):
#         if self.is_valid_token(**kwargs):
#             messages.info(request, '인증이 완료되었습니다.')
#         else:
#             messages.error(request, '인증이 실패되었습니다.')
#         return HttpResponseRedirect(self.redirect_url)   # 인증 성공여부와 상관없이 무조건 로그인 페이지로 이동

#     def is_valid_token(self, **kwargs):
#         pk = kwargs.get('pk')
#         token = kwargs.get('tonen')
#         user = self.model.objects.get(pk=pk)
#         is_valid = self.token_generator.check_token(user, token)
#         if is_valid:
#             user.is_active = True
#             user.save()     # 데이터가 변경되면 반드시 save() 메소드 호출
#         return is_valid