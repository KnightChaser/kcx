# KCX
> **K**nightchaser's **C**ryptocurrency e**X**change

## TECH STACK
- **Service buildup**

![sveltekit_lgo](https://img.shields.io/badge/SvelteKit-FF3E00?style=for-the-badge&logo=Svelte&logoColor=white)
![vite_logo](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)
![nodejs_logo](https://img.shields.io/badge/Node%20js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![jwt_logo](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![fastapi_logo](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![sqlite_logo](https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![redis_logo](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
![nginx_logo](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

- **Deployment**

![docker_logo](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![aws_logo](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)

- **You can able to deploy on**

![windows_logo](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![ubuntu_logo](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)


## A Free-From-Risk cryptocurrency exchange simulation web application

You can try KCX at **[https://kcx.knightchaser.com/](https://kcx.knightchaser.com/)**, which is hosted via AWS Lightsail by the repository owner. Note that the specifications, service status, and other things might be changed depending on the development contexts and situations. (Try only for fun! :D)

## Service environmental variables
Currently, there are environment variables to set up the services as you need. Read the next chapter(`Deployment`) for complete contextual information.
```env
SQLALCHEMY_DB_SQLITE3_PATH="sqlite:///kcx.db"

TEST_ACCOUNT_ID="test"
TEST_ACCOUNT_PW="test"
TEST_ACCOUNT_EMAIL="test@kcx.org"
COMMON_STARTING_BALANCE_IN_KRW=20000000000 # 20 billion KRW

# An example SECRET KEY for JWT. Change this to a random in production!
JWT_SECRET_KEY="KCXU$3R$3CR3T4JWT_"
JWT_TOKEN_EXPIRES_MINUTES=360 # 6 hours

# A custom API server built with Redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_UDPATE_INTERVAL_IN_SECONDS=1
USER_RANKING_UPDATE_INTERVAL_IN_SECONDS=10

# Service configuration
# - Money balance (Disable(false) this if you want to use a fixed starting balance for all users)
ALLOW_ARBITRARY_BALANCE_DEPOSIT=false
ALLOW_ARBITRARY_BALANCE_WITHDRAW=false
```
- Permanent data for this service will be stored in SQLite3. Configure `SQLALCHEMY_DB_SQLITE3_PATH` for the specified path.
- As a default, there are default account settings.
  - The service will create a default account for testing when the service starts. (Will not if it's already created)
  - Configure `TEST_ACCOUNT_ID`(ID = username), `TEST_ACCOUNT_PW`(password), and `TEST_ACCOUNT_EMAIL`(email) for the test account.
  - `COMMON_STARTING_BALANCE_IN_KRW` defines how much fund will be initially granted to the new user.
- This server uses JWT for user authentication. Configure `JWT_SECRET_KEY` for JWT server key(change to another random value or your own) and `JWT_TOKEN_EXPIRES_MINUTES` for JWT expiary period.
- For the price information, this service uses the market data provided from UpBIT. Of course this also mimics the cryptocurrency exchange, there are a lot of requests about the crypto market data(Generally 3 to 5 requests per second per connected user) To reduce the direct API request to UpBIT, this use REDIS database as a cache. The server caches the market data every second and multiple connected users obtain the data from this REDIS cache.
  - `REDIS_UPDATE_INTERVAL_IN_SECONDS` means which second this service refreshes the market data from UpBIT to the REDIS cache periodically. Basically, you can safely request up to 5 requests per second to UpBIT according to the current policy.
  - `USER_RANKING_UPDATE_INTERVAL_IN_SECONDS` means which second this service calculate the users' ranking data according to the calculated estimated total asset value periodically (for leaderboard). Note that this ranking calculation relatively takes a lot of computational loads(iterating all users and calculating all types of assets for estimation), so don't make it too short.
- `ALLOW_ARBITRARY_BALANCE_*` configures whether the user controls their virtual balances on their own. If these are set true, then they can unlimitedly deposit(increase) and withdraw(decrease) the wallet, that may impact on the leaderboard. If you run this service for competitions or some rules, set it to false so no one except for the administrator can control the user's balances. (By accessing the SQLite3 database.)

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