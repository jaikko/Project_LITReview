from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('dashbord', views.dashbord, name='dashbord'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ticket/create', views.createTicket, name="newticket"),
    path('subscription', views.subscription, name='subscription'),
    path('unsubscription/<int:id>', views.unsubscription, name='unsubscription'),
    path('review/create', views.createReview, name='newreview'),
    path('review/answer/<int:id>', views.answerTicket, name="answerticket"),
    path('ticket/update/<int:id>', views.editTicket, name="edit_ticket"),
    path('ticket/delele/<int:id>', views.deleteTicket, name='deleteticket'),
    path('review/update/<int:id>', views.editReview, name="edit_review"),
    path('review/delele/<int:id>', views.deleteReview, name='deletereview'),
    path('post', views.post, name="post")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
