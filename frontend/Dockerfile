# Multi-stage Dockerfile for Vue.js frontend
# Demonstrates production-ready Docker practices

# Stage 1: Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (using npm install to regenerate lock file if needed)
# Clear npm cache to ensure fresh install and verify Tailwind version
RUN npm cache clean --force && \
    npm install && \
    npm list tailwindcss && \
    cat package.json | grep tailwindcss

# Copy source code
COPY . .

# Build application
RUN npm run build

# Stage 2: Production stage
FROM nginx:alpine

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
