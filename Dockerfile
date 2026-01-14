# Zaczynamy od oficjalnego obrazu PrestaShop (taki sam jak w docker-compose)
FROM prestashop/prestashop:1.7.8.11

# Instalujemy zależności systemowe potrzebne do Memcached
RUN apt-get update && apt-get install -y \
    libmemcached-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalujemy rozszerzenie PHP Memcached przez PECL
RUN pecl install memcached \
    && docker-php-ext-enable memcached