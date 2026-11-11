from django.contrib import admin
from .models import ResumeFact, ResumeIndex, ResumePortfolio, ResumeService, ResumeSkill,Resume,ResumeCategory, ResumeSocialLink, ResumeTestimonial,ContactMessage
# Register your models here.
#test
admin.site.register(ResumeCategory)
admin.site.register(ContactMessage)
admin.site.register(ResumeSkill)
admin.site.register(Resume)
admin.site.register(ResumeFact)
admin.site.register(ResumeIndex)
admin.site.register(ResumePortfolio)
admin.site.register(ResumeService)
admin.site.register(ResumeTestimonial)
admin.site.register(ResumeSocialLink)



