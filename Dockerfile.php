FROM php:8.2-apache

# Install PHP extensions
RUN docker-php-ext-install pdo pdo_mysql

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Set ServerName to suppress warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Configure Apache to allow .htaccess overrides
RUN sed -i '/<Directory \/var\/www\/>/,/<\/Directory>/ s/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf

# Copy website files
COPY website/ /var/www/html/

# Set proper permissions
RUN chown -R www-data:www-data /var/www/html

# Expose port 80
EXPOSE 80
