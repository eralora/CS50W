from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return  f"{self.name}"

class Listing(models.Model):
	title = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=200, null=True)
	starting_bid = models.FloatField()
	image = models.ImageField(null=True, blank=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	is_active = models.BooleanField(default=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return  f"Ttitle: {self.title} id: {self.id}"

		# For errors if no picture exist
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	
		
class Bid(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
	bid = models.FloatField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return f"{self.listing}"


class Comment(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE,null=True, blank=True)
	comment = models.CharField(max_length=200, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True)

	def __str__(self):
		return f"{self.comment}"

class Watchlist(models.Model):
	watcher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return f"Watcher: {self.watcher} {self.item}"

	@property
	def get_total(self):
		watchlists = Watchlist.objects.all()
		total = len(watchlists)
		return self.total

	
	
	
class Test(models.Model):
	title=models.CharField(max_length=200,null=True, blank=True)
	img=models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.title