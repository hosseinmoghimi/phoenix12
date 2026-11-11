from phoenix.server_settings import ADMIN_URL
from .apps import APP_NAME


class AdminUtility():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        self.class_name = None
        self.app_name = APP_NAME
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'class_name' in kwargs:
            self.class_name = kwargs['class_name']
        if 'user' in kwargs:
            self.user = kwargs['user']
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']

    def get_add_skill_btn(self):
        return self.get_add_btn(class_name='resumeskill')
    def get_add_skill_link(self):
        return self.get_add_link(class_name='resumeskill')

    def get_add_resume_btn(self):
        return self.get_add_btn(class_name='resume')
    def get_add_resume_link(self):
        return self.get_add_link(class_name='resume')

    def get_add_service_btn(self):
        return self.get_add_btn(class_name='resumeservice')
    def get_add_service_link(self):
        return self.get_add_link(class_name='resumeservice')

    def get_add_resumecategory_btn(self):
        return self.get_add_btn(class_name='resumecategory')
    def get_add_resumecategory_link(self):
        return self.get_add_link(class_name='resumecategory')

    def get_add_resumecategory_link(self):
        return self.get_add_link(class_name='resumecategory')

    def get_add_fact_btn(self):
        return self.get_add_btn(class_name='resumefact')
    def get_add_portfolio_link(self):
        return self.get_add_link(class_name='resumeportfolio')

    def get_add_fact_link(self):
        return self.get_add_link(class_name='resumefact')

        
    def get_add_social_link_btn(self):
        return self.get_add_btn(class_name='resumesociallink')
    def get_add_social_link_link(self):
        return self.get_add_link(class_name='resumesociallink')

    def get_add_testimonial_btn(self):
        return self.get_add_btn(class_name='resumetestimonial')
    def get_add_testimonial_link(self):
        return self.get_add_link(class_name='resumetestimonial')

    
    
    
    def get_add_link(self, *args, **kwargs):
        if 'class_name' in kwargs:
            self.class_name = kwargs['class_name']
        if self.class_name is not None or self.app_name is not None and self.user.has_perm(APP_NAME+".add_"+self.class_name):
            url = f"""{ADMIN_URL}{self.app_name}/{self.class_name}/add/"""
            return url
        return ""


    def get_add_btn(self, *args, **kwargs):
        if 'class_name' in kwargs:
            self.class_name = kwargs['class_name']

        if self.class_name is not None or self.app_name is not None and self.user.has_perm(APP_NAME+".add_"+self.class_name):
            url = f"""{ADMIN_URL}{self.app_name}/{self.class_name}/add/"""
            return f"""
                <div class="text-center">
                    <a target="_blank" href="{url}">
                        <i class="material-icons">add</i>
                    </a>
                </div>
            """
        return ""