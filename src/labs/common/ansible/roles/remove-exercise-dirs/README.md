Role Name
=========

Use this role to delete exercise content from /home/student/SKU/labs and /home/student/SKU/solutions.

One benefit of this role is that it uses the lsof command to check if a user is in the directory (or subdirectory) that it plans to delete. Exercise instructions should have a step where the user changes out of the exercise directory before running the lab finish script. If a user is in the directory (or subdirectory), this role generates an error message and does not delete the directory.

Do not use this role if you want the exercise labs and solutions directories to remain after the user runs the lab finish script.

Courses using this role:
  - DO370

Requirements
------------

If using "become: True" in your playbook, ensure that the user (probably student) has sudo access without requiring a password.

Role Variables
--------------

      base_dir: This variable (defined in vars/main.yml) sets the base directory path for this role. It starts with /home/student and then uses the RHT_COURSE line in /etc/rht to set an upper-case SKU. For example, if /etc/rht contains "RHT_COURSE=do370", base_dir will have a value of "/home/student/DO370".

      exercise:
        name: This value is used with base_dir to identify the exercise directory.
        dirs:
          - labs # Delete the labs subdirectory.
          - solutions # Delete the solutions subdirecdtory.

Example:
      
      exercise:
        name: internal-cli
        dirs:
          - labs
          - solutions

You might define all exercises in the localhost inventory file. Definining the variables like this allows you to use a single playbook to delete the labs and solutions directories for any exercise.

    # Exercises can be defined in inventory/host_vars/localhost

    exercises:
      internal_cli:
        name: internal-cli
        dirs:
          - labs
          - solutions
    
      internal_gui:
        name: internal-gui
        dirs:
          - labs

Dependencies
------------

None

Example Playbook
----------------

Assuming the following example playbook exists in ansible/common/remove-exercise-dirs.yml, the following item can be added to the python script. This would remove the /home/student/labs/internal-cli/ and /home/student/solutions/internal-cli/ directories.

Example python item:

    {
        "label": "Removing exercise content",
        "task": self.run_playbook,
        "playbook": "ansible/common/remove-exercise-dirs.yml",
        "vars": {"exercise": "{{ exercises['internal_cli'] }}"},
        "fatal": True
    },

Example playbook:

    - name: Remove exercise directories
      hosts: localhost
      become: True
      gather_facts: False
      roles:
        - role: remove-exercise-dirs
            

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
