from dynaconf import Dynaconf

settings = Dynaconf(envvar_prefix="BP", settings_files=['configuration.toml'])

strings = Dynaconf(settings_files=['strings.toml'])
