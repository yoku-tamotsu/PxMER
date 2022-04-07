FROM mysql:8.0.28
MAINTAINER Yoku Tamotsu <yoku-tamotsu@merce>

# Setting frontend Noninteractive
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

#===== PACKAGES ========================================================

RUN apt-get update ; \
    apt-get install -y software-properties-common supervisor openvpn
	
	
#===== MYSQL ===========================================================

COPY /mysql/my.cnf /etc/mysql/my.cnf


#===== SUPERVISOR ======================================================

COPY /supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENTRYPOINT ["/usr/bin/supervisord"]