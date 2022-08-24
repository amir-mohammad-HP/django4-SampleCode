# Signals

this, let you know the signals before and after any action get done on models and decide to make another actions depending on them like creating another model

## how to use
copy "signals.py" in your django app and replace the foo models with a your model intend to got the signal

```bash
from myapp.models import foo  # foo is an arbitrary model

@receiver(pre_delete, sender = foo)
def before_foo_delete(sender, instance, *args, **kwargs):

    print(instance) # this will call before foo instance delete
```
then add this function to your "apps.py" in the same app you add the "signals.py".

```python
def ready(self) -> None:
        from myapp import signals
        return super().ready()
```

you can find more information in [django](https://docs.djangoproject.com/en/4.0/ref/signals/) website
