from django.urls import path
from apps.api.views import (
    # Authentication
    AuthRegister,
    AuthLogin,
    AuthLogout,
    AuthValid,
    AuthRefresh,
    
    # User
    UserInfo,
    UserSolves,
    UserProfile,

    # Admin
    AdminChallengeList,
    AdminChallengeAdd,
    AdminChallengeDelete,
    AdminChallenge,
    AdminHint,
    AdminFlag,
    AdminTag,
    AdminConfig,

    # Misc
    IsLive,

    # App
    ChallengeList,
    ChallengeAttempt,
    Scoreboard,
    # ChallengeSolves,
    ChallengesSolves,
)

urlpatterns = [
    path('challenges/', ChallengeList.as_view()),
    path('challenges/attempt/', ChallengeAttempt.as_view()),
    # path('challenges/<slug:uuid>/solves/', ChallengeSolves.as_view()),
    path('challenges/solves/', ChallengesSolves.as_view()),

    # AUTHENTICATION
    path('auth/register/', AuthRegister.as_view()),
    path('auth/valid/', AuthValid.as_view()),
    path('auth/login/', AuthLogin.as_view()),
    path('auth/logout/', AuthLogout.as_view()),
    path('auth/refresh/', AuthRefresh.as_view()),

    # USER
    path('user/me/', UserInfo.as_view()),
    path('user/solves/', UserSolves.as_view()),
    path('user/profile/<slug:slug>/', UserProfile.as_view()),

    # ADMIN
    path('admin/challenges/', AdminChallengeList.as_view()),
    path('admin/challenges/add/', AdminChallengeAdd.as_view()),
    path('admin/challenge/<str:uuid>/', AdminChallenge.as_view()),
    path('admin/challenge/<str:uuid>/delete/', AdminChallengeDelete.as_view()),
    path('admin/hint/', AdminHint.as_view()),
    path('admin/flag/', AdminFlag.as_view()),
    path('admin/tag/', AdminTag.as_view()),
    path('admin/config/', AdminConfig.as_view()),

    # MISC
    path('live/', IsLive.as_view()),
    path('scoreboard/', Scoreboard.as_view()),
]
