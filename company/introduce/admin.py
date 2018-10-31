from django.contrib import admin

import xadmin
# Register your models here.
from .models import CompanyInfo,Department
import xadmin.views as xviews

xadmin.site.register(CompanyInfo)

xadmin.site.register(Department)

class BaseSetting(object):

  enable_themes = True

  use_bootswatch = True

xadmin.site.register(xviews.BaseAdminView, BaseSetting)

 

class AdminSettings(object):

  # 设置base_site.html的Title

  site_title = 'FDD管理后台'

  # 设置base_site.html的Footer

  site_footer = 'han-xiansheng@qq.com'

  menu_style = 'default'

 

xadmin.site.register(xviews.CommAdminView, AdminSettings) 