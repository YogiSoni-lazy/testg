# Distributing the Framework to the Student

## Concepts

This training module includes the following concepts:

- Infrastructure for PyPI servers

- Accessing the Nexus PyPI server

- How the course package is installed on the classroom workstation

- How to implement hot fixes on a published course

- Versioning guidelines

### PyPI Server Infrastructure

1.  Nexus

    1.  Production

    2.  Stage

2.  backups

3.  failover

### Using the Nexus PyPI Server

1.  Browsing Packages

2.  Logging in as Administrator

3.  Deleting Packages

### Workstation Configuration

The following are prerequisites for the lab grading framework. Verify
the following: .. Python 3.6 or higher .. Python virtual environment ..
Pip3 .. bash-completion package . Course Package Installation . Tab
completion configuration . BYOD Considerations .. Pre-reqs .. Install
script

### Hot Fixes

1.  `lab load` command

### Versioning Guidelines

Course packages:

1.  Matching course book / exercise changes

    1.  Recommended numbering scheme

    2.  Making sure hot fixes don’t bring them into the next version of
        coursebook

Product packages:

1.  Matching product version changes

    1.  Recommended numbering scheme

    2.  Backwards compatibility

Core package:

1.  When to increase a version number

    1.  X

    2.  Y

    3.  Z

## Guided Exercise 9.1: Accessing the PyPI Server

1.  Navigate to the Nexus instance

    1.  Open a browser

    2.  Enter the appropriate URL

        - Production:
          <http://nexus-common.apps.tools-na.prod.nextcle.com>

        - Stage: <http://nexus-common.apps.tools.dev.nextcle.com>

2.  Select `Sign in` in the upper right corner.

    1.  Use `admin` as the username.

    2.  Contact your DLE for the password.

    3.  Click `Sign in`.

3.  Browse the packages in the `labs` PyPI library

    1.  Click `Browse` on the left hand panel.

    2.  Click on `labs` in the Browse list.

    3.  Click on the plus symbol next to `rht-labs-core`.

    4.  Note the versions of that package that are stored here.

4.  Manage the packages in the PyPI server

    1.  Click on Search \| PyPI in the left hand panel.

    2.  Notice the list of packages stored here.

    3.  Notice the multiple lines for `rht-labs-core`.

    4.  Click on one of the `rht-labs-gl006` packages that you uploaded.

    5.  If you have uploaded a version of this package, you may use the
        `Delete component` button to delete it.

        <div class="note">

        Do not delete any package that you did not upload as a test
        package.

        </div>

5.  Log out of Nexus

    1.  Click `Sign out` in the upper right corner of the page.

## Guided Exercise 9.2: Installing on the Workstation

1.  Allocate a classroom (usually on ROL Stage)

2.  SSH into the workstation

## Guided Exercise 9.3: Installing on BYOD

**FIXME**

