###############################################################################
# TOPIC: Virtual Environments, pip, and sys.prefix Isolation Internals
#
# 1. DEFINITION & INTRODUCTION:
#    - Virtual Environment: An isolated directory containing its own Python executable,
#      standard libraries, and site-packages folder. Created using `python -m venv venv_name`.
#    - Motivation: Prevents "dependency hell" (version conflicts between requirements of
#      different applications installed globally on the same system).
#    - `pip`: The standard package installer for Python, pulling packages from the Python
#      Package Index (PyPI).
#
# 2. ISOLATION MECHANICS (CPython Internals):
#    - How does Python know it is running inside a virtual environment?
#    - When you run the Python binary inside a virtual environment directory:
#        1. The launcher looks for a file named `pyvenv.cfg` in the executable's parent folder.
#        2. If found, CPython sets two key internal prefixes:
#           - `sys.base_prefix`: Points to the global standard Python installation directory.
#           - `sys.prefix`: Points to the active virtual environment directory containing the
#             local `site-packages`.
#        3. When compiling `sys.path`, Python dynamically redirects search paths to look in the virtual
#           environment's `site-packages` directory instead of the system-wide site-packages.
#    - Shell Activation: Activating a virtual environment (`source venv/bin/activate`) simply
#      updates the shell's environment variables:
#        - Prepends the venv `bin/` directory to the `PATH` variable, ensuring typing `python`
#          targets the virtual environment launcher.
#        - Modifies the shell prompt (prefixing `(venv)`).
#      Note: Activation is not strictly required. Executing `path/to/venv/bin/python` directly
#      automatically triggers environment redirection.
#
# 3. PACKAGING AND DEPENDENCY DECLARATION:
#    - `requirements.txt`: Flat text file listing dependencies and versions.
#    - `pip freeze`: Outputs currently installed package versions in format for `requirements.txt`.
#
# 4. BEST PRACTICES:
#    - Always create a virtual environment for every new project. Never install packages globally
#      using system Python (e.g. `sudo pip install`), which can break system package managers.
#    - Commit `requirements.txt` or modern configurations (like `pyproject.toml`) to git.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: How does CPython dynamically determine if it is executing inside a virtual environment?
#      A: By checking for the presence of the `pyvenv.cfg` configuration file in the executable's
#         parent directory. If present, it redirects `sys.prefix` to point to the venv directory.
#    - Q: What is the difference between `sys.prefix` and `sys.base_prefix`?
#      A: `sys.prefix` points to the active environment (which is the venv folder if active).
#         `sys.base_prefix` points to the system-wide core Python installation. They are equal
#         if running outside a virtual environment.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a script that checks if it is currently running inside an isolated
#      virtual environment, printing the base prefix and virtual prefix paths.
#
###############################################################################

import sys  # Standard library to inspect path prefixes
import os  # Standard library to query environment variables

# 1. Virtual Environment Isolation Detection
# We inspect sys.prefix and sys.base_prefix.
# If they are different, we are running inside a virtual environment.
in_virtual_env = sys.prefix != sys.base_prefix

print("--- Virtual Environment Detection ---")
print(f"Is running inside a virtual environment? {in_virtual_env}")
print(f"Active prefix (sys.prefix):           {sys.prefix}")
print(f"Base prefix (sys.base_prefix):       {sys.base_prefix}")

# 2. Check pyvenv.cfg configuration
# We attempt to check if pyvenv.cfg is present in the parent path.
pyvenv_cfg_path = os.path.join(sys.prefix, "pyvenv.cfg")
print(f"\nChecking for pyvenv.cfg at: {pyvenv_cfg_path}")
print(f"Does pyvenv.cfg exist? {os.path.exists(pyvenv_cfg_path)}")

# 3. Inspect active shell environment variables
# When activated, the shell sets 'VIRTUAL_ENV' environment variable pointing to the folder.
env_var_active = os.environ.get("VIRTUAL_ENV")
print(f"VIRTUAL_ENV environment variable: {repr(env_var_active)}")

# 4. Generating a requirements.txt file simulation
# We can dynamically print how we write requirements.txt
mock_dependencies = [
    "requests==2.31.0",
    "numpy==1.26.2",
    "fastapi==0.104.1"
]

print("\n--- Generating requirements.txt output ---")
for dep in mock_dependencies:
    # Print dependency lines
    print(dep)
