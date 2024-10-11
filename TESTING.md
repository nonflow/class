# Unit Testing Documentation

This document provides an overview of the unit tests for the project and instructions on how to run them.

## Test Files

The following test files have been created for each service and module:

1. `tests/test_cloudflare_service.py`: Tests for CloudflareService
2. `tests/test_gitlab_service.py`: Tests for GitLabService
3. `tests/test_github_service.py`: Tests for GitHubService
4. `tests/test_plesk_service.py`: Tests for PleskService
5. `tests/test_email_service.py`: Tests for EmailService, GmailService, and OutlookService
6. `tests/test_date_converters.py`: Tests for date converter functions

## Running Tests

### Using Python

To run all tests using Python's unittest module, use the following command from the project root directory:

```
python -m unittest discover tests
```

To run tests for a specific service:

```
python -m unittest tests/test_<service_name>.py
```

Replace `<service_name>` with the name of the service you want to test (e.g., cloudflare_service, gitlab_service, etc.).

For verbose output, add the `-v` flag:

```
python -m unittest discover -v tests
```

### Using Bash Script

A bash script `run_tests.sh` has been provided to simplify running tests. To use it:

1. Make sure the script is executable:
   ```
   chmod +x run_tests.sh
   ```

2. Run all tests:
   ```
   ./run_tests.sh
   ```

3. Run tests for a specific service:
   ```
   ./run_tests.sh <service_name>
   ```

   Replace `<service_name>` with the name of the service you want to test.

4. Run tests with verbose output:
   ```
   ./run_tests.sh -v
   ```

## Writing New Tests

When adding new functionality to the project, make sure to add corresponding unit tests. Follow these guidelines:

1. Create a new test file in the `tests/` directory if you're adding a new service or module.
2. Use the `unittest` module for writing tests.
3. Mock external dependencies to ensure tests are isolated and repeatable.
4. Aim for high test coverage, testing both normal operation and edge cases.

## Continuous Integration

Consider setting up a CI/CD pipeline to automatically run these tests on each commit or pull request to ensure code quality and catch regressions early.
