#ifndef _INTERFACE_H_
#define _INTERFACE_H_

struct eth_addr {
  unsigned char addr[6];
};


typedef struct {
	struct eth_addr 	mac_addr;
	struct eth_addr 	dst_addr;
	unsigned char 		mag_enc[3];
	unsigned char 		valve_power;
	signed char   		valve_dir;
	float				p_gain;
	float				i_gain;
	float				d_gain;
} interface_struct;

#endif