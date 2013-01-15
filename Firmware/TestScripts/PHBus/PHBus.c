#include <arpa/inet.h>
#include <linux/if_packet.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <net/if.h>
#include <netinet/ether.h>
#include <unistd.h>
 
#define DEFAULT_IF "lo"

#define MY_DEST_MAC0 0
#define MY_DEST_MAC1 0
#define MY_DEST_MAC2 0
#define MY_DEST_MAC3 0
#define MY_DEST_MAC4 0
#define MY_DEST_MAC5 0

#define ETHER_TYPE 0x0800
#define BUF_SIZ 1500

// Hexapod bus packet header
struct PHEtherHeader{
    unsigned char ether_dhost[6];
    unsigned char ether_shost[6];
    unsigned char magic_word;
    unsigned char cmd_id;
    unsigned short packet_id;
};

struct PHStreamHeader{
    unsigned short len;
};

int main(int argc, char *argv[])
{
    int    sockfd;
    struct ifreq if_idx;
    struct ifreq if_mac;
    int    tx_len = 0;
    char   sendbuf[BUF_SIZ];
    struct ether_header *eh = (struct ether_header *) sendbuf;
    struct iphdr *iph = (struct iphdr *) (sendbuf + sizeof(struct ether_header));
    struct sockaddr_ll socket_address;
    char   ifName[IFNAMSIZ];

    fd_set read_set;
    fd_set write_set;
    struct timeval timeout;

    struct ifreq ifopts;    /* set promiscuous mode */
    int sockopt;
    uint8_t buf[BUF_SIZ];
    int numbytes;

    struct PHStreamHeader stream_header;
    char str_buf[128];

    int rc, i;

    /* Get interface name */
    if (argc > 1)
        strcpy(ifName, argv[1]);
    else
        strcpy(ifName, DEFAULT_IF);
     
    /* Open RAW socket to send on */
    if ((sockfd = socket(PF_PACKET, SOCK_RAW, htons(ETHER_TYPE))) == -1) {
        perror("socket");
    }
    /* Set interface to promiscuous mode - do we need to do this every time? */
    strncpy(ifopts.ifr_name, ifName, IFNAMSIZ-1);
    ioctl(sockfd, SIOCGIFFLAGS, &ifopts);
    ifopts.ifr_flags |= IFF_PROMISC;
    ioctl(sockfd, SIOCSIFFLAGS, &ifopts);
    /* Allow the socket to be reused - incase connection is closed prematurely */
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &sockopt, sizeof sockopt) == -1) {
        perror("setsockopt");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    /* Bind to device */
    if (setsockopt(sockfd, SOL_SOCKET, SO_BINDTODEVICE, ifName, IFNAMSIZ-1) == -1)  {
        perror("SO_BINDTODEVICE");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
     
    /* Get the index of the interface to send on */
    memset(&if_idx, 0, sizeof(struct ifreq));
    strncpy(if_idx.ifr_name, ifName, IFNAMSIZ-1);
    if (ioctl(sockfd, SIOCGIFINDEX, &if_idx) < 0)
        perror("SIOCGIFINDEX");
    /* Get the MAC address of the interface to send on */
    memset(&if_mac, 0, sizeof(struct ifreq));
    strncpy(if_mac.ifr_name, ifName, IFNAMSIZ-1);
    if (ioctl(sockfd, SIOCGIFHWADDR, &if_mac) < 0)
        perror("SIOCGIFHWADDR");
     
    /* Construct the Ethernet header */
    memset(sendbuf, 0, BUF_SIZ);
    /* Ethernet header */
    eh->ether_shost[0] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[0];
    eh->ether_shost[1] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[1];
    eh->ether_shost[2] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[2];
    eh->ether_shost[3] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[3];
    eh->ether_shost[4] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[4];
    eh->ether_shost[5] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[5];
    eh->ether_dhost[0] = MY_DEST_MAC0;
    eh->ether_dhost[1] = MY_DEST_MAC1;
    eh->ether_dhost[2] = MY_DEST_MAC2;
    eh->ether_dhost[3] = MY_DEST_MAC3;
    eh->ether_dhost[4] = MY_DEST_MAC4;
    eh->ether_dhost[5] = MY_DEST_MAC5;
    /* Ethertype field */
    eh->ether_type = htons(ETH_P_IP);
    tx_len += sizeof(struct ether_header);
     
    /* Packet data */
    sendbuf[tx_len++] = 0xde;
    sendbuf[tx_len++] = 0xad;
    sendbuf[tx_len++] = 0xbe;
    sendbuf[tx_len++] = 0xef;
     
    /* Index of the network device */
    socket_address.sll_ifindex = if_idx.ifr_ifindex;
    /* Address length*/
    socket_address.sll_halen = ETH_ALEN;
    /* Destination MAC */
    socket_address.sll_addr[0] = MY_DEST_MAC0;
    socket_address.sll_addr[1] = MY_DEST_MAC1;
    socket_address.sll_addr[2] = MY_DEST_MAC2;
    socket_address.sll_addr[3] = MY_DEST_MAC3;
    socket_address.sll_addr[4] = MY_DEST_MAC4;
    socket_address.sll_addr[5] = MY_DEST_MAC5;
    
    while( 1 )
    {
        // Construct the file descriptor set we will check in the main loop
        FD_ZERO(&read_set);
        FD_SET( sockfd, &read_set );
        FD_SET( STDIN_FILENO, &read_set );
        // Set the timeout to 1 second
        timeout.tv_sec  = 1;
        timeout.tv_usec = 0;
        rc = select( sockfd+1, //Max FD in any of the sets +1
                &read_set,     // Watch for available data
                NULL,          // Watch for capacity to be written
                NULL,          // Watch for exceptions
                &timeout );    // How long until timeout
        if(rc==0)
        {
            printf("select timed out...\n");
        }
        else if(rc<0)
        {
            perror("select errored");
        }
        // If we've made it here, there is data to be read
        // from one or both descriptors
        //
        // Check the socket for data available
        if(FD_ISSET(sockfd, &read_set))
        {
            // Get the packet
            numbytes = recvfrom(sockfd, buf, BUF_SIZ, 0, NULL, NULL);
            struct PHEtherHeader* tmp = (struct PHEtherHeader*)buf;
            // Validate that it's the type we care about
            if(tmp->magic_word == 0x69 )
            {
                // Push a header to the stream
                stream_header.len = numbytes;
                write( STDOUT_FILENO, &stream_header, sizeof(stream_header) );
                // Push the data to the stream
                write( STDOUT_FILENO, buf, numbytes );
            }
            else {
                //snprintf(str_buf, 128, "Received %d bytes of junk", numbytes);
                //write(STDOUT_FILENO, str_buf, strlen(str_buf));
            }
        }
        // Check STDIN for data available
        if(FD_ISSET(STDIN_FILENO, &read_set))
        {
            numbytes = read(STDIN_FILENO, buf, BUF_SIZ);
            // Read the header from the stream, make sure
            // we got a whole packet
            struct PHStreamHeader* tmp = (struct PHStreamHeader*)buf;
            unsigned char* pack_start = buf + sizeof(struct PHStreamHeader);
            if(numbytes >= sizeof(struct PHStreamHeader) + tmp->len)
            {
                // Copy the target MAC
                // TODO: Why do we need to do this?  It's already in the packet
                memcpy( socket_address.sll_addr, pack_start, 6);
                // Push the data to the socket
                if (sendto(sockfd, pack_start, tmp->len, 0, (struct sockaddr*)&socket_address, sizeof(struct sockaddr_ll)) < 0)
                    perror("Send failed:");
                // On to the next packet
                numbytes -= (tmp->len + sizeof(struct PHStreamHeader));
                pack_start += tmp->len;
                tmp = (struct PHStreamHeader*)tmp;
                tmp += sizeof(struct PHStreamHeader);
            }
        }
    }
    return 0;
}
