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
COPY --from=builder /app .
EXPOSE 3000
ENV NODE_ENV=production
CMD ["npm","start"]
