# Lab 5: Issues found in smart_home.py

Before: Pylint 4.80/10, Bandit 1 High + 1 Medium + 2 Low, Flake8 4 issues.
After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `shell=True` in subprocess (B602, High) | Security | 51 | `runScene` glues the scene name onto `"bash scenes/"` and runs it through a shell. Someone could pass `x; rm -rf ~` or `../../evil.sh` and it would just run | Dropped the shell and call `subprocess.call(["/bin/bash", path])`. The name goes through `os.path.basename` and is rejected if it changes or the file isn't there |
| Binding to all interfaces (B104, Medium) | Security | 4 | `HUB_HOST = "0.0.0.0"` makes the hub reachable from every network the machine is on | Default is now `127.0.0.1`, and it can be changed with the `HUB_HOST` env variable |
| Hardcoded password (B105, Low) | Security | 7 | `HUB_PASSWORD = "smarthome-demo"` sits in the source and ends up on GitHub | Reads `HUB_PASSWORD` from the environment instead |
| `subprocess` import (B404, Low) | Security | 2 | Just an informational warning about importing subprocess | I still need it, so I added `# nosec B404` with a reason. Same for `# nosec B603` on the call, since the arguments are a fixed list and the file name is validated |
| Mutable default argument (W0102) | Bug | 11-13 | `settings={}` is created once and shared. Setting the thermostat to 30 also gave the Ceiling Light `temperature: 30` (the demo printed it) | Default is `None`, and each device gets its own `{}` |
| `setTemperature` crashes on unknown device | Bug (no tool flagged it) | 24 | `devices[deviceName]` throws `KeyError` if the name doesn't exist, while `toggleDevice` handles that case fine | Used `devices.get()`, print "Device not found" and return `False` |
| Inconsistent return (R1710) | Code quality | 16-20 | `toggleDevice` returns a value in one branch and nothing in the other | Added an explicit `return None` |
| `open()` without encoding (W1514) | Code quality | 41 | Encoding depends on the computer's locale | Added `encoding="utf-8"` |
| camelCase names (C0103, 10 hits) | Style | 11-49 | `addDevice`, `deviceName`, `saveState` etc. aren't snake_case | Renamed everything to snake_case and updated the calls |
| Missing docstrings (C0114, C0116) | Documentation | 1, 11-54 | No module docstring and no function docstrings | Wrote short docstrings |
| Space before `:` (E203) | Flake8 | 6 | `"light" : 10` | `"light": 10` |
| Expected 2 blank lines (E302) | Flake8 | 40 | Only one blank line before `saveState` | Added one more |
| Inline comment spacing (E261) | Flake8 | 66 | One space before `# for app setup` | Two spaces |
| Line too long (E501) | Flake8 | 68 | 80 characters, limit is 79 | Moved the list into a variable `on_now` first |
| `main()` runs on import | Design | 72 | Importing the file runs the demo and writes `home_state.json` | Wrapped it in `if __name__ == "__main__":` |
| Magic numbers 16 and 30 | Design | 28 | Safe temperature range is hidden inside one line | Made them `MIN_TEMP` and `MAX_TEMP` |

## Commits
1. Fix Bandit security issues (shell=True, bind address, hardcoded password)
2. Fix Flake8 style issues (E203, E302, E261, E501)
3. Fix Pylint issues (mutable default, naming, docstrings, encoding, returns)
