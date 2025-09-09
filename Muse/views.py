from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.db.models import Q
import json

# Import models and forms at the bottom to avoid circular import issues
from .models import Movie, Review, Genre
from .forms import ReviewForm, CustomUserCreationForm, CustomAuthenticationForm


# ------------------------------
# Authentication Views
# ------------------------------
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('movie_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


# ------------------------------
# Movie Views
# ------------------------------
def movie_list(request):
    search_query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')
    movies = Movie.objects.all()

    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(director__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if genre_filter:
        movies = movies.filter(genre__name=genre_filter)

    genres = Genre.objects.all()

    return render(request, 'muse/movie_list.html', {
        'movies': movies,
        'genres': genres,
        'search_query': search_query,
        'selected_genre': genre_filter,
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie).select_related('user')
    user_review = None

    if request.user.is_authenticated:
        user_review = Review.objects.filter(movie=movie, user=request.user).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to leave a review.')
            return redirect('login')

        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been saved!')
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = ReviewForm(instance=user_review)

    return render(request, 'muse/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    })


# ------------------------------
# API Views
# ------------------------------
class MovieReviewsView(View):
    """Return all reviews for a specific movie"""
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        reviews = Review.objects.filter(movie=movie).select_related('user')

        reviews_data = [{
            'id': r.id,
            'username': r.user.username,
            'review': r.review,
            'rating': r.rating,
            'created_at': r.created_at.isoformat(),
        } for r in reviews]

        return JsonResponse(reviews_data, safe=False)


class ReviewCreateView(View):
    @csrf_exempt
    def post(self, request, movie_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        movie = get_object_or_404(Movie, id=movie_id)
        data = json.loads(request.body)

        if Review.objects.filter(movie=movie, user=request.user).exists():
            return JsonResponse({'error': 'You have already reviewed this movie'}, status=400)

        review = Review.objects.create(
            user=request.user,
            movie=movie,
            review=data.get('review', ''),
            rating=data.get('rating', 5)
        )
        return JsonResponse({
            'id': review.id,
            'username': review.user.username,
            'review': review.review,
            'rating': review.rating,
            'created_at': review.created_at.isoformat()
        })


class ReviewUpdateView(View):
    @csrf_exempt
    def put(self, request, review_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        review = get_object_or_404(Review, id=review_id)
        if review.user != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        data = json.loads(request.body)
        review.review = data.get('review', review.review)
        review.rating = data.get('rating', review.rating)
        review.save()

        return JsonResponse({
            'id': review.id,
            'review': review.review,
            'rating': review.rating,
            'updated_at': review.updated_at.isoformat()
        })


class ReviewDeleteView(View):
    @csrf_exempt
    def delete(self, request, review_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        review = get_object_or_404(Review, id=review_id)
        if review.user != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        review.delete()
        return JsonResponse({'message': 'Review deleted successfully'}, status=200)
