#include "config.h"

#include <fcntl.h>
#include <netinet/in.h>
#include <netinet/ip_icmp.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#include <sys/types.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

int get_icmp(int,unsigned char *,int,struct saddr_in *,socklen_t *);
int send_icmp(int,unsigned char *,int,struct saddr_in *,socklen_t);
int create_tunnel(char *dev);

int main()
{

unsigned char buff[4096];
fd_set rset;
struct saddr_in addr;
struct saddr_in addr_recv;
int soc;
int ret;
socklen_t len = sizeof(struct saddr_in);
socklen_t len_recv = sizeof(struct saddr_in);

unsigned char dev[] = "tun0";
int tunfd;

if ((tunfd = create_tunnel(dev)) < 0)
{
   perror("error creating tunnel");
   exit(1);
}

if (system(buff) < 0)
{
   perror("forking error");
   exit(1);
}

if ((soc = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)) < 0)
{
   perror("socket error");
   exit(1);
}

memset(&addr,0,sizeof(struct saddr_in));
addr.sin_family = AF_INET;
addr.sin_port = 0;
addr.sin_addr.s_addr = inet_addr(PEER_IP);

while(1)
{ 
  FD_ZERO(&rset);
  FD_SET(soc,&rset);
  FD_SET(tunfd,&rset);
  while ((ret = select(soc+1,&rset,NULL,NULL,NULL)) < 0 && errno == EINTR);
  if (ret < 0)
  {
     perror("error: select");
     exit(1);
  }
  if (FD_ISSET(soc,&rset))
  {
    if ((ret = get_icmp(soc,buff,sizeof(buff),&addr_recv,&len_recv)) > 0)
    {
       write(tunfd,buff,ret);
    }
  }
  if (FD_ISSET(tunfd,&rset))
  {
    ret = read(tunfd,buff,sizeof(buff));
    send_icmp(soc,buff,ret,&addr,len);
  }
}

return(0);
}
