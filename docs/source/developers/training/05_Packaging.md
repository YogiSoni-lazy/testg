# Packaging concepts (Core, Product, and Course)

## Concepts

There are three principal concepts the developer must know while working
on the development of a course.

Core library  
The core library contains the files necessary to deploy the framework
you are working on (in this case, the Lab Grading Framework). The core
library is found at <https://github.com/RedHatTraining/rht-labs-core>.

Product library  
The product library contains the files necessary to create a shared
library for a given product, such as OpenShift Container Platform. Code
in the product library should include common functions that can be used
across multiple courses which use the technology. One example of a
product library is found at
<https://github.com/RedHatTraining/rht-labs-ocp>.

Course  
The course contains the lab files for the course exercises. The course
relies on the core library and typically one or more product libraries.
If the product library contains Ansible roles, then the course is the
implementation of those roles. For this training, the example course is
either **rht-labs-gl006** or **rht-labs-gl007**.

## Makefile targets

The default target for `make` is `build`.

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><code>make venv</code></p></td>
<td style="text-align: left;"><p>This option creates the Python
<em>virtual environment</em> and installs the dependencies listed in the
<code>requirements.txt</code> file.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>make clean</code></p></td>
<td style="text-align: left;"><p>This options deletes the files of the
installed core framework by executing <code>rm -rf</code> on
<code>dist</code>, <code>build</code>, <code>.eggs</code> and
<code>*.egg-info</code>, so you can reinstall the framework if a
necessary file is missing or changes were applied, and you want to get
the original files and its contents.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>make distclean</code></p></td>
<td style="text-align: left;"><p>This option calls
<code>make clean</code> first and then removes the Python <em>virtual
environment</em> directory.</p>
<div class="note">
<p>You must execute <code>deactivate</code> <strong>before</strong>
running <code>make clean</code>.</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>make lint</code></p></td>
<td style="text-align: left;"><p>This option calls the linter to check
for syntax errors.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>make build</code></p></td>
<td style="text-align: left;"><p>This option comes as the default one
when running the <code>make</code> command without an argument.</p>
<p>It first calls the <code>clean</code> target to delete the installed
core framework files if they exist, and then it executes
<code>setup.py sdist</code> to create the source distribution
package.</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>make publish-stage</code></p></td>
<td style="text-align: left;"><p>This option installs a clean core
framework, creates the source distribution package, and uploads the
package to the testing PyPi server.</p>
<p>The <code>make publish-stage</code> command calls the
<code>clean</code> target to delete the installed core framework files
if they exist, and then it calls the <code>build</code> target to create
the <em>source distribution package</em>.</p>
<p>Finally, it uploads the package to the testing PyPi server indicated
in the <code>Makefile</code>.</p>
<div class="note">
<p>You must set the <code>PS_PASSWD</code> environment variable
<strong>before</strong> executing <code>make publish-stage</code></p>
</div></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>make publish-prod</code></p></td>
<td style="text-align: left;"><p>This option installs a clean core
framework, creates the source distribution package, and uploads the
package to the production PyPi server.</p>
<p>The <code>make publish-prod</code> command calls the
<code>clean</code> target to delete the installed core framework files
if they exist, and then it calls the <code>build</code> target to create
the <em>source distribution package</em>.</p>
<p>Finally, it uploads the package to the production PyPi server
indicated in the <code>Makefile</code>.</p>
<div class="note">
<p>You must set the <code>PS_PASSWD_PROD</code> environment variable
<strong>before</strong> executing <code>make publish-prod</code></p>
</div></td>
</tr>
</tbody>
</table>

<div class="note">

**Do not add the PyPi server password to the `Makefile`**.

- You must set the `PS_PASSWD` environment variable **before** executing
  `make publish-stage`

- You must set the `PS_PASSWD_PROD` environment variable **before**
  executing `make publish-prod`

Either run `export PS_PASSWD=<PASSWORD>` or
`export PS_PASSWD_PROD=<PASSWORD>` from the command line, or add the
appropriate line to your `~/.bashrc` file.

Contact your DLE for the password.

</div>

## Configuration files

`setup.cfg`  
It contains the metadata used to know which code files needs to be
included in the packaging process, and also tells the `setuptools` (the
library containing the necessary functions to create python packages and
publish them into PyPi repository) some important data of our package,
like its name, the version, the platform, project URLs, dependencies,
etc.

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><code>[metadata]</code></p></td>
<td style="text-align: left;"><p>Contains basic info such as the name of
the project (labs), the project source code URL (github) and some
classifiers (used to give more information about the package to the
<strong>index</strong> and <code>pip</code> tool) like the Operating
System it can runs on (MacOS X, Windows and POSIX).</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>[options]</code></p></td>
<td style="text-align: left;"><p>Indicates to include the packages under
the directory defined in the <code>[options.packages.find]</code> option
(in this case <code>rht-labs-core/src</code>).</p>
<p>It also indicates the install and python requirements.</p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>[options.entry_points]</code></p></td>
<td style="text-align: left;"><p>Indicates the installation of the
<code>lab</code> script which will invoke the <code>main</code>
function.</p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>[options.packages.find]</code></p></td>
<td style="text-align: left;"><p>It defines the directories to be used
in the <code>[options]</code> section.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>[sdist]</code></p></td>
<td style="text-align: left;"><p>Indicates the distribution format (in
this case, <code>gztar</code>).</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>[bdist_wheel]</code></p></td>
<td style="text-align: left;"><p>Indicates the built package (wheel
type) is purely Python by setting the <code>universal</code> value to
<code>true</code>.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>[flake8]</code></p></td>
<td style="text-align: left;"><p>Defines the use of the lint
<code>flake8</code> wrapper for the Python code.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>[tool:pytest]</code></p></td>
<td style="text-align: left;"><p>It defines the <code>pytest</code> tool
available to create and run small tests.</p></td>
</tr>
</tbody>
</table>

`setup.py`  
It contains the global `setup()` function, which calls the `version`
function from the `src.labs.version` library. This function obtains the
Python module version.

`version.py`  
It contains the version of the module. This file is called by `setup.py`
in its `setup()` function. This file is located inside `src` directory.

`MANIFEST.in`  
It contains the definitions of files that need to be added or excluded
into the packaging process. In this case, are excluded file that are not
needed (these files were added by default by `setuptools-scm`), and
included all the `sh` files.

`README.md`  
It contains the general information about the library, such as the
purpose and a reference to the development guide. This file is called in
the `[metadata]` section of the `setup.cfg` file to provide more
information to the `setuptools` library.

`LICENSE`  
It contains the Copyright license for the `rht-labs-core` library. This
file is called in the `[metadata]` section of the `setup.cfg` file to
provide more information to the `setuptools` library.

## Next Steps

The next training module will help you to create your first laboratory
script using Python.

