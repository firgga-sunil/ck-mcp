# Enable BuildKit for docker builds
export DOCKER_BUILDKIT=1

# Variables for Docker build
DOCKER_REGISTRY=ghcr.io
GRADLE_PROPS_FILE=$(HOME)/.gradle/gradle.properties
DOCKER_REGISTRY_USERNAME=$(shell echo $${DOCKER_REGISTRY_USERNAME:-$(shell grep '^gpr\.user=' $(GRADLE_PROPS_FILE) 2>/dev/null | cut -d'=' -f2 || echo "")})
DOCKER_REGISTRY_TOKEN=$(shell echo $${DOCKER_REGISTRY_TOKEN:-$(shell grep '^gpr\.token=' $(GRADLE_PROPS_FILE) 2>/dev/null | cut -d'=' -f2 || echo "")})
IMAGE_NAME=ck-mcp-server

.PHONY: help check-credentials setup-gradle-props build-and-deploy-ckqa build-and-deploy-prod build-and-deploy-gcp-fk-ckqa build-and-deploy-gcp-demo deploy-ckqa deploy-prod deploy-gcp-fk-ckqa deploy-gcp-demo build-and-deploy-local dockerise-local deploy-common help-detailed verify-context verify-ckqa-context verify-prod-context verify-gcp-fk-ckqa-context verify-gcp-demo-context verify-local-context create-registry-secret build-docker-image build-cleartrip

# Default target when just 'make' is run
help:
	@echo "ck-mcp-server Build and Deployment Targets"
	@echo "=========================================="
	@echo ""
	@echo "CONTEXT AND NAMESPACE MAPPING:"
	@echo "  local context → codekarma namespace (Local Kind cluster)"
	@echo "  ckqa context → codekarma namespace (CKQA environment)"
	@echo "  prod context → codekarma namespace (Production environment)"
	@echo "  gcp-fk-ckqa context → codekarma namespace (GCP FK CKQA environment)"
	@echo "  gcp-demo context → codekarma namespace (GCP Demo environment)"
	@echo ""
	@echo "DEPLOYMENT TARGETS:"
	@echo "  build-and-deploy-local          - Build and deploy to local Kind cluster"
	@echo "  build-and-deploy-ckqa - Build Docker image and deploy to CKQA environment"
	@echo "  build-and-deploy-prod  - Build Docker image and deploy to production environment"
	@echo "  build-and-deploy-gcp-fk-ckqa - Build Docker image and deploy to GCP FK CKQA environment"
	@echo "  build-and-deploy-gcp-demo   - Build Docker image and deploy to GCP Demo environment"
	@echo "  deploy-ckqa           - Deploy existing image to CKQA environment"
	@echo "  deploy-prod           - Deploy existing image to production environment"
	@echo "  deploy-gcp-fk-ckqa    - Deploy existing image to GCP FK CKQA environment"
	@echo "  deploy-gcp-demo       - Deploy existing image to GCP Demo environment"
	@echo ""
	@echo "BUILD-ONLY TARGETS:"
	@echo "  build-cleartrip       - Build Docker image for cleartrip environment (no deployment)"
	@echo ""
	@echo "UTILITY TARGETS:"
	@echo "  check-credentials     - Verify Docker registry credentials"
	@echo "  setup-gradle-props    - Help set up gradle.properties file"
	@echo "  help-detailed         - Show comprehensive documentation"
	@echo ""
	@echo "For detailed documentation, run: make help-detailed"

# Check Docker registry credentials
check-credentials: ## Verify that registry credentials are available
	@echo "Checking registry credentials..."
	@if [ -z "$(DOCKER_REGISTRY_USERNAME)" ] || [ -z "$(DOCKER_REGISTRY_TOKEN)" ]; then \
		echo "ERROR: Docker registry credentials not found!"; \
		echo ""; \
		echo "Please set one of the following:"; \
		echo "1. Environment variables:"; \
		echo "   export DOCKER_REGISTRY_USERNAME=your-github-username"; \
		echo "   export DOCKER_REGISTRY_TOKEN=your-github-personal-access-token"; \
		echo ""; \
		echo "2. Or set up gradle.properties file:"; \
		echo "   make setup-gradle-props"; \
		echo ""; \
		echo "Current values:"; \
		echo "  DOCKER_REGISTRY_USERNAME: $(DOCKER_REGISTRY_USERNAME)"; \
		echo "  DOCKER_REGISTRY_TOKEN: $(if $(DOCKER_REGISTRY_TOKEN),***hidden***,not set)"; \
		exit 1; \
	fi
	@echo "✓ Registry credentials found"
	@echo "  Username: $(DOCKER_REGISTRY_USERNAME)"
	@echo "  Token: ***hidden***"

# Help set up gradle.properties file
setup-gradle-props: ## Help set up gradle.properties file for registry credentials
	@echo "Setting up gradle.properties file for registry credentials..."
	@mkdir -p $(HOME)/.gradle
	@if [ ! -f $(GRADLE_PROPS_FILE) ]; then \
		echo "Creating $(GRADLE_PROPS_FILE)..."; \
		touch $(GRADLE_PROPS_FILE); \
	fi
	@echo ""
	@echo "Please edit $(GRADLE_PROPS_FILE) and set:"
	@echo "  gpr.user=your-github-username"
	@echo "  gpr.token=your-github-personal-access-token"

# Create Docker registry secret for specific environment
create-registry-secret: ## Create/update Docker registry secret for specific environment
	@echo "Creating/updating Docker registry secret for $(ENV) environment..."
	@kubectl create secret docker-registry ckn-ghcr-secret \
		--docker-server=$(DOCKER_REGISTRY) \
		--docker-username="$(DOCKER_REGISTRY_USERNAME)" \
		--docker-password="$(DOCKER_REGISTRY_TOKEN)" \
		--docker-email="$(DOCKER_REGISTRY_USERNAME)@codekarma.tech" \
		--namespace=codekarma \
		--save-config --dry-run=client -o yaml | kubectl apply -f -
	@echo "✓ Docker registry secret created/updated successfully"

# Context verification functions
verify-local-context: ## Verify kubectl context for local deployment
	@echo "Checking kubectl context for local deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != *"kind-"* ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a Kind context."; \
		echo "Expected: A Kind cluster context (should contain 'kind-')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <kind-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is Kind: $$CURRENT_CONTEXT"

verify-ckqa-context: ## Verify kubectl context for CKQA deployment
	@echo "Checking kubectl context for CKQA deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != *"ck-qa"* ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a CKQA context."; \
		echo "Expected: AWS CKQA cluster context (should contain 'ck-qa')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <ckqa-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is CKQA: $$CURRENT_CONTEXT"

verify-prod-context: ## Verify kubectl context for production deployment
	@echo "Checking kubectl context for production deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != *"ck-aws-prod"* ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a production context."; \
		echo "Expected: AWS production cluster context (should contain 'ck-aws-prod')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <prod-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is Production: $$CURRENT_CONTEXT"

verify-gcp-fk-ckqa-context: ## Verify kubectl context for GCP FK CKQA deployment
	@echo "Checking kubectl context for GCP FK CKQA deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != *"gke_codekarma-auth_us-east1_ck-fk-pg"* ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a GCP FK CKQA context."; \
		echo "Expected: GCP FK CKQA cluster context (should contain 'gke_codekarma-auth_us-east1_ck-fk-pg')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <gcp-fk-ckqa-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is GCP FK CKQA: $$CURRENT_CONTEXT"

verify-gcp-demo-context: ## Verify kubectl context for GCP Demo deployment
	@echo "Checking kubectl context for GCP Demo deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != "gke_resounding-node-471205-f9_us-east1_demo-cluster" ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a GCP Demo context."; \
		echo "Expected: GCP Demo cluster context (should contain 'gke_codekarma-demo')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <gcp-demo-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is GCP Demo: $$CURRENT_CONTEXT"

# Build and deploy to CKQA environment
build-and-deploy-ckqa: check-credentials verify-ckqa-context ## Build Docker image and deploy to CKQA environment
	@echo "Building Docker image and deploying to CKQA environment..."
	@$(MAKE) build-docker-image ENV=ckqa
	@$(MAKE) deploy-ckqa
	@echo "✓ CKQA build and deployment completed successfully"

# Build and deploy to production environment
build-and-deploy-prod: check-credentials verify-prod-context ## Build Docker image and deploy to production environment
	@echo "Building Docker image and deploying to production environment..."
	@$(MAKE) build-docker-image ENV=prod
	@$(MAKE) deploy-prod
	@echo "✓ Production build and deployment completed successfully"

# Build and deploy to GCP FK CKQA environment
build-and-deploy-gcp-fk-ckqa: check-credentials verify-gcp-fk-ckqa-context ## Build Docker image and deploy to GCP FK CKQA environment
	@echo "Building Docker image and deploying to GCP FK CKQA environment..."
	@$(MAKE) build-docker-image ENV=gcp-fk-ckqa
	@$(MAKE) deploy-gcp-fk-ckqa
	@echo "✓ GCP FK CKQA build and deployment completed successfully"

# Build and deploy to GCP Demo environment
build-and-deploy-gcp-demo: check-credentials verify-gcp-demo-context ## Build Docker image and deploy to GCP Demo environment
	@echo "Building Docker image and deploying to GCP Demo environment..."
	@$(MAKE) build-docker-image ENV=gcp-demo
	@$(MAKE) deploy-gcp-demo
	@echo "✓ GCP Demo build and deployment completed successfully"

# Build and push Docker image for specific environment
build-docker-image: ## Build and push Docker image for specific environment
	@echo "Building Docker image for $(ENV) environment..."
	@echo "Using registry username: $(DOCKER_REGISTRY_USERNAME)"
	@echo "Logging into $(DOCKER_REGISTRY)..."
	@echo "$(DOCKER_REGISTRY_TOKEN)" | docker login $(DOCKER_REGISTRY) -u "$(DOCKER_REGISTRY_USERNAME)" --password-stdin
	@echo "Building multi-platform Docker image..."
	@docker buildx build --platform linux/amd64,linux/arm64 \
		-t $(DOCKER_REGISTRY)/$(DOCKER_REGISTRY_USERNAME)/$(ENV)/$(IMAGE_NAME)/$(IMAGE_NAME):latest \
		--push .
	@echo "✓ Docker image built and pushed for $(ENV) environment: $(DOCKER_REGISTRY)/$(DOCKER_REGISTRY_USERNAME)/$(ENV)/$(IMAGE_NAME)/$(IMAGE_NAME):latest"

# Build Docker image for cleartrip environment (build only, no deployment)
build-cleartrip: check-credentials ## Build Docker image for cleartrip environment (build only, no deployment)
	@echo "Building Docker image for cleartrip environment..."
	@$(MAKE) build-docker-image ENV=cleartrip

# Local Docker build for Kind cluster
dockerise-local: ## Build Docker image and load into local Kind cluster
	@echo "Building Docker image for local deployment..."
	@docker build -t $(IMAGE_NAME):latest .
	@echo "Loading image into Kind cluster..."
	@kind load docker-image $(IMAGE_NAME):latest --name=kind
	@echo "✓ Local docker image built and loaded successfully"

# Deployment targets (using unified common function)
deploy-ckqa: check-credentials verify-ckqa-context ## Deploy existing image to CKQA environment
	@$(MAKE) deploy-common ENV=ckqa

deploy-prod: check-credentials verify-prod-context ## Deploy existing image to production environment
	@$(MAKE) deploy-common ENV=prod

deploy-gcp-fk-ckqa: check-credentials verify-gcp-fk-ckqa-context ## Deploy existing image to GCP FK CKQA environment
	@$(MAKE) deploy-common ENV=gcp-fk-ckqa

deploy-gcp-demo: check-credentials verify-gcp-demo-context ## Deploy existing image to GCP Demo environment
	@$(MAKE) deploy-common ENV=gcp-demo

# Local deployment to Kind cluster
build-and-deploy-local: verify-local-context dockerise-local ## Build and deploy to local Kind cluster
	@echo "Uninstalling ck-mcp-server from local Kind cluster..."
	@helm uninstall ck-mcp-server -n codekarma || true
	@sleep 4
	@echo "Installing ck-mcp-server to local Kind cluster..."
	@helm install ck-mcp-server ./charts/ck-mcp-charts \
		--namespace codekarma \
		--create-namespace \
		--set image.repository="$(IMAGE_NAME)" \
		--set image.tag="latest" \
		--set image.pullPolicy="Never" \
		-f ./charts/ck-mcp-charts/values.yaml
	@sleep 2
	@echo "✓ Local deployment completed successfully"

# Common deployment function (unified Helm command)
deploy-common: ## Common deployment function for all environments
	@echo "Deploying to $(ENV) environment..."
	@$(MAKE) create-registry-secret ENV=$(ENV)
	@echo "Checking if existing release exists..."
	@if helm list -n codekarma | grep -q ck-mcp-server; then \
		echo "Uninstalling existing ck-mcp-server release..."; \
		helm uninstall ck-mcp-server -n codekarma; \
		echo "Waiting for cleanup..."; \
		sleep 5; \
	else \
		echo "No existing release found, proceeding with fresh installation..."; \
	fi
	@echo "Installing fresh ck-mcp-server release..."
	@helm install ck-mcp-server ./charts/ck-mcp-charts \
		--namespace codekarma \
		--create-namespace \
		--set image.repository="$(DOCKER_REGISTRY)/$(DOCKER_REGISTRY_USERNAME)/$(ENV)/$(IMAGE_NAME)/$(IMAGE_NAME)" \
		--set image.tag="latest" \
		--set image.pullPolicy="Always" \
		-f ./charts/ck-mcp-charts/values-$(ENV).yaml
	@echo "Waiting for ck-mcp-server deployment to be ready..."
	@kubectl wait --for=condition=ready pod -l app=ck-mcp-server -n codekarma --timeout=300s
	@echo "ck-mcp-server deployed successfully"
	@sleep 3
	@echo "Restarting ck-ingress-nginx deployment..."
	@kubectl rollout restart deployment/ck-ingress-nginx -n codekarma
	@echo "Waiting for ingress controller to be ready..."
	@kubectl rollout status deployment/ck-ingress-nginx -n codekarma --timeout=120s
	@echo "✓ $(ENV) deployment completed successfully"

# Comprehensive help documentation
help-detailed:
	@echo "ck-mcp-server Build and Deployment Makefile"
	@echo "==========================================="
	@echo ""
	@echo "OVERVIEW:"
	@echo "This Makefile provides targets for building Docker images and deploying ck-mcp-server"
	@echo "to different environments (local Kind, CKQA, production, GCP FK CKQA, GCP Demo) using Helm."
	@echo ""
	@echo "DEPLOYMENT APPROACH:"
	@echo "HELM-BASED: Uses Helm charts with --set for image override"
	@echo ""
	@echo "ENVIRONMENT-SPECIFIC IMAGE PATHS:"
	@echo "  Local:    ck-mcp-server:latest (loaded into Kind cluster)"
	@echo "  CKQA:     ghcr.io/sabareesh-ckt/ckqa/ck-mcp-server/ck-mcp-server:latest"
	@echo "  Production: ghcr.io/sabareesh-ckt/prod/ck-mcp-server/ck-mcp-server:latest"
	@echo "  GCP FK CKQA: ghcr.io/sabareesh-ckt/gcp-fk-ckqa/ck-mcp-server/ck-mcp-server:latest"
	@echo "  GCP Demo:   ghcr.io/sabareesh-ckt/gcp-demo/ck-mcp-server/ck-mcp-server:latest"
	@echo "  Cleartrip:  ghcr.io/sabareesh-ckt/cleartrip/ck-mcp-server/ck-mcp-server:latest"
	@echo ""
	@echo "CREDENTIALS:"
	@echo "Docker registry credentials are automatically loaded from:"
	@echo "  1. Environment variables: DOCKER_REGISTRY_USERNAME, DOCKER_REGISTRY_TOKEN"
	@echo "  2. Gradle properties file: ~/.gradle/gradle.properties (gpr.user, gpr.token)"
	@echo ""
	@echo "DEPLOYMENT TARGETS:"
	@echo "  build-and-deploy-local          - Build and deploy to local Kind cluster"
	@echo "  build-and-deploy-ckqa - Complete pipeline: build image + deploy to CKQA"
	@echo "  build-and-deploy-prod  - Complete pipeline: build image + deploy to production"
	@echo "  build-and-deploy-gcp-fk-ckqa - Complete pipeline: build image + deploy to GCP FK CKQA"
	@echo "  build-and-deploy-gcp-demo   - Complete pipeline: build image + deploy to GCP Demo"
	@echo "  deploy-ckqa           - Deploy existing image to CKQA environment"
	@echo "  deploy-prod           - Deploy existing image to production environment"
	@echo "  deploy-gcp-fk-ckqa    - Deploy existing image to GCP FK CKQA environment"
	@echo "  deploy-gcp-demo       - Deploy existing image to GCP Demo environment"
	@echo ""
	@echo "BUILD-ONLY TARGETS:"
	@echo "  build-cleartrip       - Build Docker image for cleartrip environment (no deployment)"
	@echo ""
	@echo "UTILITY TARGETS:"
	@echo "  check-credentials     - Verify Docker registry credentials are available"
	@echo "  setup-gradle-props    - Help set up gradle.properties file"
	@echo ""
	@echo "CONTEXT VERIFICATION:"
	@echo "The following kubectl contexts are expected:"
	@echo "  Local:     Context containing 'kind-' (Kind cluster)"
	@echo "  CKQA:      Context containing 'ck-qa'"
	@echo "  Production: Context containing 'ck-aws-prod'"
	@echo "  GCP FK CKQA: Context containing 'gke_codekarma-auth_us-east1_ck-fk-pg'"
	@echo "  GCP Demo:   Context containing 'gke_codekarma-demo'"
	@echo ""
	@echo "EXAMPLES:"
	@echo "  # Build and deploy to local Kind cluster"
	@echo "  make build-and-deploy-local"
	@echo ""
	@echo "  # Build and deploy to CKQA environment"
	@echo "  make build-and-deploy-ckqa"
	@echo ""
	@echo "  # Build and deploy to production environment"
	@echo "  make build-and-deploy-prod"
	@echo ""
	@echo "  # Build and deploy to GCP FK CKQA environment"
	@echo "  make build-and-deploy-gcp-fk-ckqa"
	@echo ""
	@echo "  # Build and deploy to GCP Demo environment"
	@echo "  make build-and-deploy-gcp-demo"
	@echo ""
	@echo "  # Deploy existing image to CKQA"
	@echo "  make deploy-ckqa"
	@echo ""
	@echo "  # Deploy existing image to GCP FK CKQA"
	@echo "  make deploy-gcp-fk-ckqa"
	@echo ""
	@echo "  # Deploy existing image to GCP Demo"
	@echo "  make deploy-gcp-demo"
	@echo ""
	@echo "  # Build image for cleartrip environment (no deployment)"
	@echo "  make build-cleartrip"
	@echo ""
	@echo "  # Check if credentials are properly configured"
	@echo "  make check-credentials"
	@echo ""
	@echo "  # Set up gradle.properties file"
	@echo "  make setup-gradle-props"
	@echo ""
	@echo "NOTES:"
	@echo "- Helm approach: Uses '--set' to override image repository and tag"
	@echo "- Single command deployment with atomic updates"
	@echo "- Docker images are built for both linux/amd64 and linux/arm64 platforms"
	@echo "- Registry secrets are automatically created/updated in the codekarma namespace"
	@echo "- Helm provides better templating, rollback, and environment management"
	@echo "- GCP FK CKQA and GCP Demo deployments use the same Helm chart with environment-specific values"

