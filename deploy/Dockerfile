FROM prestashop/prestashop:1.7.8.11

# Install system dependencies required for Memcached
RUN apt-get update && apt-get install -y \
    libmemcached-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install PHP Memcached extension via PECL
RUN pecl install memcached \
    && docker-php-ext-enable memcached

# Copy shop files
COPY prestashop/ /var/www/html/

# Copy Apache configuration with SSL
COPY prestashop/apache-config/000-default.conf /etc/apache2/sites-available/000-default.conf

# Copy SSL certificates
COPY prestashop/apache-config/ssl/cert.pem /etc/ssl/certs/cert.pem
COPY prestashop/apache-config/ssl/key.pem /etc/ssl/certs/key.pem

# Enable SSL module in Apache
RUN a2enmod ssl

# Set permissions
RUN chown -R www-data:www-data /var/www/html \
    && chmod 600 /etc/ssl/certs/key.pem \
    && chmod 644 /etc/ssl/certs/cert.pem

EXPOSE 80 443

CMD ["apache2-foreground"]
