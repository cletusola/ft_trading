from django.db import models
from django.contrib.auth import get_user_model 
User = get_user_model()



# profile model 
class Profile(models.Model):
    firstname = models.CharField(max_length=20, null=False, blank=False)
    lastname = models.CharField(max_length=20, null=False, blank=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=120, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)


    class Meta: 
        ordering = ['-date']

    def __str__(self):
        return f"{self.username}" 



# trading model 
class Trade(models.Model):
    profit_or_loss = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trade")
    time = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user}" 

        