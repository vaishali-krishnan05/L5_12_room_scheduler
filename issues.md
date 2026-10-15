\# Static Code Analysis — Issues Found



| Issue | Type | Line(s) | Description | Fix Approach |

|---|---|---|---|---|

| Unsafe shell command | Security — High | 43 | `os.system("cat " + file)` executes a shell command using a filename, creating a potential command-injection vulnerability. | Replace shell execution with safe Python file handling using a context manager. |

| Equipment over-allocation | Bug — Medium | 16–17 | Equipment counts are reduced without checking whether the equipment exists or sufficient stock is available. Counts may become negative or an invalid equipment name may cause an error. | Validate equipment names and stock before updating counts or creating a reservation. |

| Invalid time-slot handling | Bug — Medium | 31–32, 48–49 | `slot\_hours()` can return a negative duration for `14-12`, and `schedule\_room()` accepts an integer slot instead of a string. | Validate the slot format and ensure the end time is later than the start time. |

| Unsafe cancellation error handling | Code quality — Low | 23–28 | A bare `except` silently ignores errors, including attempts to cancel nonexistent reservations. | Check whether the reservation exists and handle the expected `KeyError` explicitly or return a clear result. |

| Mutable default argument | Code quality — Medium | 11 | `equipment\_list=\[]` uses a mutable default object that can be shared across calls. | Use `None` as the default and create a fresh list inside the function. |

| Unclosed file handling | Code quality — Medium | 35–37, 40–43 | Files are opened and closed manually, and `logConflicts()` does not close its file explicitly. | Use `with open(...)` context managers and specify an encoding. |

| Missing documentation and inconsistent naming | Code quality | 1, 9, 11, 22, 30, 34, 39, 45 | The module and functions lack docstrings, and names such as `next\_reservation` and `logConflicts` do not follow Pylint's naming conventions for constants and functions. | Add appropriate docstrings, use `NEXT\_RESERVATION` for a constant if it is truly constant, and rename `logConflicts` to `log\_conflicts`. |

| Formatting violations and unused variables | Style | 11, 14, 18, 22, 30, 34, 39, 45–49, 59 | Flake8 reports missing blank lines, long lines, and unused local variables (`a`, `a\_more`, and `c`). | Apply consistent formatting, split long lines, remove unused variables, and add the required blank lines. |

