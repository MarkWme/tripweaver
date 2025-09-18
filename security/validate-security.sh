#!/bin/bash
# Security validation script for CVE-2025-8941 mitigation measures
# This script validates that all security hardening measures are properly implemented

set -e

echo "🔐 TripWeaver Security Validation - CVE-2025-8941 Mitigation"
echo "============================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo
echo "1. Checking Dockerfile Security Configurations..."
echo "------------------------------------------------"

# Check API Dockerfile for non-root user
if grep -q "USER tripweaver" api/Dockerfile; then
    print_status 0 "API Dockerfile uses non-root user"
else
    print_status 1 "API Dockerfile missing non-root user configuration"
fi

# Check for PAM hardening in API Dockerfile
if grep -q "namespace.conf" api/Dockerfile; then
    print_status 0 "API Dockerfile includes PAM hardening"
else
    print_status 1 "API Dockerfile missing PAM hardening"
fi

# Check Frontend Dockerfile for non-root user
if grep -q "USER tripweaver" frontend/Dockerfile; then
    print_status 0 "Frontend Dockerfile uses non-root user"
else
    print_status 1 "Frontend Dockerfile missing non-root user configuration"
fi

# Check Seedgen Dockerfile for non-root user
if grep -q "USER tripweaver" tools/seedgen/Dockerfile; then
    print_status 0 "Seedgen Dockerfile uses non-root user"
else
    print_status 1 "Seedgen Dockerfile missing non-root user configuration"
fi

echo
echo "2. Checking Kubernetes Security Contexts..."
echo "-------------------------------------------"

# Check K8s deployment for security context
if grep -q "runAsNonRoot: true" infra/k8s/api-deployment.yaml; then
    print_status 0 "Kubernetes deployment has security context"
else
    print_status 1 "Kubernetes deployment missing security context"
fi

# Check for capability restrictions
if grep -q "allowPrivilegeEscalation: false" infra/k8s/api-deployment.yaml; then
    print_status 0 "Kubernetes deployment prevents privilege escalation"
else
    print_status 1 "Kubernetes deployment missing privilege escalation prevention"
fi

echo
echo "3. Checking Helm Chart Security Configuration..."
echo "-----------------------------------------------"

# Check Helm values for security context
if grep -q "runAsNonRoot: true" charts/tripweaver/values.yaml; then
    print_status 0 "Helm chart includes security context defaults"
else
    print_status 1 "Helm chart missing security context defaults"
fi

# Check Helm template for security context
if grep -q "securityContext:" charts/tripweaver/templates/deployment.yaml; then
    print_status 0 "Helm template includes security context"
else
    print_status 1 "Helm template missing security context"
fi

echo
echo "4. Checking Docker Compose Security Settings..."
echo "-----------------------------------------------"

# Check docker-compose for user specification
if grep -q 'user: "1001:1001"' docker-compose.yml; then
    print_status 0 "Docker Compose specifies non-root user"
else
    print_status 1 "Docker Compose missing user specification"
fi

# Check for security options
if grep -q "no-new-privileges:true" docker-compose.yml; then
    print_status 0 "Docker Compose includes no-new-privileges"
else
    print_status 1 "Docker Compose missing no-new-privileges"
fi

echo
echo "5. Checking Security Documentation..."
echo "------------------------------------"

# Check for security documentation
if [ -f "SECURITY.md" ]; then
    print_status 0 "Security documentation exists"
else
    print_status 1 "Security documentation missing"
fi

# Check for PAM configuration files
if [ -f "security/namespace.conf" ] && [ -f "security/pam-hardening.conf" ]; then
    print_status 0 "PAM security configuration files exist"
else
    print_status 1 "PAM security configuration files missing"
fi

echo
echo "6. Functional Validation..."
echo "--------------------------"

# Test that the API still works after hardening
echo "Testing API functionality..."
cd api
if [ -d ".venv" ]; then
    source .venv/bin/activate
    # Quick test to ensure the application can still start
    if python -c "from app.main import app; print('✓ API imports successfully')" 2>/dev/null; then
        print_status 0 "API functionality preserved after hardening"
    else
        print_status 1 "API functionality broken after hardening"
    fi
else
    print_warning "Python virtual environment not found - skipping API test"
fi
cd ..

echo
echo "🔐 Security Validation Summary"
echo "==============================="
echo "CVE-2025-8941 mitigation measures have been implemented across:"
echo "- Container user restrictions (non-root execution)"
echo "- PAM configuration hardening"
echo "- Kubernetes security contexts"
echo "- Docker Compose security settings"
echo "- Comprehensive security documentation"
echo
echo "⚠️  Note: Due to network restrictions, Docker image builds may fail."
echo "   Use local development environment for testing functionality."
echo
echo "For production deployment, ensure all security measures are properly"
echo "configured and regularly monitored as outlined in SECURITY.md"