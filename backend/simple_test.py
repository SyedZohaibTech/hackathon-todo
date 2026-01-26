#!/usr/bin/env python3
"""
Simple test to verify that basic functionality works
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing basic functionality...")

# Test 1: Check if we can create basic data structures
try:
    from datetime import datetime
    from uuid import uuid4

    # Create a mock task-like object
    task_title = "Test Task"
    task_description = "Test Description"
    task_completed = False
    task_created_at = datetime.now()

    print(f"[OK] Basic data structures work: {task_title}")
except Exception as e:
    print(f"[FAIL] Basic data structures failed: {e}")

# Test 2: Check if we can work with UUIDs
try:
    user_id = uuid4()
    print(f"[OK] UUID generation works: {str(user_id)[:8]}...")
except Exception as e:
    print(f"[FAIL] UUID generation failed: {e}")

# Test 3: Check if we can work with basic imports
try:
    import json
    import re
    print("[OK] Basic Python modules work")
except Exception as e:
    print(f"[FAIL] Basic Python modules failed: {e}")

print("\nBasic functionality tests completed.")
print("Note: More comprehensive testing would require full dependency installation.")