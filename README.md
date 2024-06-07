# KCX
> **K**nightchaser's **C**ryptocurrency e**X**change

![sveltekit_lgo](https://img.shields.io/badge/SvelteKit-FF3E00?style=for-the-badge&logo=Svelte&logoColor=white)
![vite_logo](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)
![nodejs_logo](https://img.shields.io/badge/Node%20js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![fastapi_logo](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![sqlite_logo](https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![redis_logo](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
![docker-logo](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![nginx_logo](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![aws_logo](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)

## A Free-From-Risk cryptocurrency exchange simulation web application

You can try KCX at **[https://kcx.knightchaser.com/](https://kcx.knightchaser.com/)**, which is hosted via AWS Lightsail by the repository owner. Note that the specifications, service status, and other things might be changed depending on the development contexts and situations. (Try only for fun! :D)

## Deployment
- Clone the repository on your server/environments
```sh
https://github.com/KnightChaser/kcx.git
```
- To intiate the service, you'll have to use **`docker-compose`**(Or, `docker compose` for Docker Compose v2. Not matter which version you use).
- If you are going to run service locally(such as windows), execute the following commands(the system(Windows/Linux) should be able to operate the docker applications)
```sh
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```
- If you are going to run service globally with TLS/SSL certificates(For production. `https://kcx.knightchaser.com` is currently running on this way.), check the prerequisites and operate the docker.
    - Ensure that you have your own **domain**(FQDN) such as `*.knightchaser.com` and it's registered on the global DNS server. (i.e. Route53 in AWS)
    - Ensure that the **valid TLS/SSL certificates** are issued and prepared on your system. (i.e. A certificate issued by Certbot via `letsencrypt`)
    - Ensure that you properly adjusted the settings(described in the next chapter; **`Note about TLS/SSL`**.). Then, boot up the service with the following commands.
```sh
docker-compose -f docker-compose-server-deploy.yml build
docker-compose -f docker-compose-server-deploy.yml up -d
```

## Note about TLS/SSL
- The TLS/SSL extensions are expected to be in `/etc/letsencrypt` in general if you use `letsencrypt`.
```
(/etc/letsencrypt)
├── live
│   ├── README
│   └── knightchaser.com
│       ├── README
│       ├── cert.pem -> ../../archive/knightchaser.com/cert1.pem
│       ├── chain.pem -> ../../archive/knightchaser.com/chain1.pem
│       ├── fullchain.pem -> ../../archive/knightchaser.com/fullchain1.pem
│       └── privkey.pem -> ../../archive/knightchaser.com/privkey1.pem
```

- In **`nginx.conf`**, the basic structure will be the below example. (The given example is `https://kcx.knightchaser.com`'s.) Change `server_name`, `ssl_certificate`, and `ssl_certificate_key` properties to your own.
```nginx
events { }

http {
    server {
        listen 80;
        server_name kcx.knightchaser.com;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name kcx.knightchaser.com;

        ssl_certificate /etc/letsencrypt/live/knightchaser.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/knightchaser.com/privkey.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://frontend:5173;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```
- In the **Docker compsure file(`docker-compose-server-deploy.yml`)**, adjust the `volumes` part of **`nginx`** to yours(if it's needed). If you follow the standard `letsencrypt`'s  TLS/SSL issuing procedure with Certbot, this adjustment won't be necessary. 
```yml
  ...
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/letsencrypt
    depends_on:
      - frontend
      - backend
    networks:
      - kcx-network
```
- In **`<PROJECT_DIR>/frontend/.env`**(Vite environment variable file), adjust the backend API URL to your domain. Since the suffix string `/api` is the hardcoded value of this project for consistency, you will only have to adjust the URL part. `https://kcx.knightchaser.com` part for the example below.
```
VITE_BACKEND_API_URL="https://kcx.knightchaser.com/api"
```
- Miscellaneous: **TLS/SSL** uses the port `443`. Allow `80` and `443` ports at least.