from django.db import models

class Contact(models.Model):
    full_name = models.CharField(max_length=50)
    email_address = models.EmailField()
    message_body = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email_address
