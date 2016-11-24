
def cmd2msgnum(cmd):
    if type(cmd) is str:
        cmd = cmd[:2].encode()

    if len(cmd) > 1:
        return cmd[1] << 8 | cmd[0]
    else:
        return cmd[0]

