# Lab 5 Reflection

## 1. Which issues were easiest and hardest to fix?
The Flake8 ones were the easiest. It tells you the exact line and what's wrong, so it was basically just spacing and blank lines. The naming and docstring warnings from Pylint were the same, boring but quick.

The hardest was the `shell=True` problem in `run_scene`. Taking out the shell was one change, but then I had to decide what a valid scene name even is. I ended up allowing only a plain file name inside `scenes/` and rejecting anything with a path in it. The mutable default argument was also tricky to understand at first. The fix is tiny, but I only really got it after seeing the light's settings show `temperature: 30` in the output.

## 2. Did the tools give any false positives or miss anything?
A couple of Bandit warnings were more of a heads-up than a real problem. B404 just says "you imported subprocess", and I actually need it, so I suppressed it with `# nosec` and wrote why. B603 on the call is the same story, since after the fix the arguments are a fixed list with a checked file name. The password warning (B105) was correct here, but I can see it firing on harmless variables that just have "password" in the name.

The tools also missed things. `set_temperature` crashed with a `KeyError` for a device that doesn't exist, and nothing flagged it. Also `main()` ran as soon as the file was imported. I only caught those by reading the code and the program output. Pylint did point at the shared `{}` default, but it can't tell you that this makes a light get a temperature.

## 3. How would you use static analysis in a real project?
I'd run Flake8 and Pylint locally with a pre-commit hook so the easy stuff never gets committed. Then I'd run all three tools in CI (GitHub Actions for example) on every pull request, and fail the build on any Bandit High or Medium issue or if the Pylint score drops under something like 9.5. I'd also keep `# nosec` and `# pylint: disable` comments rare and always add a reason, so a reviewer can question them.

## 4. What did static analysis add to code quality and maintainability?
The score went from 4.80 to 10.00 and Bandit went from four findings to zero. More important to me, it found a command injection hole, an open network binding, a committed password and a real shared-state bug without me running anything. The code is also easier to read now with consistent names and docstrings. But it can't replace actually running the program and thinking about what it should do, because tools only match patterns and don't know the intent.
