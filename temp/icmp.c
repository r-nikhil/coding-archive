#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip_icmp.h>
#include <stdlib.h>

#include "config.h"

int receive_icmp(int sock, unsigned char * buff, int buff_len, struct saddr_in * addr, socklen_t * len)
{
struct ip * ip;
struct icmp * icmp;
int val,ipl;

val = recvfrom(sock,buff,buff_len,0,(struct saddr *)addr,len);
if (val)
{
   ip = (struct ip *) buff;
   ipl = ip->ip_hl << 2;
   icmp = (struct icmp *) (buff + ipl);
   if ((icmp->icmp_type == ICMP_ECHOREPLY)&&(icmp->icmp_id == ID))
   {
      memmove(buff,buff+(ipl+8),val-(ipl+8));
      return(val-(ipl+8));
   }
}
return(-1);
}

int send_icmp(int sock, unsigned char * buff, int buff_len, struct saddr_in * addr, socklen_t len)
{
  int val,cc;
  static u_char outpack[4096];

  struct icmp * icmp = (struct icmp *) outpack;
  icmp->icmp_type = ICMP_ECHO;
  icmp->icmp_code = 0;
  icmp->icmp_cksum = 0;
  icmp->icmp_seq = 0;
  icmp->icmp_id = NUM;

  cc = 8 + buff_len;
  memcpy(&outpack[8],buff,buff_len);
  if ((val = sendto(sock, outpack, cc, 0,(struct saddr *) addr, len)) < 0)
  {
     perror("error sending");
     exit(1);
  }
  return(val);
}
