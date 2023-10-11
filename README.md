<h1 align="center">

<img src="docs/source/_static/DynoLabs.png" width=200px >

</h1>


This framework provides the lab grading infrastructure
for Red Hat Training courseware.
The tools in this library allow the student to grade the progress of their lab work
in their classroom lab environment.

## Documentation

The reference and usage documentation is available at [jenkins.prod.nextcle.com/userContent/dynolabs-docs/latest](https://jenkins.prod.nextcle.com/userContent/dynolabs-docs/latest/index.html)

## Developing Lab Scripts

### Training

Start learning your way around the framework with the [Lab Grading Framework Training](https://jenkins.prod.nextcle.com/userContent/dynolabs-docs/latest/developers/training/README.html).

### Scaffolding a New Project

Learn how to scaffold DynoLabs scripts in a course project with the [Quick Start Guide](https://jenkins.prod.nextcle.com/userContent/dynolabs-docs/latest/developers/quickstart.html).

### Guides

If you want to reuse the common functions of the framework in the lab scripts of a course, read the [Lab Scripts Dev Guides](https://jenkins.prod.nextcle.com/userContent/dynolabs-docs/latest/developers/guides/README.html)


### Learning Sessions

| Date       | Session                         | Topics     | Additional resources |
|------------|---------------------------------|------------|----------------------|
| 2023-06-02 | [DynoLabs introductory session for Portolio Labs](https://drive.google.com/file/d/1N-4H4JwIuGc3EMoSRvKPZzDxrPGiNoXb/view) | Getting Started |
| 2023-03-01 | Learning Content Development Teams Bi-weekly (from 4:50): [Syncing files between localhost and the lab environment for a better development workflow](https://drive.google.com/file/d/1plH2aCa8P380WKQ5ndFjpJW3S_zWKGu7/view) | Development flow | [Curriculum tools for development](https://github.com/RedHatTraining/curriculum-tools/tree/rhct) |
| 2023-02-28 | [Ansible upskilling session](https://drive.google.com/file/d/1w_3LbSTvu3ycUVlWn2KOmHAf1dCbXUCp/view) | Ansible | |
| 2022-09-16 | [Python/DynoLabs testing session](https://drive.google.com/file/d/1AtVfY_H38_StS3W1Su4ObK_Ryk2CpWRY/view?usp=drive_web)| Testing | |

### Lab Script Examples

Examples are available at the [gl006 example project](/packages-gl006/src/gl006).


## Contributing

If you are already familiar with the framework and want to start contributing to the DynoLabs core library, read the [contributing guide](https://jenkins.prod.nextcle.com/userContent/dynolabs-docs/latest/contributors/README.html).

If you are releasing a new version of `rht-labs-core`, then read the [release guide](https://jenkins.prod.nextcle.com/userContent/dynolabs-docs/latest/contributors/core_publish.html).


### TODOs

- Implement and test a small example course including course lib and product lib.
- Reporting
  - Implement a target reporting API endpoint
    +
    Implement the invocation of the API and test the integration.
    Document the preliminary JSON payload.
    Do we need to implement python package signing?
    How do we do that? Our prod packages should probably be signed.
    +
