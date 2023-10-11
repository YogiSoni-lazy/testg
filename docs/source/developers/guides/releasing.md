# Releasing the Lab Scripts of a Course

Each course must publish a Python package containing its lab scripts to our [PyPI servers](../../infrastructure/pypi.md).

The release process is mostly automatic.
Jenkins takes care of this process by using our [Jenkins shared library](https://github.com/RedHatTraining/curriculum-jenkins-library/blob/main/vars/flamel.groovy) and the `classroom/grading/Makefile`.

## Naming Conventions

Name the package following the `rht-labs-<SKU>` format.
For example, for `DO378`, the package is `rht-labs-do378`.

## Versions & Releases

Use the `classroom/grading/src/SKU/version.py` file to set the package version, following a semantic release approach.

## Releasing

### Continuous Dev releases

Every change in the `main` branch is continuously published as a new development build to the PyPI servers.
Dev builds are deployed to the PyPI prod server, and are intended to be used in EA Prod.

Dev builds are versioned as `x.y.z.dev<BUILD_ID>`, where:

* `x.y.z` is read from `sku/version.py`.
* `BUILD_ID` is the Jenkins Build id.

Inspect `../Jenkinsfile-curriculum` and the [shared Jenkins library](https://github.com/RedHatTraining/curriculum-jenkins-library/blob/main/vars/flamel.groovy) for more details.

### GA releases (Releasing to Production)

For (non-EA) production GA releases, follow these steps:

1. Bump the version in `sku/version.py`.
2. Commit changes and create a PR.
3. After the PR is merged, and the new version is on `main`, trigger the Jenkins job from `https://jenkins.prod.nextcle.com/job/RHT/job/SKU/job/main/build`
4. Select the `PublishLabScripts` check box.
5. Click `Build`.
6. Wait for the pipeline to finish.

If, for some reason, you cannot run the Jenkins job, you can trigger the release from your own workstation, as follows:

```console
$ make build
$ PS_PASSWD_PROD=... make publish-prod
```

:::{note}
Normally you won't need to run `make build` locally.
Use the Jenkins pipeline at `https://jenkins.prod.nextcle.com/job/RHT/job/SKU/job/main/build` instead.
:::