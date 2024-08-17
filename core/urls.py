
from django.contrib import admin 
from django.urls import path,include

from users.views import signup, login,logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('login/', login,name = 'login'),
    path('signup/',  signup,name = 'signup'),
    path('logout/',  logout,name = 'logout'),

]
