# Tests Directory

This directory contains all test files and test-related documentation for the QR Code Secret Messages project.

## Test Files

### `test_suite.py`
Comprehensive test suite that validates all features of the application:
- **Test A**: Key Derivation (SHA-256)
- **Test B**: AES-GCM Encryption/Decryption
- **Test C**: Password Strength Checker
- **Test D**: Brute Force Protection
- **Test E**: Authentication System
- **Test F**: Text File Encryption
- **Test G**: QR Code Generation
- **Test H**: QR Code Decryption

### `run_tests.py`
Test runner script that executes the complete test suite and displays results.

## Running Tests

To run all tests, execute from the project root directory:

```bash
python tests/run_tests.py
```

Or from within the tests directory:

```bash
cd tests
python run_tests.py
```

## Test Documentation

### `TEST_RESULTS_SUMMARY.md`
Detailed summary of test results including:
- Test execution results
- Pass/fail status for each test
- Security notes and suggestions
- Performance metrics

### `FUNCTION_VERIFICATION_REPORT.md`
Comprehensive verification report documenting:
- Function-by-function verification
- Security feature validation
- Implementation details
- Test coverage analysis

## Test Coverage

The test suite covers:
-  Cryptographic functions (encryption, decryption, key derivation)
-  QR code generation and reading
-  Password strength validation
-  User authentication and registration
-  Brute-force protection mechanisms
-  File encryption/decryption workflows
-  End-to-end encryption/decryption cycles

## Requirements

All tests require the project dependencies to be installed:

```bash
pip install -r requirements.txt
```

## Notes

- Tests use temporary files to avoid modifying production data
- Test files are automatically cleaned up after execution
- Some tests may take a few seconds to complete (especially QR code tests)
- All tests are designed to be run independently and in sequence

