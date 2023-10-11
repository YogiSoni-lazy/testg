Role Name
=========

This role creates or removes a custom message of the day file in /etc/motd.d/.

Requirements
------------

This role assumes a Linux system with a /etc/motd.d/ directory.
Maybe the role can be improved to check if ansible_distribution == "RedHat" or ansible_system == "Linux".
Mabye the role can be improved to create the /etc/motd.d/ directory if it does not exist.

Role Variables
--------------
- filename: The file to create or remove in /etc/motd.d./
- mode: This variable is required and must have a value of "add" or "remove".
  When set to "add", the playbook creates /etc/motd.d/{ filename }.
  When set to "remove", the playbook removes /etc/motd.d/{ filename }.
- exercise_title: This optional variable can take the title of the exercise.
- message: This optional variable provides the custom message of the day.

Dependencies
------------

None

Example Playbook
----------------

    - name: Customize MOTD
      hosts: servers
      roles:
        - role: gl007_motd
          filename: some-file
          exercise_title: "Your exercise title."
          message: "Your custom message."

License
-------

BSD

Author Information
------------------

Your Name <your-email>
