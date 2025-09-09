from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Main pages
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # proper logout

    # API endpoints
    path('api/movies/<int:movie_id>/reviews/', views.MovieReviewsView.as_view(), name='movie_reviews_api'),
    path('api/movies/<int:movie_id>/reviews/create/', views.ReviewCreateView.as_view(), name='create_review_api'),
    path('api/reviews/<int:review_id>/update/', views.ReviewUpdateView.as_view(), name='update_review_api'),
    path('api/reviews/<int:review_id>/delete/', views.ReviewDeleteView.as_view(), name='delete_review_api'),
]
