from helpers import * 

import json
import os
import sys

cache_file_path = 'test_cache.json'

# Load cache file if it exists, otherwise create an empty dictionary
if os.path.exists(cache_file_path):
    with open(cache_file_path, 'r') as cache_file:
        module_cache = json.load(cache_file)
else:
    module_cache = {}

for module, module_name in sorted(find_steps(), key=lambda x: x[1]):
    # Skip modules that are already marked as 'ok' in the cache
    if module_cache.get(module_name) == 'ok':
        print(module_name +' OK')
        continue

    test_functions = [func for func in dir(module) if callable(getattr(module, func)) and func.startswith('test_')]
    all_tests_passed = True
    for test_function in test_functions:
        print('\n' + test_function)
        result = getattr(module, test_function)()
        if result == 'FAIL':
            all_tests_passed = False
            break

    # Update the cache based on the results of the tests
    module_cache[module_name] = 'ok' if all_tests_passed else 'fail'

    # If any test failed, do not proceed with the next module
    if not all_tests_passed:
        with open(cache_file_path, 'w') as cache_file:
            json.dump(module_cache, cache_file)
        sys.exit(1)

# Save the updated cache at the end of the testing
with open(cache_file_path, 'w') as cache_file:
    json.dump(module_cache, cache_file)


print('You are awesome!')