#!/bin/bash
# Alternative method: Direct build indexing configuration
# Usage: ./enable-build-indexing.sh

echo "Setting up build indexing for tripweaver-ci..."

# Method 1: Try to get current indexing configuration
echo "Getting current build indexing configuration..."
ARTIFACTORY_ID=$(jf config show | grep "Server ID" | head -1 | awk '{print $3}')
echo "Using Artifactory Server ID: $ARTIFACTORY_ID"

# Create build indexing configuration
cat > build-indexing.json << 'EOF'
{
  "bin_mgr_id": "ARTIFACTORY_ID_PLACEHOLDER",
  "indexed_builds": [
    "tripweaver-ci"
  ],
  "non_indexed_builds": []
}
EOF

# Replace placeholder with actual server ID
sed -i "s/ARTIFACTORY_ID_PLACEHOLDER/$ARTIFACTORY_ID/g" build-indexing.json

# Apply the configuration
echo "Applying build indexing configuration..."
jf xr curl -X PUT "/api/v1/binMgr/$ARTIFACTORY_ID/builds" \
  -H "Content-Type: application/json" \
  -d @build-indexing.json

echo "Build indexing configuration applied. Builds may take a few minutes to be indexed."

# Clean up
rm -f build-indexing.json