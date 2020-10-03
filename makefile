help:
	$(info * deployment:  build, publish, publish-test)
	$(info * versioning:  bump-patch, bump-minor, bump-major)
	$(info * setup:       venv)

clean-build:
	$(info * cleaning build files)
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__
	@rm -rf stonky.egg-info build dist

clean-venv:
	$(info * removing venv files)
	@deactivate 2> /dev/null || true
	@rm -rf venv

clean: clean-build clean-venv


# Deployment Helpers -----------------------------------------------------------

build: clean-build
	$(info * building distributable)
	@python3 setup.py sdist bdist_wheel --universal > /dev/null

publish: build
	$(info * publishing to PyPI repository)
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*.whl

publish-test: build
	$(info * publishing to PyPI test repository)
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl


# Version Helpers --------------------------------------------------------------

bump-patch:
	$(info * resetting any current changes)
	git reset --
	$(info * bumping patch version)
	@vbump --patch
	git add stonky/__version__.py
	$(info * commiting version change)
	git commit -m "Patch version bump"
	$(info * creating tag)
	git tag `vbump | egrep -o '[0-9].*'`

bump-minor:
	$(info * resetting any current changes)
	git reset --
	$(info * bumping minor version)
	vbump --minor
	git add stonky/__version__.py
	$(info * commiting version change)
	git commit -m "Minor version bump"
	$(info * creating tag)
	git tag `vbump | egrep -o '[0-9].*'`

bump-major:
	$(info * resetting any current changes)
	git reset --
	$(info * bumping major version)
	vbump --major
	git add stonky/__version__.py
	$(info * commiting version change)
	git commit -m "Major version bump"
	$(info * creating tag)
	git tag `vbump | egrep -o '[0-9].*'`


# Setup Helpers ----------------------------------------------------------------

venv: clean-venv
	$(info * initializing venv)
	@python3 -m venv venv
	$(info * installing dev requirements)
	@./venv/bin/pip install -qU pip
	@./venv/bin/pip install -qr requirements-dev.txt
