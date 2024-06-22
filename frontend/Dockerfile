# Dockerfile for Svelte frontend

FROM node:16
WORKDIR /app
COPY ./package*.json ./
RUN npm install
COPY . .

# Expose the port the dev server runs on
EXPOSE 5173

# Command to run the app in development mode
CMD ["npm", "run", "dev", "--", "--host"]
