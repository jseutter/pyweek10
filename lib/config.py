"""Configuration parameters stored in a module namespace.

This file is loaded during the program initialisation before the main module is
imported. Consequently, this file must not import any other modules, or those
modules will be initialised before the main module, which means that command
line options may not have been registered.

Parameters come in two types, those that are stored in the config file and those
that aren't. Running the profiler is an example of the former; fullscreen mode
would be an example of the latter.

Just because an option is stored in the config file doesn't mean it can't also
be changed by, for example, a command line switch. But doing so should not
alter the config file's value.

The `save_option` method is used to alter a value here and in the config file.
It can only be called for a predefined list of options. The `save_all` method
should probably not be used. It will write all current values for config file
parameters to the config file.

"""

# IMPORTANT!
# Never do "from config import ...". This module relies on manipulation of its
# own namespace to work properly.
__all__ = []


class LocalConfig(object):
    """Manager for the local config file.

    """

    def __init__(self, **defaults):
        """Create a LocalConfig object.

        Keyword arguments define the import local config options and their
        default values.

        """
        self.defaults = defaults
        self.locals = dict(defaults)
        self.load()

    @property
    def config_path(self):
        """The path to the local user config file.

        """
        import constants, os, pyglet
        config_dir = pyglet.resource.get_settings_path(constants.CONFIG_NAME)
        if not os.path.exists(config_dir): os.makedirs(config_dir)
        config_path = os.path.join(config_dir, "local.py")
        open(config_path, "a").close()
        return config_path

    def load(self):
        """Read the config file.

        """
        config_scope = {}
        exec open(self.config_path) in config_scope
        for name in self.defaults:
            value = config_scope.get(name, self.defaults[name])
            self.locals[name] = globals()[name] = value

    def save(self):
        """Write the config file.

        """
        config_fd = open(self.config_path, "w")
        for key in self.defaults:
            value = self.locals[key]
            if value != self.defaults[key]:
                line = "%s = %r\n" % (key, value)
                config_fd.write(line)
        config_fd.close()

    def save_option(self, name, value=None):
        """Change an option in the config file.

        :Parameters:
            `name` : str
                The name of the option to save.
            `value` : object
                The value to set.

        """
        assert name in self.defaults
        if value is not None:
            globals()[name] = value
        self.locals[name] = globals()[name]
        self.save()

    def save_all(self):
        """Save all current values to the config file.

        """
        for name in self.defaults:
            self.locals[name] = globals()[name]
        self.save()


# Default values for non-persistent options.
profile = False

# Default values for persistent options.
local = LocalConfig(
    fullscreen = True,
    width = 800,
    height = 600,
)

# See the module docstring for details of these methods.
save_option = local.save_option
save_all = local.save_all

# Clean up the module namespace.
del local, LocalConfig
