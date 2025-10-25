#!/usr/bin/env python3
"""
Fix all remaining linting issues
"""
import os
import re

def fix_routes_py():
    """Fix routes.py issues"""
    file_path = 'app/routes.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add constant for "Task not found"
    content = content.replace(
        'from typing import Optional',
        'from typing import Optional\n\n# Constants\nTASK_NOT_FOUND_MSG = "Task not found"'
    )
    
    # Replace all "Task not found" with constant
    content = content.replace('"Task not found"', 'TASK_NOT_FOUND_MSG')
    
    # Fix status variable name conflict
    content = content.replace(
        'status: Optional[str] = Query(None)',
        'task_status: Optional[str] = Query(None)'
    )
    content = content.replace('if status:', 'if task_status:')
    content = content.replace('Task.status == status', 'Task.status == task_status')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_test_files():
    """Fix test files"""
    test_files = [
        'test_api.py',
        'debug_db.py', 
        'reset_db.py',
        'reset_db_simple.py',
        'test_task_creation.py'
    ]
    
    for file_name in test_files:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove unused imports
            lines = content.split('\n')
            cleaned_lines = []
            
            for line in lines:
                # Skip lines with unused imports
                if any(unused in line for unused in [
                    'from app.models import User, Task',
                    'from app.models import Task, TaskStatus, TaskPriority',
                    'from app.auth import get_password_hash',
                    'from app.database import engine',
                    'import json'
                ]):
                    continue
                cleaned_lines.append(line)
            
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write('\n'.join(cleaned_lines))

def main():
    """Fix all issues"""
    print("Fixing routes.py...")
    fix_routes_py()
    
    print("Fixing test files...")
    fix_test_files()
    
    print("All issues fixed!")

if __name__ == "__main__":
    main()
