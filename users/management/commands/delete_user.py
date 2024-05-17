from django.core.management.base import BaseCommand
from users.models import CustomUser as User

class Command(BaseCommand):
    help = 'Delete a user by username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user to delete')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        
        try:
            user_to_delete = User.objects.get(username=username)
            user_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f"User '{username}' deleted successfully!"))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{username}' does not exist."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))