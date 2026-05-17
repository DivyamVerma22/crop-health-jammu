# Contributing

Thank you for your interest in this research repository. Although the codebase originated as a dissertation artefact, contributions that strengthen reproducibility, broaden the methodology, or improve the deployed application are very welcome.

## Reporting Issues

Please open a GitHub issue for any bug report, reproducibility failure, or methodological question. A useful report typically includes the operating system, Python version, the exact command that was run, the full traceback, and — where relevant — a minimal data sample that reproduces the behaviour.

## Proposing Changes

For non-trivial changes, please open an issue first to discuss the proposal so that effort is not duplicated. Smaller improvements such as documentation fixes, dependency bumps, or refactors of a single function can be sent directly as a pull request.

The expected workflow is to fork the repository, create a topic branch named after the change, commit with clear messages, and open a pull request against `main`. Each pull request should describe what changed and why, link to any relevant issue, and confirm that the affected notebooks or scripts still run end-to-end.

## Code Style

Python code follows standard PEP 8 conventions. Type hints are preferred where they aid clarity. Notebook cells should be re-runnable from a clean kernel, with all `pip install` lines confined to the first cell and clearly commented.

## Data and Models

Please do not commit raw satellite extractions or trained model files to the repository. The `.gitignore` file is already configured to exclude these. Large artefacts should be hosted externally and referenced through `scripts/download_model.py` or an equivalent helper.

## Conduct

Please be respectful, constructive, and patient in all interactions. This is an open academic project and good-faith engagement is assumed on all sides.
