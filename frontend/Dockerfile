FROM node:18-alpine AS builder
ARG ARTIFACTORY_NPM_REGISTRY
ARG ARTIFACTORY_NPM_AUTH_TOKEN
WORKDIR /app
COPY package.json package-lock.json* ./
# If an Artifactory NPM registry is provided, configure a transient .npmrc
RUN set -e; \
		if [ -n "$ARTIFACTORY_NPM_REGISTRY" ]; then \
			echo "Using Artifactory NPM registry: $ARTIFACTORY_NPM_REGISTRY"; \
			if [ -n "$ARTIFACTORY_NPM_AUTH_TOKEN" ]; then AUTH_LINE="//${ARTIFACTORY_NPM_REGISTRY#https://}:_authToken=${ARTIFACTORY_NPM_AUTH_TOKEN}"; fi; \
			{ \
				echo "registry=$ARTIFACTORY_NPM_REGISTRY"; \
				echo "always-auth=true"; \
				if [ -n "$AUTH_LINE" ]; then echo "$AUTH_LINE"; fi; \
			} > .npmrc; \
		fi; \
		npm install --no-package-lock --only=production --no-audit --no-fund; \
		rm -f .npmrc || true
COPY . ./
RUN npm run build || true

FROM node:18-alpine
WORKDIR /app

# Create non-root user for security hardening
RUN addgroup -g 1001 -S tripweaver && \
    adduser -S tripweaver -u 1001 -G tripweaver

COPY --from=builder /app .

# Set ownership and permissions for the application directory
RUN chown -R tripweaver:tripweaver /app && \
    chmod -R 755 /app

# Switch to non-root user
USER tripweaver

EXPOSE 3000
ENV NODE_ENV=production
CMD ["npm","start"]
