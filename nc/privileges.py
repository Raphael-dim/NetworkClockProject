import os


def drop_privileges():
    if os.name != "nt":
        # We're assuming a Unix-like system
        import pwd, grp

        try:
            # Drop group privileges
            os.setgroups([])
            os.setgid(grp.getgrnam("nogroup").gr_gid)
            os.setuid(pwd.getpwnam("nobody").pw_uid)

            # Ensure a very conservative umask
            os.umask(0o77)
        except Exception as e:
            print(f"Failed to drop privileges: {e}")
    else:
        print("Privilege dropping not implemented for Windows")


if __name__ == "__main__":
    drop_privileges()
    