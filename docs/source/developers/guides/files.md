# Copying Lab Files

Many lab scripts include some files that are copied to the student home directory on workstation.

The {py:func}`labs.common.fs.copy_materials_step` function helps perform this functionality.

There are many places to keep the lab files.

## Keeping the Lab Files in the Course Repo

```
import pathlib

from labs.grading import Default
from labs.common import fs


class FooBar(Default):
    __LAB__ = "foo-bar"

    def start(self):
        fs.copy_materials_step(pathlib.Path(__file__).parent / "materials", self.__LAB__, pathlib.Path.home() / "SKU123")
```

If you place the files in `classroom/grading/src/{package}/materials/{labs,solutions}/{lab-name}`, then the lab start command copies them to `/home/student/SKU123/{labs,solutions}/{lab-name}`.
