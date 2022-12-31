# CHANGELOG

## v0.5.0
- Rework package
  - Update `dash_allgraphs_live.py`
    - `env` argument enables the use of environment variables
    - Add function to always check for database file on startup
    - Update usage help output
    - Update LS120/settings.py accordingly
  - Add note to init in LS120 module about import order
  - Add and update logging entries in db_create and db_auto_import
  - Add BUG note to read_youless.py
    - TODO - fix this bug
  - Change default logging path to base youless folder
    - Update yaml config accordingly
  - Rework dependency import order
- Update README.md
- Update package.md
- Update startupscript.md
  - Add instructions for using a shell script
  - Add instructions for using environment variables
  - Modify service instructions to use shell script
- Update requirements.txt to newest versions
- Update Python version to 3.10
- Remove all last modified entries
- Remove whitespace from files
- Add .dockerignore
- Add .gitignore
- Add .code-workspace file
- Add CHANGELOG.md
