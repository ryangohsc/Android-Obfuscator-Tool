import os
from contextlib import contextmanager


# Adapted from https://www.zopatista.com/python/2013/11/26/inplace-file-rewriting/
@contextmanager
def inplace_edit_file(filename):
    """
    Allow for a file to be replaced with new content.
    Yield a tuple of (readable, writable) file objects, where writable replaces
    readable. If an exception occurs, the old file is restored, removing the
    written data.
    """

    backup_filename = "{0}{1}{2}".format(filename, os.extsep, "bak")

    try:
        os.unlink(backup_filename)
    except OSError:
        pass
    os.rename(filename, backup_filename)

    readable = open(backup_filename, "r", encoding="utf-8")
    try:
        perm = os.fstat(readable.fileno()).st_mode
    except OSError:
        writable = open(filename, "w", encoding="utf-8", newline="")
    else:
        os_mode = os.O_CREAT | os.O_WRONLY | os.O_TRUNC
        if hasattr(os, "O_BINARY"):
            os_mode |= os.O_BINARY
        fd = os.open(filename, os_mode, perm)
        writable = open(fd, "w", encoding="utf-8", newline="")
        try:
            if hasattr(os, "chmod"):
                os.chmod(filename, perm)
        except OSError:
            pass
    try:
        yield readable, writable
    except Exception as e:
        try:
            os.unlink(filename)
        except OSError:
            pass
        os.rename(backup_filename, filename)
        raise
    finally:
        readable.close()
        writable.close()
        try:
            os.unlink(backup_filename)
        except OSError:
            pass
