* Decide on a version number (semantic versioning)
* Update the `CHANGELOG.md`
* Update the version number in `setup.py`

```bash
# Compile release
python setup.py build sdist

# Publish to PyPI
python -m twine upload dist/*
```
