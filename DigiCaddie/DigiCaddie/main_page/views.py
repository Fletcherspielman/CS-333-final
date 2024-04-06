from django.shortcuts import render, get_object_or_404 
from .models import ReportedComment, ReportedPost, userpost, user_information, comments_post, user_friends, friend_request_model, ReportComment, report_post
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import image_fourms, user_profile_pic_form, comment_form_post, update_profile, update_security, comment_form_reply
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login
import warnings
from main_page import aws_rekognition
from django.conf import settings

def index(request):
    liked = []
    # main feed form post
    if request.method == 'POST' and 'upload_image' in request.POST:
        form_post_image = image_fourms(request.POST, request.FILES)
        if form_post_image.is_valid():
            form = form_post_image.save(commit=False) # we need to add data for the class or an error will occur 
            form.author = request.user
            form.caption = form_post_image.cleaned_data["caption"]
            form.rating = 0 
            form.save()
            form_post_image = image_fourms()
            if settings.USE_S3: # check if the were in the aws server 
                post = userpost.objects.filter(author=request.user).latest('picture')
                check_rating = aws_rekognition.content_moderation(post.picture.url)
                if check_rating == False:
                    messages.add_message(request, messages.INFO, "Error the post that you have uploaded was demed inappropriate")
                    post.delete() 
            return HttpResponseRedirect("mainpage")
        else:
            messages.add_message(request, messages.INFO, "Error uploading image or bad caption please try again")
    else:
        # if no form was submitted then load the form
        form_post_image = image_fourms()  
    possible_friends = []
    users_friends = user_friends.objects.get(user=request.user)
    user_friend_request = friend_request_model.objects.filter(request=request.user)
    user_recived_request = friend_request_model.objects.filter(sent=request.user)
    # to look for users to add to recomendations we pull all users from the database
    # we will filter through this list to make sure we are not adding more users to the list that have already been giving a friend request or are already friends 
    for y in User.objects.all():
        if y != request.user and not users_friends.friends.contains(y) and not (user_friend_request.filter(sent=y).exists()) and not (user_recived_request.filter(request=y).exists()):
            possible_friends.append(y)
        if len(possible_friends) == 5:
            break
    context = {
        "form_post_image":form_post_image,
        "comment_form_post":comment_form_post,
        "comment_form_reply": comment_form_reply,
        "liked":liked,
        "possible_friends":possible_friends,
    }
    return render(request, "main_page/mainpage.html", context=context)

def load_post(request):
    post_to_load = []
    liked = []
    for x in userpost.objects.filter(active=True).order_by('-posted_date')[:5]:
        post_to_load.append(x)
        if x.likes.filter(id=request.user.id).exists():
            liked.append(x.id)
    context = {
        "post_to_load":post_to_load,
        "request":request,
        "liked":liked,
    }
    html = render_to_string('main_page/post.html', context)
    return JsonResponse({'html': html})


def load_more_post(request):
    post_to_load = []
    liked = []
    count = request.GET.get("count", None)
    count = int(count)
    for x in userpost.objects.filter(active=True).order_by('-posted_date')[count:count+5]:
        post_to_load.append(x)
        if x.likes.filter(id=request.user.id).exists():
            liked.append(x.id)
    if len(post_to_load) == 0:
        empty = True
    else:
        empty = False
    context = {
        "post_to_load":post_to_load,
        "request":request,
        "liked":liked,
    }
    html = render_to_string('main_page/post.html', context)
    return JsonResponse({'html': html, 'empty': empty})

def load_comments(request):
    if request.method == 'GET':
        post = request.GET.get("id_post", None)
        post = userpost.objects.get(id = post)
        comments_likes = []
        if post.comments.exists():
            for y in post.comments.all():
                if y.likes_comment.filter(id=request.user.id).exists():
                    comments_likes.append(y.id)
        context = {
            'photo': post,
            'comments_likes': comments_likes,
            "comment_form_reply": comment_form_reply,
            "request": request
        }
        html = render_to_string('main_page/comments.html', context)
        return JsonResponse({'html': html})
    
def load_all_comments(request):
    if request.method == 'GET':
        post = request.GET.get("id_post", None)
        post = userpost.objects.get(id = post)
        comments_likes = []
        if post.comments.exists():
            for y in post.comments.all():
                if y.likes_comment.filter(id=request.user.id).exists():
                    comments_likes.append(y.id)
        context = {
            'photo': post,
            'comments_likes': comments_likes
        }
        html = render_to_string('main_page/load_all_comments.html', context)
        return JsonResponse({'html': html})
    
def picture_page(request, picture_id): 
    # page just to load one picture for the user to look at
    photo = userpost.objects.get(id = picture_id)
    context = {
        "photo":photo,
    }
    return render(request, "main_page/picture_page.html" , context)

# inspired by https://medium.com/@nishalk25121999/how-to-make-a-like-button-using-django-ajax-d2db38e6d2f8
@csrf_protect  
def like_post(request): 
    # ajax post 
    # if the user likes a post then this will add to the likes without refreshing the page
    if request.method == 'POST':
        photoid = request.POST.get("content_id", None)
        picture = get_object_or_404(userpost, pk=photoid)
        if picture.likes.filter(id=request.user.id):
            picture.likes.remove(request.user) 
            liked=False
        else:
            picture.likes.add(request.user) 
            liked=True
        ctx={"likes_count":picture.like_total,"liked":liked,"content_id":photoid}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        warnings.warn("Error: Like_Post")

@csrf_protect      
def comment_post_pros(request):
    if request.method == "POST":
        post_id = request.POST.get("content_id", None)
        post_information = get_object_or_404(userpost, pk=post_id)
        comment = comment_form_post(request.POST)
        if comment.is_valid():
            test = comment.save(commit=False)
            test.text = comment.cleaned_data["text"]   
            test.post = post_information
            test.author = request.user
            test.save()
            post_information.comments.add(test)
            comment_id = test.id
            ctx={"comment":request.POST.get("text", None),"content_id":post_id, "author":request.user.username, "comment_id":comment_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        else:
            warnings.warn("Error: comment post form is not valid")
    else:
        warnings.warn("Error: comment post pros")
         
@csrf_protect      
def comment_reply_pros(request):
    # user comment processing 
    if request.method == "POST":
        post_id = request.POST.get("content_id", None)
        post_information = get_object_or_404(comments_post, pk=post_id)
        comment = comment_form_reply(request.POST)
        if comment.is_valid():
            test = comment.save(commit=False)
            test.text = comment.cleaned_data["text"]       
            test.post = post_information
            test.author = request.user
            test.save()
            post_information.comment_replies.add(test)
            comment_id = test.id
            ctx={"comment":request.POST.get("text", None),"content_id":post_id, "author":request.user.username, "comment_id":comment_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        else:
            warnings.warn("Error: comment post form is not valid")
    else:
        warnings.warn("Error: comment post pros")


@csrf_protect  
def like_comment(request): 
    # this is similar to like post just for comments
    if request.method == 'POST':
        commentid = request.POST.get("content_id", None)
        comment = get_object_or_404(comments_post, pk=commentid)
        if comment.likes_comment.filter(id=request.user.id):
            comment.likes_comment.remove(request.user) 
            liked=False
        else:
            comment.likes_comment.add(request.user) 
            liked=True
        ctx={"likes_count":comment.like_comment_total,"liked":liked,"content_id":commentid}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        warnings.warn("Error: Like_Post")

@csrf_protect  
def send_friend_request(request):
    # sending friend request ajax 
    # get both users and create a new friend request in the database
    if request.method == 'POST':
        user_id = request.user
        user_request_id = request.POST.get("user_id_sent", None)
        user = get_object_or_404(User, username=user_id)
        user_send_to = get_object_or_404(User, username=user_request_id)
        friend_request_model.objects.create(request=user, sent=user_send_to)
        ctx={"user_request_id":user_request_id}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        warnings.warn("Error: send friend request")

@csrf_protect  
def accept_friend_request(request):
    # accept friend request ajax post
    if request.method == 'POST':
        # get data from request and grab the users information
        # this will be accepted by the reciver 
        id_request = request.POST.get("id_accepted", None)
        id_friend = friend_request_model.objects.get(pk=id_request)
        acceptor = id_friend.sent
        sender = id_friend.request
        id_friend.delete()
        # add as friends 
        acceptor_friends = user_friends.objects.get(user=acceptor)
        acceptor_friends.friends.add(sender)
        sender_friends = user_friends.objects.get(user=sender)
        sender_friends.friends.add(acceptor)
        ctx={"done":1}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        warnings.warn("Error: accept friend request")

@csrf_protect  
def remove_friend(request):
    # accept friend request ajax post
    if request.method == 'POST':
        id_request = request.POST.get("friend", None)
        id_request = User.objects.get(username=id_request)
        user = request.user
        requester_friends = user_friends.objects.get(user = user)
        requester_friends.friends.remove(id_request)
        removed_friends = user_friends.objects.get(user = id_request)
        removed_friends.friends.remove(request.user)
        ctx={"done":1}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        warnings.warn("Error: Remove friend")

@csrf_protect  
def report_comment(request):
    # this will be sent to the admin page
    if request.method == 'POST':
        id_comment = request.POST.get("id_comment", None)
        post = comments_post.objects.get(id=id_comment)
        ReportComment.objects.create(user=request.user, comment=post)
        ctx={"done":1}
        reports = ReportComment.objects.filter(comment=post).count()

        if reports > 2:
            post.active = False
            post.save()
            ReportedComment.objects.create(comment=post)

        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        warnings.warn("Error: report comment")

@csrf_protect  
def report_post_ajax(request):
    # this will be sent to the admin page
    if request.method == 'POST':
        id_comment = request.POST.get("id_post", None)
        comment = userpost.objects.get(id=id_comment)
        report_post.objects.create(user = request.user, post=comment)
        ctx={"done":1}
        reports = report_post.objects.filter(post=comment).count()
        
        if reports > 2:
            comment.active = False
            comment.save()

            ReportedPost.objects.create(post=comment)

        return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        warnings.warn("Error: report post")

@csrf_protect  
def delete_post(request):
    # ajax request to delete a post.
    if request.method == 'POST':
        id_post = request.POST.get("id_post", None)
        post = userpost.objects.get(id=id_post)
        if request.user == post.author:
            post.delete()
            ctx={"done":1}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        else: 
            warnings.warn("Error: delete post user does not match requester")
    else:
        warnings.warn("Error: delete post")

@csrf_protect  
def delete_comments(request):
    # ajax request to delete a comment
    if request.method == 'POST':
        id_comment = request.POST.get("id_comment", None)
        post = comments_post.objects.get(id=id_comment)
        if request.user == post.author:
            post.delete()
            ctx={"done":1}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        else: 
            warnings.warn("Error: delete post user does not match requester")
    else:
        warnings.warn("Error: delete comment")

@csrf_protect  
def profile_page(request, username):
    # this will load as a "slug url" and we need to pass the username into the function call to load the users page
    # thier are protections in the template to make sure the users cant change other users information
    user = User.objects.get(username = username)
    post_to_load = []
    profile_pic = user_information.objects.filter(user=user)
    profile_pic_id = request.user.profile_pic
    # user profile picture form
    if request.method == 'POST' and 'upload_profile_pic' in request.POST:
        form_post_profile_pic = user_profile_pic_form(request.POST, request.FILES, instance=profile_pic_id)
        if form_post_profile_pic.is_valid():
            form_post_profile_pic.save()
            return HttpResponseRedirect(reverse("main_page:profile_page", kwargs={'username':request.user}))
    else:
        # load all pictures from the user and will be orderd by what has been posted most recently 
        for x in userpost.objects.filter(author=user).order_by('-posted_date'):
            post_to_load.append(x)
        form_post_profile_pic = user_profile_pic_form()
        # this is to get the rows loaded up correctly on the profile page template
        # how many rows are their gonna be 
        r = int(len(post_to_load)/3) + 1
        # how many post on each row
        c = 3
        # we need a remainder for the last row
        remainder = len(post_to_load)%3
        # set up the list for the pictures 
        load_pic_row_col = [[0 for x in range(c)] for y in range(r)] 
        # counter
        k = 0
        # add the post into the list
        for y in range(r):
            for z in range(c):
                if r - y - 1 == 0:
                    for j in range(remainder):
                        load_pic_row_col[y][j] = post_to_load[k]
                        k = k + 1
                    break
                else:
                    load_pic_row_col[y][z] = post_to_load[k]
                    k = k + 1
        # pervent an error by passing how many post are going to the main page
        error_post_to_load = len(post_to_load)
        # remove a row if thier are no remainders 
        if remainder == 0:
            range_loop = r - 1
        else:
            range_loop = r

        # if friend or has friend request
        show_friend_request = False
        if friend_request_model.objects.filter(request = request.user, sent=user).exists() or friend_request_model.objects.filter(request = user, sent= request.user).exists():
            show_friend_request = True

        context = {
            "name":user,
            "form_post_profile_pic":form_post_profile_pic,
            "profile_pic":profile_pic,
            "post_to_load":post_to_load,
            "rows":r - 1,
            "remainder":remainder,
            "rows_cols":load_pic_row_col,
            "rang_rows":range(range_loop),
            "error_post_to_load":error_post_to_load,
            "show":show_friend_request
        }
        return render(request, "main_page/profile_page.html", context=context)

@csrf_protect  
def search_friends(request):
    # ajax request to search for users
    if request.method == 'POST':
        list_users_array = []
        search_term = request.POST.get('person')
        list_users = User.objects.filter(username__contains=search_term)
        i=0
        # load users and get thier friends and friend request
        users_friends = user_friends.objects.get(user=request.user)
        user_friend_request = friend_request_model.objects.filter(request=request.user)
        user_recived_request = friend_request_model.objects.filter(sent=request.user)
        # if the user already has a friend request it will mark it and will show on the template
        for x in list_users:
            profile_picture_url = user_information.objects.get(user=x)
            if x == request.user or  users_friends.friends.contains(x) or (user_friend_request.filter(sent=x).exists()) or (user_recived_request.filter(request=x).exists()):
                list_users_array.append([x.id, x.username, profile_picture_url.user_profile_picture.url, 0])
            else:
                list_users_array.append([x.id, x.username, profile_picture_url.user_profile_picture.url, 1])
            i=i+1
            if i == 10:
                break
        # no user found     
        if len(list_users) == 0:
            ctx={"list_users":list_users_array, "empty": 1}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        else:
            ctx={"list_users":list_users_array, "empty": 0}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        warnings.warn("Error: Search friends")

def settings_page(request):
    # user profile picture form
    if request.method == 'POST':
        user = User.objects.get(username = request.user.username)
        if 'update_profile' in request.POST:
            up_profile = update_profile(request.POST)
            if up_profile.is_valid():
                first_name = up_profile.cleaned_data["firstname"]
                last_name = up_profile.cleaned_data["lastname"]
                email = up_profile.cleaned_data["email"]
                if len(first_name) != 0: 
                    user.first_name = first_name
                if len(last_name) != 0:
                    user.last_name = last_name
                if len(email) != 0: 
                    user.email = email
                user.save()
        elif 'update_security' in request.POST:
            up_sec = update_security(request.POST)
            if up_sec.is_valid():
                password = up_sec.cleaned_data["current_password"]
                if user.check_password(password):
                    new_password = up_sec.cleaned_data["new_password"]
                    new_password_confirmed = up_sec.cleaned_data["confirm_new_password"]
                    if new_password == new_password_confirmed:
                        user.set_password(new_password)
                        user.save()
                        login(request, user)
                    else: 
                        messages.add_message(request, messages.INFO, "Error Passwords do not match please try again!")
                else: 
                    messages.add_message(request, messages.INFO, "Error Incorrect password please try again!")
        elif 'update_picture_profile' in request.POST:
            update_profile_picture = user_profile_pic_form(request.POST, request.FILES, instance=request.user.profile_pic)
            if update_profile_picture.is_valid():
                update_profile_picture.save()
                if settings.USE_S3:
                    profile_pic = user_information.objects.filter(user=request.user).latest('user_profile_picture')
                    check_rating = aws_rekognition.content_moderation(profile_pic.user_profile_picture.url)
                    if check_rating == False:
                        messages.add_message(request, messages.INFO, "Error the profile picture that you have uploaded was demed inappropriate")
                        profile_pic.delete()
                        user_information.objects.create(user=request.user)
        elif 'update_privacy' in request.POST:
            pass
        else:
            warnings.warn("error with POST settings page")
        return HttpResponseRedirect("settings")
    else:
        
        return render(request, "main_page/settings.html")
