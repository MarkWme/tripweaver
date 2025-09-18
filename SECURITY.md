# TripWeaver Security Guide

## CVE-2025-8941 Mitigation

This document outlines the security hardening measures implemented to mitigate CVE-2025-8941, a high-severity privilege escalation vulnerability in libpam0g affecting the Debian Bookworm base image.

### Vulnerability Overview

- **CVE:** CVE-2025-8941
- **Component:** libpam0g 1.5.2-6+deb12u1 (Debian Bookworm)
- **Severity:** High (7.8)
- **Impact:** Local privilege escalation to root via pam_namespace exploitation

### Implemented Security Measures

#### 1. Container User Restrictions

All Docker containers now run as non-root users:

- **API Container:** Uses `tripweaver` user (UID/GID: 1001)
- **Frontend Container:** Uses `tripweaver` user (UID/GID: 1001)  
- **Seedgen Container:** Uses `tripweaver` user (UID/GID: 1001)

#### 2. PAM Configuration Hardening

- Empty `/etc/security/namespace.conf` prevents pam_namespace exploitation
- Restrictive file permissions (644, root:root ownership)
- Disabled pam_namespace module where possible

#### 3. Container Security Contexts

**Kubernetes Deployments:**
- `runAsNonRoot: true`
- `runAsUser: 1001` and `runAsGroup: 1001`
- `allowPrivilegeEscalation: false`
- `seccompProfile: RuntimeDefault`
- Capabilities dropped to minimum required (`NET_BIND_SERVICE` only)

**Docker Compose:**
- User specification: `1001:1001`
- `no-new-privileges:true`
- Minimal capability set (only `NET_BIND_SERVICE`)

#### 4. File System Protections

- Application directories owned by non-root user
- Restrictive permissions (755) on application files
- Read-only data volumes where appropriate

### Security Validation

#### Manual Testing

1. **Verify Non-Root Execution:**
   ```bash
   docker run --rm tripweaver-api:local whoami
   # Should return: tripweaver
   ```

2. **Check PAM Configuration:**
   ```bash
   docker run --rm tripweaver-api:local cat /etc/security/namespace.conf
   # Should return empty file with comment
   ```

3. **Privilege Escalation Prevention:**
   ```bash
   docker run --rm tripweaver-api:local id
   # Should show UID/GID 1001, not root
   ```

#### Automated Monitoring

The following should be monitored in production:

- PAM authentication events in system logs
- Unusual privilege escalation attempts
- File system access patterns
- Container runtime security events

### Best Practices

1. **Regular Updates:** Keep base images updated when security patches become available
2. **Principle of Least Privilege:** Run containers with minimal required permissions
3. **Security Scanning:** Regularly scan images for vulnerabilities
4. **Runtime Security:** Use container runtime security tools (Falco, etc.)
5. **Network Segmentation:** Isolate containers with proper network policies

### Production Deployment

For production environments, additionally consider:

- Use distroless or minimal base images when possible
- Implement Pod Security Standards in Kubernetes
- Use admission controllers to enforce security policies
- Regular security audits of container configurations
- Implement monitoring and alerting for security events

### Emergency Response

If privilege escalation is detected:

1. Immediately isolate affected containers
2. Review system logs for attack patterns
3. Check for unauthorized file system modifications
4. Verify integrity of application data
5. Update incident response procedures

### References

- [CVE-2025-8941 Details](https://nvd.nist.gov/vuln/detail/CVE-2025-8941)
- [Linux PAM Documentation](http://www.linux-pam.org/)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [Docker Security Guidelines](https://docs.docker.com/engine/security/)

---

**Last Updated:** 2024-09-18  
**Security Review Required:** Every 6 months or after significant changes