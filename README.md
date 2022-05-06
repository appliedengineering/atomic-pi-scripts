# Atomic Pi Scripts

# Architecture
The atomic pi acts as a forwarder in order to forward data from the raspberry pi to users' devices.\
It utilizes a pyzmq forwarding device set in `FORWARDER` mode.

# Connection properties
Raspberry Pi Network DHCP range = `192.168.1.2 - 192.168.1.255`

Raspberry Pi PtP ip = `192.168.3.1` \
port = `5556`

Atomic Pi Network DHCP range = `192.168.4.1 - 192.168.4.255`

Atomic Pi PtP ip = `192.168.4.1`

# Forwarding properties
The atomic pi fowards data out of \
port `55563` \
ip `192.168.3.2` \
^ connect to the above settings in the applied engineering app

# Timestamp server
The atomic pi uses the following connection to forward timestamp data to the raspberry pi \
ip = `192.168.3.2`\
port = `7242`

