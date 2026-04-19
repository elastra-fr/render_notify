# Render Notify Addon for Blender

Render on Blender can took a long time, and it can be frustrating to wait without knowing when the process is complete. The Render Notify addon for Blender aims to solve this problem by providing a simple notification system that alerts users when their renders are finished. You can safely mow your lawn, do the dishes, or even take a nap while waiting for your render to complete, knowing that you'll be notified as soon as it's done or even if it fails.

The addon is currently in its early stages of development, and the version is set to 0.0.1. The author is Emmanuel LASTRA DE NATIAS. The addon is designed to work with Blender version 4.0.0 and above (to be confirmed).

This addon provides a simple notification system for Blender's render process. It allows users to receive notifications when a render is complete, making it easier to manage long rendering tasks without having to constantly check the progress.

## Security

Credentials are stored via the `keyring` library, which securely manages sensitive information. This ensures that your email and/or Discord credentials are not exposed in plain text.

## Messages customization

The addon allows users to customize the notification messages that are sent when a render is complete. This feature enables users to personalize their notifications according to their preferences, making the experience more enjoyable and tailored to their needs.

## Channels 

The addon supports multiple notification channels, including for now 
- email 
- Discord. 

Users can choose their preferred method of receiving notifications, allowing for greater flexibility and convenience in managing their rendering workflow.

### Email

Users can set up email notifications to receive alerts when their renders are complete. This is particularly useful for those who want to stay informed without having to check Blender constantly.

Do not use a personal email address for this purpose. Instead, create a dedicated email account for sending notifications to ensure better security and management of your credentials. If you can use an app specific password, it is recommended to enhance security further.

### Discord

Users can also opt to receive notifications via Discord, which is a popular communication platform for gamers and communities. This allows users to stay connected and receive updates in real-time without leaving their workflow. To set up Discord notifications, users will need to create a webhook in their Discord server and provide the webhook URL in the addon's settings. This way, they can receive notifications directly in their chosen Discord channel when a render is complete.

## Tests 

A test suite with `pytest` is provided in `tests/`. The tests can be run outside of Blender thanks to fakes for `bpy` and `keyring`.

Prerequisite: `pytest` and virtual environment (recommended).

Create a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
```


Activate the virtual environment (Linux/MacOS) :

```bash
source .venv/bin/activate
```

Deactivate the virtual environment:

```bash
deactivate
```

Execution examples:

```bash
# in the project's virtual environment (recommended)
./.venv/bin/python3 -m pytest -v

# or globally
python3 -m pytest -v
```

Install `pytest` in the venv:

```bash
./.venv/bin/python3 -m pip install pytest
```

## Installation

Pour installer l’addon dans Blender, téléchargez **render_notify-x.y.z.zip** depuis la section “Assets” de la page de release GitHub (ne pas utiliser “Source code”).

Dans Blender :
- Edit > Preferences > Add-ons > Install…
- Sélectionnez le fichier render_notify-x.y.z.zip téléchargé

Redémarrez Blender si besoin, puis activez l’addon dans la liste.

## Workflow

This project follows a Git workflow and automated CI/release rules:

- Branches:
	- `main`: release branch containing released code and tags.
	- `develop`: integration branch for completed features.
	- `feature/*`: feature branches created from `develop`.
	- `hotfix/*`: urgent fixes created from `main` and merged back into `develop`.
    - `refactor/*`: refactoring branches created from `develop` for code improvements without changing functionality.
    - `chores/*`: maintenance branches created from `develop` for tasks like updating dependencies, improving documentation, or other non-feature work.
    - `ci/*`: branches for CI configuration changes, created from `develop` and merged back after review.

- Pull Requests & CI:
	- Pull requests targeting `develop` or `main` run the CI workflow (`.github/workflows/ci.yml`).
	- CI performs a `version-check` (ensures `render_notify/_version.py` matches `bl_info['version']`), then runs tests and uploads coverage artifacts (`htmlcov`, `coverage.xml`).

- Release:
	- Pushing or merging to `main` triggers the release workflow (`.github/workflows/release.yml`).
	- The release workflow reads the package version from `render_notify/_version.py` and creates a Git tag `vX.Y.Z` and a GitHub Release (skipping tag creation if the tag already exists).

- Versioning:
	- The single source of truth is `render_notify/_version.py` (`__version__ = "X.Y.Z"`).
	- `bl_info['version']` is derived from `_version.py` at import time.
	- Use `bump2version` (configured via `.bumpversion.cfg`) to bump versions, commit, and create tags consistently.

Quick commands (using the project's venv):

```bash
# create + activate venv (optional)
python3 -m venv .venv
source .venv/bin/activate

# run tests
./.venv/bin/python -m pytest -v

# run coverage and produce HTML report
./.venv/bin/python -m pytest --cov=render_notify --cov-report=term-missing --cov-report=html

# bump the version (patch/minor/major)
./.venv/bin/bump2version patch
```


