from django.contrib import admin
from .models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count


#Custom Form Ckeditor
class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'

#Nhúng Form Lesson vào Course Quan hệ n-n
class LessonTagInlineAdmin(admin.StackedInline):
    model = Lesson.tags.through

#Custom Admin
class LessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("/static/css/main.css",)
        }
    form = LessonForm
    list_display = ["id" , "subject", "created_date", "active", "course"]
    search_fields = ["subject", "created_date" , "course__subject"]
    list_filter = ["subject" , "course__subject"]
    readonly_fields = ['avatar']
    inlines = (LessonTagInlineAdmin,)
    
    def avatar(seft , lesson):
        return mark_safe('''
              <img src="/static/{image_url}" width="100" height="100" />
            '''.format(image_url=lesson.image.name , alt=lesson.subject))

#Nhúng Form Lesson vào Course Quan hệ 1-n
class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    pk_name = 'course'

class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonInlineAdmin, )

#Custom Admin Site , thêm trang thống kê
class CourseAppAdminSite(admin.AdminSite):
    site_header = "E-Courses"
    
    def get_urls(self):
        return[
          path('course-stats/' , self.course_stats)
        ] + super().get_urls()

    def course_stats(seft,request):
        course_count = Course.objects.count()
        stats = Course.objects.annotate(lesson_count = Count('lessons')).values('id' , 'subject' , 'lesson_count')

        return TemplateResponse(request , 'admin/course-stats.html' 
                                , {'course_count':course_count , 'stats':stats})
    
admin_site = CourseAppAdminSite("myadmin")

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Course , CourseAdmin)
# admin.site.register(Lesson , LessonAdmin)

admin_site.register(Category)
admin_site.register(Course , CourseAdmin)
admin_site.register(Lesson , LessonAdmin)
