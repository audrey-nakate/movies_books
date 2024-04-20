from django.apps import AppConfig


class MoviesBooksAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies_books_app'

    # overriding the ready() method of the users app config to perform initialization task which is registering signals.
    def ready(self):
        import movies_books_app.signals


    