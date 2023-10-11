# Contributing to Other DynoLabs Shared Libraries

As well as `rht-labs-core`, DynoLabs includes shared libraries that
provide tools to control specific technologies, such as [`rht-labs-ocpcli`](https://github.com/RedHatTraining/rht-labs-ocpcli).

To contribute to these libraries, read their README files, available at the repository of each library.

## Creating New Libraries

If you need to create a new library, follow these guidelines.

* Create the library repository as `https://github.com/RedHatTraining/rht-labs-<product>`.
* Call the Python package `rht-labs-<product>`.
* Choose a name for the main module of the library that is less prone to collisions.
For example, `rht-labs-ocpcli` exposes the `ocpcli` module.
You might also consider prefixing the module name with `rht_`.