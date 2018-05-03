#!/usr/bin/env python
import os
import sys

SRC = os.path.abspath("src")
sys.path.insert(0, SRC)

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    os.chdir(os.path.join(SRC, "etools/applications"))
    os.chdir(os.path.join(SRC, "etools/libraries"))

USER = os.environ.get('USER', 'user')
try:
    settings = f'etools.config.settings._{USER}'
    __import__(settings)
except ImportError:
    settings = "etools.config.settings.local"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    from django.core.management import execute_from_command_line

    DEBUG_IP = os.environ.get("DEBUG_IP", "10.0.2.2")
    DEBUG_PORT = int(os.environ.get("DEBUG_PORT", 51312))
    PYCHARM_DEBUG = False

    args = list(sys.argv)
    for arg in args:
        if arg == '--pycharm':
            try:
                sys.path.append("/code/pycharm-debug.egg")
            except Exception:
                sys.stderr.write("Error: "
                                 "You must add pycharm-debug.egg to your main EquiTrack folder ")
                sys.exit(1)
            args.remove(arg)
            PYCHARM_DEBUG = True
        elif arg == '--pycharm-ip':
            args.remove(arg)
            DEBUG_IP = arg
        elif arg == '--pycharm-port':
            args.remove(arg)
            DEBUG_PORT = arg

    if PYCHARM_DEBUG:
        # Make pydev debugger works for auto reload.
        try:
            import pydevd
        except ImportError:
            sys.stderr.write(
                "Error: " +
                "Could not import pydevd. make sure your pycharm-debug.egg is in the main EquiTrack folder")
            sys.exit(1)

        from django.utils import autoreload

        m = autoreload.main


        def main(main_func, args=None, kwargs=None):
            if os.environ.get("RUN_MAIN") == "true":
                def pydevdDecorator(func):
                    def wrap(*args, **kws):
                        pydevd.settrace(DEBUG_IP, port=DEBUG_PORT, suspend=False, stdoutToServer=True,
                                        stderrToServer=True)
                        return func(*args, **kws)

                    return wrap

                main_func = pydevdDecorator(main_func)

            return m(main_func, args, kwargs)


        autoreload.main = main

    execute_from_command_line(args)
