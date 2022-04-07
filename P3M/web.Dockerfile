FROM p1m
MAINTAINER Yoku Tamotsu <yoku-tamotsu@merce>

# Setting frontend Noninteractive
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

#===== PACKAGES ========================================================

RUN apt update ; \
	apt install -y pip iputils-ping
	
	
#===== EXTRA PYTHON LIBS ===============================================

RUN pip install httplib2


#===== OVPN SUPERVISOR =================================================

RUN mv /usr/sbin/openvpn /usr/sbin/openvpn-real
COPY python-openvpn-supervisor/pos.py /usr/sbin/openvpn
RUN chmod +x /usr/sbin/openvpn
