import ConfigParser
import os.path
import io

class Config(object):


    PACKAGE_CONFIG_FILE = 'config.cnf'
    DEFAULT_CONFIG_FILE = os.path.expanduser('~/') + '.rpm.cnf'

    _instance = None
    _config   = None

    def __new__(cls, *args, **kwargs):
        """ Singleton, the python way
        """
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(
                                cls, *args, **kwargs)

            config = ConfigParser.RawConfigParser(allow_no_value=True)

            if os.path.isfile(Config.DEFAULT_CONFIG_FILE):
                config.read(io.BytesIO(Config.DEFAULT_CONFIG_FILE))
            else:
                config.read(io.BytesIO(Config.PACKAGE_CONFIG_FILE))

            cls._config = config

        return cls._instance

    def g(self, section, option):
        return self._config.get(section, option)

    def s(self, section, option, value):
        if not self._config.has_section(section):
            self.a(section)
        return self._config.set(section, option, value)

    def a(self, sections):
        if isinstance(sections, list):
            for section in sections:
                self._config.add_section(section)
        else:
            self._config.add_section(sections)

    def exist(self):
        if os.path.isfile(Config.DEFAULT_CONFIG_FILE):
            return True
        if os.path.isfile(Config.PACKAGE_CONFIG_FILE):
            return True
        return False
