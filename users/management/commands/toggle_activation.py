from django.core.management.base import BaseCommand, CommandError
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Toggle the activation status of a user account'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the account to be toggled')
        parser.add_argument('status', type=str, help='Activation status: true to activate, false to deactivate')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        status = kwargs['status'].lower()

        try:
            user = CustomUser.objects.get(username=username)
            if status not in ['true', 'false']:
                raise CommandError('Status must be either "true" or "false".')

            user.is_activated = status == 'true'
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully {"activated" if status == "true" else "deactivated"} user: {username}'))
        except CustomUser.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')