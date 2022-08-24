from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete

# import a model from your app :
from myapp.models import foo 

@receiver(pre_delete, sender = foo)
def before_foo_delete(sender, instance, *args, **kwargs):

    print(instance) # this will call before foo instance delete


@receiver(post_delete, sender = foo)
def after_foo_delete(sender, instance, *args, **kwargs):

    print(instance) # this will call after foo instance deleted
    

@receiver(pre_save, sender = foo)
def before_foo_save(sender, instance, *args, **kwargs):

    print(instance) # this will call before foo instance save


@receiver(post_save, sender = foo)
def after_foo_saved(sender, instance, created, *args, **kwargs):

    if created: # if foo new instance created
        try:
            print(instance) # this would call 
        except:
            pass

