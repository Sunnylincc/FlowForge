FROM node:20-alpine
WORKDIR /repo
COPY package.json package-lock.json* ./
COPY packages/shared/package.json ./packages/shared/package.json
COPY apps/web/package.json ./apps/web/package.json
RUN npm install
COPY packages ./packages
COPY apps/web ./apps/web
WORKDIR /repo/apps/web
CMD ["npm", "run", "dev"]
