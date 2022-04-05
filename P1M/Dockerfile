FROM ubuntu:20.04
MAINTAINER Yoku Tamotsu <yoku-tamotsu@merce>

# Setting frontend Noninteractive
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Avoid ERROR: invoke-rc.d: policy-rc.d denied execution of start.
RUN echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d

# Edit sources.list to add to install libapache2-mod-fastcgi
# Adding
#deb http://archive.ubuntu.com/ubuntu trusty multiverse
#deb http://archive.ubuntu.com/ubuntu trusty-updates multiverse
#deb http://security.ubuntu.com/ubuntu trusty-security multiverse
RUN echo "deb http://archive.ubuntu.com/ubuntu trusty multiverse \ndeb http://archive.ubuntu.com/ubuntu trusty-updates multiverse \ndeb http://security.ubuntu.com/ubuntu trusty-security multiverse" >> /etc/apt/sources.list


RUN apt-get update ; \
    apt-get install -y software-properties-common supervisor openvpn
    
RUN LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php ; \
    apt-get update ; \
    apt-get install -y \
    apache2 \
    libapache2-mod-fastcgi \
    php7.4-fpm \
    php7.4-ldap \
    php7.4-xml \
    php7.4-mysql \
	php7.4-curl \
	php7.4-pdo \
	php7.4-cli \
	php7.4-pdo-mysql \
    libmysqlclient-dev \
    mysql-client ;
	
#===== OPENVPN =========================================================

COPY openvpn/ /etc/openvpn/


#===== APACHE2 / PHP 7.4 ===============================================

#Copy Apache Config files
COPY apache2/000-default.conf /etc/apache2/sites-enabled/000-default.conf 
COPY apache2/apache2.conf /etc/apache2/apache2.conf

#Add Site user and group
RUN groupadd -g 1000 site; \
    adduser --gecos "First Last,RoomNumber,WorkPhone,HomePhone" --home /home/site --uid 1000 --ingroup site --disabled-login --disabled-password site; \ 
    usermod -a -G sudo site; \
    chown -R site:site /var/lib/apache2/fastcgi

#Changing Apache User and PHP-FPM User
RUN sed -rie 's|export APACHE_RUN_USER=.*|export APACHE_RUN_USER=site|g' /etc/apache2/envvars; \
    sed -rie 's|export APACHE_RUN_GROUP=.*|export APACHE_RUN_GROUP=site|g' /etc/apache2/envvars; \
    sed -ie 's/www-data/site/g' /etc/php/7.4/fpm/pool.d/www.conf

#Create docroot directory, copy code and grant permission to documents root
RUN mkdir -p /var/www/html ; \
    rm -r /var/www/html/* ; \
	echo "<?php phpinfo();" > /var/www/html/index.php
	
COPY html /var/www/html

RUN chown -R site:site /var/www/html

# Copy the Apache Config file for Php-fpm
COPY apache2/php7.4-fpm.conf /etc/apache2/conf-available/php7.4-fpm.conf

# Create dir for php-fpm .sock file
RUN mkdir -p /run/php

# Enable Php-Fpm Conf
RUN a2enconf php7.4-fpm ; \
    a2enmod actions rewrite headers; \
    touch /usr/lib/cgi-bin/php5.fcgi ; \
    chown -R site:site /usr/lib/cgi-bin  

EXPOSE 80


#===== SUPERVISOR ======================================================

# Copy Supervisor file in to conatianer
COPY /supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
   
ENTRYPOINT ["/usr/bin/supervisord"]

