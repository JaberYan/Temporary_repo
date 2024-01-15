from django.shortcuts import render, redirect
from .models import PostModel, LikeDislikeModel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import AddPostForm, CommentForm
from django.contrib import messages
from django.views.generic import DetailView





# Create your views here.
@login_required
def likeview(request,id,user_id):
    # post = PostModel.objects.get(id=id)
    # post.like += 1 
    # post.save()
    # return redirect('homepage')
    post_cl = PostModel.objects.get(id=id)
    user_cl = User.objects.get(id=user_id) 
    login_user = User.objects.get(id=request.user.id)
    if LikeDislikeModel.objects.filter(post=post_cl,user=user_cl).exists():
        existLikeModel = LikeDislikeModel.objects.get(post=id,user=user_cl)
        
        if existLikeModel.like == 0:
            existLikeModel.limit_decrease = False
            existLikeModel.like = existLikeModel.like+1
            existLikeModel.save()
            return redirect('homepage')
        else:
            if existLikeModel.limit_decrease == False:
                existLikeModel.like = existLikeModel.like-1
                existLikeModel.limit_decrease = True
                existLikeModel.save()
                return redirect('homepage')
    
    elif not LikeDislikeModel.objects.filter(post=post_cl,user=user_cl).exists() and LikeDislikeModel.objects.filter(post=post_cl).exists():
        pass                                                                                                                  
    
    else:
        likeOnePost=LikeDislikeModel.objects.create(
            user = user_cl,
            post = post_cl,
            like = 1,
            dislike = 0
        )
        likeOnePost.save()
        return redirect('homepage')
    # if count == 1 and user == track_user and post == track_post:
    #     post.like -= 1 
    #     post.save()
    #     print('if : ',count)
    #     return redirect('homepage')
    
    # elif count == 0 and user != track_user and post != track_post:
    #     post.like += 1
    #     count += 1
    #     track_post = post
    #     track_user = user
    #     print('elif : ',count)
    #     post.save()
    #     return redirect('homepage')


@login_required
def dislikeview(request,id,user_id):
    post = PostModel.objects.get(id=id)
    post.dislike += 1 
    post.save()
    return redirect('homepage')
    # if count == 1 and user == track_user and post == track_post:
    #     post.dislike -= 1 
    #     post.save()
    #     print('if : ',count)
    #     return redirect('homepage')
    
    # elif count == 0 and user != track_user and post != track_post:
    #     post.dislike += 1
    #     count += 1
    #     track_post = post
    #     track_user = user
    #     print('elif : ',count)
    #     post.save()
    #     return redirect('homepage')
    
    
@login_required
def dashboardview(request):
    return render(request, 'dashboard.html')


def user_post(request,user_id):
    user = User.objects.get(id=user_id)
    data = PostModel.objects.filter(user=user)
    # print(user.username)
    return render(request,'user_post.html',{'posts':data})



@login_required
def addpostview(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST,request.FILES)
        if form.is_valid():
            caption = form.cleaned_data['caption']
            print(caption)
            messages.success(request,'Post Added Successfully')
            form.save()
            return redirect('homepage')
        else:
            print(form.errors)
            messages.error(request,'Nope Make a error when your add post plz solve this error')
    else:
        form = AddPostForm()
    return render(request,'add_post.html',{'form':form})


class DetailViewOfPost(DetailView):
    model = PostModel
    pk_url_kwarg = 'pk'
    template_name = 'post_detail.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()
        comment_form = CommentForm()
        # print(self.pk_url_kwarg)

        context['comments'] = comments
        context['comment_form'] = comment_form
        return context