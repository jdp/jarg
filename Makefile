VERSION = $(shell python -c "import jarg; print '.'.join(jarg.__VERSION__)")

man/jarg.1.html: man/jarg.1.ronn
	ronn --html --style=toc --organization="jarg $(VERSION)" $<

release:
	python setup.py sdist upload -r pypi

clean:
	-rm -rf dist *.egg *.egg-info

.PHONY: release clean
