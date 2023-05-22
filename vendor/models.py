from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification



class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vender_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='media/vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vender_name
    

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                context = {
                        'user': self.user,
                        'is_approved': self.is_approved
                }

                if self.is_approved:
                    # Send notification email
                    mail_subject = "Congratulations! Your restaurant has been approved"
                else:
                    # Send not notification email
                    mail_subject = "Sorry you are not eligible for registration."

                send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)