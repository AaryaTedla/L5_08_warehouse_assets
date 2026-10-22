
# Lab 5 - Static Code Analysis

## Identified Issues and Fixes

### Initial Analysis Results

- Pylint: 6.55/10
- Bandit: 1 Medium and 1 Low severity issue
- Flake8: 12 violations

## Issues Identified

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Insecure temporary file | Security | 40 | tempfile.mktemp() creates a predictable temporary filename without securely creating the file. | Replaced it with tempfile.NamedTemporaryFile(). |
| Assert used for validation | Security | 61 | Assertions can be disabled in optimized Python execution. | Replaced the assertion with an explicit RuntimeError check. |
| Mutable default argument | Bug | 10 | A default list persists across calls and can produce unexpected shared state. | Used None as the default and initialized the log separately. |
| Bare except | Code Quality | 18 | The exception handler catches unexpected errors and hides their causes. | Replaced it with specific error handling. |
| Missing docstrings | Style | 1, 10-50 | Module and functions had no documentation. | Added module and function docstrings. |
| Unsafe file handling | Code Quality | 34, 41 | Files were opened without context managers and explicit encoding. | Used with statements and UTF-8 encoding. |
| Global statement | Code Quality | 30 | A function modified a global configuration value. | Stored the configuration in a settings dictionary. |
| Incorrect naming | Style | 46 | printAlerts did not follow Python naming conventions. | Renamed it to print_alerts. |
| Unused import | Style | 2 | logging was imported but never used. | Removed the unused import. |
| Formatting violations | Style | Multiple | Functions lacked blank lines and some lines exceeded 79 characters. | Reformatted the code according to Flake8 conventions. |
| Invalid asset ID | Logic | 53 | An empty asset ID was accepted. | Added validation to reject empty IDs. |
| Duplicate asset | Logic | 54 | Registering FL-01 again overwrote the previous record. | Added a duplicate registration check. |
| Negative interval | Logic | 57 | A negative inspection interval was accepted. | Restricted the interval to positive integers. |
| Invalid service date | Logic | 15-19 | Invalid or future dates could be stored. | Added date parsing and validation. |

## Fix Summary

### Bandit

The insecure tempfile.mktemp() call was replaced with
tempfile.NamedTemporaryFile().

The assertion used for runtime validation was replaced
with an explicit exception.

### Pylint

Added docstrings, removed the unused import, improved
exception handling, removed the mutable default argument,
and improved file handling.

### Flake8

Corrected function spacing, line lengths, and formatting
to follow Python style conventions.

### Logical Corrections

Added validation for asset IDs, duplicate registrations,
service dates, and inspection intervals.

## Verification

The original reports are stored in reports/before/.

The updated reports are stored in reports/after/.

The final program was checked using Pylint, Bandit,
and Flake8 to verify the corrections.
