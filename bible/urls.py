from django.contrib import admin
from django.urls import path

import bible.core.views

urlpatterns = [
    path('', bible.core.views.home, name='home'),
    path('tasks/<int:pk>', bible.core.views.detail, name='detail'),
    path('books/<str:abbreviation>', bible.core.views.book, name='book'),
    path('sign-in/', bible.core.views.sign_in, name='sign-in'),
    path('sign-up/', bible.core.views.sign_up, name='sign-up'),
    path('sign-out/', bible.core.views.sign_out, name='sign-out'),
    path('reset-password/', bible.core.views.reset_password, name='reset-password'),
    path('admin/', admin.site.urls),
]
