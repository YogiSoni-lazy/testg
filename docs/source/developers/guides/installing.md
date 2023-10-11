# Installing DynoLabs Libraries in Courses

DynoLabs courses depend on the `rht-labs-core` package, which is the core DynoLabs framework.
This package, and others like `rht-labs-ocpcli`, are available in the Red Hat Training PyPI servers.

There are servers available for production and development.
See the full list in the [PyPI document](../../infrastructure/pypi.md).

Because we do not publish these packages to the default PyPI (https://pypi.org/) server, you must tell `pip` to also search for packages in our PyPI servers, by using the `--extra-index-url` parameter

For example, considering that you have already created a virtual environment for your course at `classroom/grading/.venv`, you can install the dependencies of your course-specific `rht-labs-<sku>` package as follows:

```console
$ cd ~/courses/SKU/classroom/grading
$ source .venv/bin/activate
(.venv) $ pip install -e . \
--extra-index-url https://pypi.apps.tools-na.prod.nextcle.com/repository/labs/simple/
```

You can also use the same parameter to install a specific DynoLabs library.

```console
(.venv) $ pip install rht-labs-ocpcli \
--extra-index-url https://pypi.apps.tools-na.prod.nextcle.com/repository/labs/simple/
```

