from django.db import models

# Create your models here.

class Elaboration(models.Model):
    challenge = models.ForeignKey('Challenge.Challenge')
    portfolio = models.ForeignKey('Portfolio.Portfolio')
    user = models.ForeignKey('PortfolioUser.PortfolioUser')
    creationDate = models.DateTimeField(auto_now_add=True)