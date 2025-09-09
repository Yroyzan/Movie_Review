from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ManyToManyField(Genre, blank=True, related_name="movies")
    director = models.CharField(max_length=50)
    release_year = models.DateField()
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        """Calculate average rating from all reviews"""
        return self.reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    def get_total_reviews(self):
        """Get total number of reviews"""
        return self.reviews.count()

class Review(models.Model):
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE, 
        related_name="reviews", 
        default=1  # TEMPORARY: default first movie ID
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="reviews", 
        default=1  # TEMPORARY: default admin user ID
    )
    review = models.TextField(max_length=500, default="")  # TEMPORARY default
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,  # TEMPORARY default
        help_text="Rate from 1 to 5 stars"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.title} - {self.rating} stars"
