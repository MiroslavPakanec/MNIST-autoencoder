FROM node:16.20.2
WORKDIR /workspace

COPY . .
RUN npm install
RUN npm i --save-dev @types/p5
CMD npm run serve -- --port ${CONTAINER_PORT} --host ${HOST_IP}