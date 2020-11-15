FROM nginx
WORKDIR /etc/nginx
ADD web ./web
ADD nginx .
RUN rm /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]