import os
import sys

def main():
    # Set the default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digistore.settings.dev')

    # Import Django's command-line utility for management tasks
    from django.core.management import execute_from_command_line

    # Execute the command-line utility with provided arguments
    execute_from_command_line(sys.argv)

# Entry point of the script
if __name__ == '__main__':
    main()