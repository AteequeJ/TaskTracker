from rest_framework.routers import DefaultRouter
from .views import PageViewSet, TodoViewSet, TaskViewSet

router = DefaultRouter()
router.register(r"pages", PageViewSet, basename="page")
router.register(r"todos", TodoViewSet, basename="todo")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = router.urls
