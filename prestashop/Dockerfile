FROM prestashop/prestashop:1.7.8

# Skopiuj pliki sklepu
COPY . /var/www/html/

# Usuń katalog instalacyjny
RUN rm -rf /var/www/html/install

# Instalacja OpenSSL (jeśli nie jest zainstalowany)
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

# Włącz moduły Apache
RUN a2enmod ssl rewrite headers

# Utwórz samopodpisany certyfikat SSL (można odświeżać przy starcie kontenera)
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/prestashop.key \
    -out /etc/ssl/certs/prestashop.crt \
    -subj "/C=PL/ST=Pomerania/L=Gdansk/O=PG-ETI/OU=BE/CN=prestashop-be-197652"

# Skopiuj minimalny vhost SSL z DirectoryIndex i PHP handler
RUN echo '<VirtualHost *:443>\n\
    ServerName prestashop-be-197652\n\
    DocumentRoot /var/www/html\n\
    SSLEngine on\n\
    SSLCertificateFile /etc/ssl/certs/prestashop.crt\n\
    SSLCertificateKeyFile /etc/ssl/private/prestashop.key\n\
    <Directory /var/www/html>\n\
        Options Indexes FollowSymLinks\n\
        AllowOverride All\n\
        Require all granted\n\
        DirectoryIndex index.php index.html\n\
    </Directory>\n\
    <FilesMatch "\.php$">\n\
        SetHandler application/x-httpd-php\n\
    </FilesMatch>\n\
    ErrorLog ${APACHE_LOG_DIR}/error.log\n\
    CustomLog ${APACHE_LOG_DIR}/access.log combined\n\
</VirtualHost>' > /etc/apache2/sites-available/default-ssl.conf

# Włącz SSL site
RUN a2ensite default-ssl.conf

# Uprawnienia plików
RUN chown -R www-data:www-data /var/www/html \
    && find /var/www/html -type d -exec chmod 755 {} \; \
    && find /var/www/html -type f -exec chmod 644 {} \;

# Eksport portów
EXPOSE 80 443

# Start Apache
CMD ["apache2-foreground"]

