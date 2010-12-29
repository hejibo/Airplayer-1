import os
import resource

def clear_folder(folder):
    """
    Remove the given folder's content.
    """
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e
            
def clean_hostname(hostname):
    """
    Remove the .local appendix of a hostname.
    """
    if hostname:
        return hostname.replace('.local', '')
        
"""
The following code is originating from Gunicorn:
https://github.com/benoitc/gunicorn
"""        
        
MAXFD = 1024
if (hasattr(os, "devnull")):
   REDIRECT_TO = os.devnull
else:
   REDIRECT_TO = "/dev/null"        
        
def get_maxfd():
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if (maxfd == resource.RLIM_INFINITY):
        maxfd = MAXFD
    return maxfd
            
def daemonize():
    """\
    Standard daemonization of a process. Code is basd on the
    ActiveState recipe at:
        http://code.activestate.com/recipes/278731/
    """
       
    if os.fork() == 0: 
        os.setsid()
        if os.fork() != 0:
            os.umask(0) 
        else:
            os._exit(0)
    else:
        os._exit(0)

    maxfd = get_maxfd()

    # Iterate through and close all file descriptors.
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:	# ERROR, fd wasn't open to begin with (ignored)
            pass

    os.open(REDIRECT_TO, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)        