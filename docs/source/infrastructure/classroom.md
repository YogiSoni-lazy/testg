# Installation of DynoLabs in the Classroom Workstation

:::{caution}
This section might be outdated and requires further review.
:::

The best way to see how the framework is installed in the classroom is
to look at the Ansible code in `infrastructure/classroom`. The
installation has the following characteristics:

- Python 3 and supporting packages are installed via RPMs at the OS
  level.

- The relevant course package, e.g. `rht-labs-gl006`, is installed in a
  Python virtual environment.

  The location of this Python virtual environment is
  `/home/student/.venv/labs`. The package dependencies bring in the core
  library so that the `lab` command exists.

- The path to the virtual environment `bin`, where the `lab` command is
  installed, is added to the students path.

  This is done by dropping a script that appends to the PATH in
  `/etc/profile.d`. This keeps the student from needing to activate the
  Python virtual environment.

- The `lab` command is executed to `select` the course SKU.

  This makes sure that the student can use the lab scripts for the given
  course out of the box.

- The tab completion script is generated and places in
  `/etc/bash_completion.d`.

  The necessary RPM for bash completion is installed. The
  `lab completion bash` command is executed to produce the tab
  completion script.

- Version locking for `lab upgrade` is put in place in the `/etc/rht`
  file.

  A new variable is added to `/etc/rht` that specifies the valid version
  ranges for this course. Typically that is greater than or equal to x.y
  and less than x.y+1. The rule is: y version should be incremented when
  a new version of the course is created. For example, OCP 4.5 of course
  `GL006` should have a version lock of `>=0.1<0.2`. OCP 4.6 of course
  `GL006` should have a version lock of `>=0.2<0.3`. The z stream can be
  bumped throughout the lifetime of the course version to provide hot
  fixes.

  Version locking ensures that the student cannot upgrade into the next
  major version of the course. This could be a problem because most
  likely the lab instructions will no longer work with the next version
  of the course.
