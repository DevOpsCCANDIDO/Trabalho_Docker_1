FROM node:18.17.0 as builder
WORKDIR /app
COPY ../frontend/package.json /app/package.json
COPY ../frontend /app
RUN npm install && npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
