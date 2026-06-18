from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create default admin user and a TechnicianProfile linked to it for local testing.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        password = 'admin123'
        email = 'admin@example.com'

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}' with password '{password}'"))
        else:
            # Ensure superuser flags and password are set for deterministic testing
            changed = False
            if not user.is_superuser:
                user.is_superuser = True
                changed = True
            if not user.is_staff:
                user.is_staff = True
                changed = True
            user.set_password(password)
            if changed:
                user.save()
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists; updated flags and reset password."))

        # Lazily import the TechnicianProfile so Django app registry is ready
        try:
            from invoices.models import TechnicianProfile
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Could not import TechnicianProfile: {e}"))
            return

        employee_id = 'HE-2026'
        phone_number = '0312-5550000'

        tp, tp_created = TechnicianProfile.objects.get_or_create(user=user, defaults={'employee_id': employee_id, 'phone_number': phone_number})
        if tp_created:
            self.stdout.write(self.style.SUCCESS(f"TechnicianProfile created and linked to '{username}' (employee_id={employee_id})."))
        else:
            tp.employee_id = employee_id
            tp.phone_number = phone_number
            tp.save()
            self.stdout.write(self.style.WARNING(f"TechnicianProfile for '{username}' updated with employee_id={employee_id} and phone={phone_number}."))
