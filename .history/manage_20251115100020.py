#!/usr/bin/env python
"""فایل entry-point جنگو — اجراکننده دستورات manage.py"""
import os
import sys

def main():
    # اگر متغیر محیطی مشخص نشده، از dev استفاده کن
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digistore.settings.dev')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()