* Decide on a version number (semantic versioning)
* Update the `CHANGELOG.md`
* Update the version number in `setup.py`

```bash
# Create a tag for the new version
git tag -a vX.Y.Z -m vX.Y.Z
git push origin vX.Y.Z

# Compile release
python setup.py build sdist
```

* Create a release on GitHub
  * Create from the existing tag
  * Upload the `dist/blendplot-X.Y.Z.tar.gz` file

```
# Publish to PyPI
python -m twine upload dist/*
```
