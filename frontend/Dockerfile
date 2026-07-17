# ── Stage 1: Build ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --quiet

COPY . .

# VITE_BACKEND_URL is injected at build time via Cloud Run build arg
ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL

RUN npm run build

# ── Stage 2: Serve with nginx ────────────────────────────────────────────────
FROM nginx:1.27-alpine

# Non-root setup
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Custom nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN chown -R appuser:appgroup /usr/share/nginx/html \
    && chown -R appuser:appgroup /var/cache/nginx \
    && chown -R appuser:appgroup /var/log/nginx \
    && touch /var/run/nginx.pid \
    && chown appuser:appgroup /var/run/nginx.pid

USER appuser

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
