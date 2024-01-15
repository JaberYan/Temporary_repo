from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import logout,login
from post.models import PostModel






def home(request):
    data = PostModel.objects.all()
    return render(request, 'home.html',{'posts':data})


def signupview(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                print(user)
                token = default_token_generator.make_token(user)
                print('token : ',token)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                print('uid : ',uid)
                confirm_link = f"http://127.0.0.1:8000/active/{uid}/{token}/"
                email_subject = "Confirm Email"
                email_body = render_to_string('confirm_mail.html',{'confirm_link':confirm_link})
                
                email = EmailMultiAlternatives(email_subject,'',to=[user.email])
                email.attach_alternative(email_body,'text/html')
                email.send()
                
                
                messages.success(request,'Account Create Successfully, Check Your Account Activate Mail')
                return redirect('homepage')
        else:
            form = UserRegistrationForm()
        return render(request,'sign_up.html',{'form':form})
    else:
        return redirect('homepage')
   
   
    
    
def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
        
    except(User.DoesNotExist):
        user = None
        
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    return redirect('signup')
    




class UserLoginView(LoginView):
    template_name = 'log_in.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    
    
    def form_valid(self,form):
        messages.success(self.request,'Login Successfully. Welcome Back!')
        return super().form_valid(form)
    



def logoutview(request):
    logout(request)
    messages.info(request, 'Logout Successfully')
    return redirect('homepage')



class UserAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully updated')
            return redirect('profile')  # Redirect to the user's profile page
        else:
            messages.error(request,'Error updating profile')
        return render(request, self.template_name, {'form': form})


    

    