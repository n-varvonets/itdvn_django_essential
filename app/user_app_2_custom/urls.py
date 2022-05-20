from .views import Index, CreatUser, AllUsers, UpdateProfile
from django.urls import path
from app.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
          path('', Index.as_view(), name="index"),
          path('signup2/', CreatUser.as_view(), name="signup2"),
          path('all_users/', AllUsers.as_view(), name="all_users"),
          path('profile/<pk>', UpdateProfile.as_view(), name='profile')
      ] + static(MEDIA_URL, document_root=MEDIA_ROOT)