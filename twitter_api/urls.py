
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.routers import DefaultRouter

from main.views import TweetViewSet, TagListView, CommentViewSet, LikesViewSet, RatingViewSet

router = DefaultRouter()
router.register('tweet', TweetViewSet)
router.register('comments', CommentViewSet)
router.register('likes', LikesViewSet)
router.register('rating', RatingViewSet)


schema_view = get_schema_view(
    openapi.Info(
          title="Pytter API",
          default_version='v1',
          description="Some description",
          terms_of_service="https://www.google.com/policies/terms/",
          contact=openapi.Contact(email="contact@snippets.local"),
          license=openapi.License(name="BSD License"),
       ),
    public=True,
)

urlpatterns = [
    path('', schema_view.with_ui()),
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/categories/', TagListView.as_view()),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

