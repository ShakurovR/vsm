FROM node:18 as builder
WORKDIR /app
COPY package.json ./

RUN yarn
COPY . ./
RUN yarn build
COPY . ./

FROM nginx:latest
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
