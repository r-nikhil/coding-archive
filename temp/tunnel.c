#include "config.h"

#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <syslog.h>
#include <errno.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#include <sys/ioctl.h>
#include <sys/socket.h>


//  create a tunnel. give the file descriptor back

int create_tunnel(char *dev)
{
    char tun[14];
    int i, fd;
    if( *dev ) {
       sprintf(tun, "/dev/net/%s", dev);
       return open(tun, O_RDWR);
    }
    for(i=0; i < 255; i++){
       sprintf(tun, "/dev/net/tun%d", i);
       if( (fd=open(tun, O_RDWR)) > 0 ){
          sprintf(dev, "tun%d", i);
          return fd;
       }
    }
    return -1;
}

int close_tunnel(int fd, char *dev)
{
    return close(fd);
}

//write to the tunnel

int write_tunnel(int fd, char *buf, int len)
{
    return write(fd, buf, len);
}

// read from tunnel

int read_tunnel(int fd, char *buf, int len)
{
    return read(fd, buf, len);
}
