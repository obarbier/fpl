import os
import shlex
import subprocess


def build_waitress_command(opts, host, port):
    opts = shlex.split(opts) if opts else []
    return ['waitress-serve'] + \
        opts + [
        "--host=%s" % host,
        "--port=%s" % port,
        "--ident=fplsupercharge",
        "fplsupercharge.server:create_app()"
    ]


def build_gunicorn_command(opts, host, port, workers):
    bind_address = "%s:%s" % (host, port)
    opts = shlex.split(opts) if opts else []
    return ["gunicorn"] + \
        opts + [
            "-b",
            bind_address,
            "-w",
            "%s" % workers,
            "fplsupercharge.server:create_app()"]


class ShellCommandException(Exception):
    pass


def exec_cmd(cmd, throw_on_error=True, env=None, stream_output=True,
             cwd=None, cmd_stdin=None,
             **kwargs):
    """
    Runs a command as a child process.
    A convenience wrapper for running a command from a Python script.
    Keyword arguments:
    cmd -- the command to run, as a list of strings
    throw_on_error -- if true, raises an Exception if the exit code of the
    program is nonzero
    env -- additional environment variables to be defined when running the
    child process
    cwd -- working directory for child process
    stream_output -- if true, does not capture standard output and error;
    if false, captures these
      streams and returns them
    cmd_stdin -- if specified, passes the specified string as stdin to the
    child process.
    Note on the return value: If stream_output is true, then only the exit
    code is returned. If
    stream_output is false, then a tuple of the exit code, standard output and
    standard error is
    returned.
    """
    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)

    if stream_output:
        child = subprocess.Popen(cmd, env=cmd_env, cwd=cwd,
                                 universal_newlines=True,
                                 stdin=subprocess.PIPE, **kwargs)
        child.communicate(cmd_stdin)
        exit_code = child.wait()
        if throw_on_error and exit_code != 0:
            raise ShellCommandException("Non-zero exitcode: %s" % (exit_code))
        return exit_code
    else:
        child = subprocess.Popen(
            cmd, env=cmd_env, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd, universal_newlines=True, **kwargs)
        (stdout, stderr) = child.communicate(cmd_stdin)
        exit_code = child.wait()
        if throw_on_error and exit_code != 0:
            raise ShellCommandException(
                "Non-zero exit code: %s\n\nSTDOUT:\n%s\n\nSTDERR:%s" %
                (exit_code, stdout, stderr))
        return exit_code, stdout, stderr
