from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from . import views
import login
app_name = "main_page"
urlpatterns = [
    path('mainpage', views.index, name="index"),
    path('profile_page/<username>', views.profile_page, name="profile_page"),
    path('like_post', views.like_post, name="like_post"),
    path('comment_post_pros', views.comment_post_pros, name="comment_post_pros"),
    path('like_comment', views.like_comment, name="like_comment"),
    path('send_friend_request', views.send_friend_request, name="send_friend_request"),
    path('accept_friend_request', views.accept_friend_request, name="accept_friend_request"),
    path('report_post_ajax', views.report_post_ajax, name="report_post_ajax"),
    path('report_comment', views.report_comment, name="report_comment"),
    path('delete_post', views.delete_post, name="delete_post"),
    path('delete_comments', views.delete_comments, name="delete_comments"),
    path('photo/<picture_id>', views.picture_page, name="picture_page"),
    path('search_friends', views.search_friends, name="search_friends"),
    path('remove_friend', views.remove_friend, name="remove_friend"),
    path('settings', views.settings_page, name="settings"),
    path('comment_reply_pros', views.comment_reply_pros, name="comment_reply_pros"),
    path('load_comments', views.load_comments, name="load_comments"), 
    path('load_all_comments', views.load_all_comments, name="load_all_comments"),
    path('load_post', views.load_post, name="load_post"),
    path('load_more_post', views.load_more_post, name="load_more_post"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

