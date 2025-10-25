#!/usr/bin/env python3
"""
Final cleanup of all remaining issues
"""
import os

def clean_test_files():
    """Clean up all test files"""
    test_files = [
        'test_api.py',
        'debug_db.py', 
        'reset_db.py',
        'reset_db_simple.py',
        'test_task_creation.py',
        'tests/test_api.py'
    ]
    
    for file_name in test_files:
        if os.path.exists(file_name):
            print(f"Cleaning {file_name}...")
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove all unused imports
            lines = content.split('\n')
            cleaned_lines = []
            
            for line in lines:
                # Skip lines with unused imports
                if any(unused in line for unused in [
                    'from app.models import User, Task',
                    'from app.models import Task, TaskStatus, TaskPriority', 
                    'from app.auth import get_password_hash',
                    'from app.database import engine',
                    'import json',
                    'import re'
                ]):
                    continue
                cleaned_lines.append(line)
            
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write('\n'.join(cleaned_lines))

def main():
    """Final cleanup"""
    print("Performing final cleanup...")
    clean_test_files()
    print("Final cleanup complete!")

if __name__ == "__main__":
    main()
