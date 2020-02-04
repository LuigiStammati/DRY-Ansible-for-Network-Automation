Example:

You need to load a configuration file on your device whose hostname is "my_qfx":

1. Name the configuration file so that it ends with "my_qfx.conf" (I.e. "my_qfx.conf", "2019_08_my_qfx.conf", 
"FINALmy_qfx.conf", etc)
2. Place the file in the a folder called "_built_configs" inside the inventory folder. This is the default location, 
you can use a different folder by overriding the variables `built_configs_dir` 
3. Run the playbook