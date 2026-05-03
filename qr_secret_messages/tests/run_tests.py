

import os
import sys
import io
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

sys.stdout = sys.stderr = io.TextIOWrapper(sys.stdout.buffer, line_buffering=True)

print("=" * 80)
print("Starting Test Suite...")
print("=" * 80)
sys.stdout.flush()

try:
    from test_suite import run_all_tests
    
    print("\nRunning all tests...")
    sys.stdout.flush()
    
    results = run_all_tests()
    
    print("\n" + "=" * 80)
    print("Test execution completed!")
    print("=" * 80)
    
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

