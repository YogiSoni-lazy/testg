# Releasing `rht-labs-core`
The lab framework is delivered as Python packages by using Python index severs (PyPI).
We use Nexus PyPI servers to publish and deliver grading packages.
The following servers are used.

```{include} ../_templates/pypi_servers.md
```

## Versioning

This package follows a **semantic versioning** approach.

The version is specified in the `src/labs/version.py` file.



:::{admonition} **Do not edit the `rht-labs-core` version file!**
:class: danger

Instead, [build the Jenkins pipeline](https://jenkins.prod.nextcle.com/blue/organizations/jenkins/rht-labs-core/branches)
to create and release new versions. Jenkins will modify the version file
and create new tags.
:::



## Releases to PyPI Stage

Jenkins pushes a development version for each new Pull Request to [PyPI
Stage](https://pypi.apps.tools.dev.nextcle.com/#browse/browse:labs).

The development version follows the `X.Y.Z.dev${PR-number}` format,
where `X.Y.Z` is the semantic version specified in the
`src/labs/version.py` file.

Example:

    YOU open the Pull Request #23 ----> Jenkins creates a "X.Y.Z.devPR-23" dev version ----> Jenkins pushes the version to PyPI Stage

Releases to PyPI Stage do not modify the version file.

Development versions can be installed as any other version, for example:

``` sh
pip install rht-labs-core==2.0.9.devPR-23 --extra-index-url https://pypi.apps.tools-na100.dev.ole.redhat.com/repository/labs/simple
```

## Releasing to PyPI Prod

To release to Prod:

1.  Go to: **[Release to
    PROD](https://jenkins.prod.nextcle.com/job/Dynolabs/job/rht-labs-core/job/master/build)**

2.  Select the `VersionBump` increment (major\|minor\|patch). Jenkins
    will modify the version file, create a Git tag with the version, and
    push the changes to the master branch.

3.  Select `Publish`. This will make Jenkins push the new version to
    PyPI Prod, and create a new GitHub release.

4.  Click `Build`.

5.  Watch the build on Blue Ocean and confirm the version bump.

    The prompt times out if you don’t confirm quickly. If the prompt
    times out, then rerun the job without bump, checking the publish
    option.

6.  Go to [the releases page on
    GitHub](https://github.com/RedHatTraining/rht-labs-core/releases).
    Edit the last release. Use `Auto-generate release notes`. Click
    `Update release`.

:::{note}
You can only release to PROD from to the master branch
:::

