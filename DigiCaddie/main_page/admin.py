from django.contrib import admin
from django.utils.html import mark_safe
from .models import ReportComment, ReportedComment, ReportedPost, userpost, comments_post, user_information, user_friends, friend_request_model, report_post, comments_replies

class userpostadmin(admin.ModelAdmin):
    list_display = ["author", "posted_date", "rating", "caption", "picture", "image_view"]



# class report_comment(admin.ModelAdmin):
#     list_display = ['post', 'user']
#     readonly_fields = ['text', 'author']

#     def text(self, obj):
#         return obj.post.text

#     def author(self, obj):
#         return obj.post.author
# link reports to the post
class report_post_admin(admin.ModelAdmin):
    list_display = ['post', 'user']
    readonly_fields = ['author', 'picture', 'caption']

    def caption(self, obj):
        return obj.post.caption

    def author(self, obj):
        return obj.post.author
    
    def picture(self, obj):
        return mark_safe(f'<img src = "{obj.post.picture.url}" width = "300"/>')
        
class ReportPostInline(admin.TabularInline):
    model = report_post
    extra = 0

class ReportedPostAdmin(admin.ModelAdmin):
    list_display = ['post', 'date']
    readonly_fields = ['post', 'date']
    #inlines = [ReportPostInline]

    def post(self, obj):
        return obj.post.caption

    def date(self, obj):
        return obj.date
    
class ReportedCommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'date']
    readonly_fields = ['comment', 'date']

    def comment(self, obj):
        return obj.comment.text

    def date(self, obj):
        return obj.date

class ReportCommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'user', 'date']
    readonly_fields = ['comment', 'user', 'date']



admin.site.register(userpost, userpostadmin)
admin.site.register(comments_post)
admin.site.register(comments_replies)
admin.site.register(user_information)
admin.site.register(user_friends)
admin.site.register(friend_request_model)
admin.site.register(report_post, report_post_admin)
admin.site.register(ReportedPost, ReportedPostAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)
admin.site.register(ReportedComment, ReportedCommentAdmin)