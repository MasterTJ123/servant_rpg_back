from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, LoginView, LogoutView, RefreshView, CombatantViewSet, CombatantGroupViewSet, \
    GroupViewSet, AmbientViewSet, EncounterViewSet, EnemyEncounterViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('combatants', CombatantViewSet)
router.register('groups', GroupViewSet)
router.register('combatants-groups', CombatantGroupViewSet)
router.register('encounters', EncounterViewSet)
router.register('enemies-encounters', EnemyEncounterViewSet)
router.register('ambients', AmbientViewSet)

urlpatterns = [
    # Users
    path('', include(router.urls)),
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
]
