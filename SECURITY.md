# Security Policy

## Overview

MSK-IO processes sensitive medical imaging data and integrates with external services. This document outlines security considerations, known vulnerabilities, and best practices for secure deployment.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it to:
- **Email**: security@example.com
- **Do not** open public GitHub issues for security vulnerabilities

We will respond within 48 hours and work with you to address the issue.

## Known Security Considerations

### 1. PDFMiner.six Pickle Deserialization Vulnerability

**Severity**: CRITICAL (CVSS 7.8)

**Issue**: The pdfminer.six dependency has a known pickle deserialization vulnerability (CVE-502, CWE-502) that can lead to arbitrary code execution.

**Impact**: Processing malicious PDF files with specially crafted CMap pickle files can execute arbitrary code.

**Mitigation**:
- ✅ **Only process PDF files from trusted sources**
- ✅ Use file size validation (implemented: 100MB limit)
- ✅ Run PDF processing in sandboxed environments
- ✅ Consider replacing pdfminer.six with safer alternatives (pypdf2, pdfplumber)
- ⚠️ Never allow untrusted user uploads directly to PDF processing
- ⚠️ Implement additional file integrity checks

**References**:
- [CWE-502: Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html)
- [OWASP A08:2021 - Software and Data Integrity Failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)

### 2. URL Scheme Validation

**Issue**: Previously, `urllib.urlopen` was used without URL scheme validation, allowing potential file:// or custom scheme exploitation.

**Status**: ✅ FIXED

**Mitigation Implemented**:
- URL scheme validation (only http:// and https:// allowed)
- Network location validation
- Timeout protection (default: 30s)

**Code Location**: `src/msk_io/prompting/web_fetcher.py`

### 3. Hardcoded Temporary Directories

**Issue**: Hardcoded `/tmp` directory paths can cause security issues in multi-user environments.

**Status**: ✅ FIXED

**Mitigation Implemented**:
- Use environment variables ($TMPDIR, $TEMP) with fallback
- Proper permission handling via OS-level temp directory resolution

**Code Locations**:
- `src/msk_io/config.py`
- `src/msk_io/schema/config.py`

### 4. Insecure Random Number Generation

**Issue**: Use of `random.randint()` in medical image preprocessing.

**Severity**: LOW (for preprocessing only)

**Status**: Acceptable for current use case

**Context**: Used only for generating synthetic test data and image augmentation, not for cryptographic purposes.

**Code Location**: `src/msk_io/experimental/medical_image_analysis/preprocessing.py`

## Security Best Practices

### Deployment

1. **Container Security**:
   ```bash
   # Run as non-root user
   docker run --user 1000:1000 msk-io:latest

   # Use read-only filesystem where possible
   docker run --read-only --tmpfs /tmp msk-io:latest

   # Drop capabilities
   docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE msk-io:latest
   ```

2. **Environment Variables**:
   ```bash
   # Set restrictive file permissions
   chmod 600 .env

   # Never commit .env to version control
   echo ".env" >> .gitignore
   ```

3. **API Keys**:
   - Use secrets management (HashiCorp Vault, AWS Secrets Manager, etc.)
   - Rotate API keys regularly
   - Use least-privilege access for LLM APIs

4. **Network Security**:
   - Deploy behind reverse proxy (nginx, Caddy) with TLS
   - Implement rate limiting
   - Use firewall rules to restrict access
   - Enable CORS only for trusted origins

5. **File System**:
   - Restrict watch/input directory permissions (770 or 700)
   - Implement file size limits
   - Validate file types before processing
   - Use separate storage for untrusted data

### Medical Data (HIPAA/GDPR)

1. **Encryption**:
   - Encrypt data at rest (LUKS, dm-crypt)
   - Use TLS 1.3 for data in transit
   - Encrypt backups

2. **Access Control**:
   - Implement role-based access control (RBAC)
   - Log all data access (audit trail)
   - Use multi-factor authentication (MFA)

3. **Data Retention**:
   - Define data retention policies
   - Implement secure deletion (shred, TRIM/discard)
   - Comply with local regulations (HIPAA, GDPR, etc.)

4. **Anonymization**:
   - Remove or pseudonymize patient identifiers
   - Use DICOM de-identification tools
   - Audit for PHI/PII leakage

### Development

1. **Dependency Management**:
   ```bash
   # Regular security scans
   pip-audit
   bandit -r src/
   safety check
   ```

2. **Code Review**:
   - Review all code for security issues
   - Use pre-commit hooks (configured in `.pre-commit-config.yaml`)
   - Run static analysis (ruff, mypy, bandit)

3. **Testing**:
   - Include security test cases
   - Test with malicious inputs
   - Fuzz testing for parsers

## Dependency Security

### Current Vulnerabilities

| Package | Version | Vulnerability | Severity | Status |
|---------|---------|--------------|----------|--------|
| pdfminer.six | 20251107 | Pickle RCE | CRITICAL | ⚠️ Mitigated |

### Monitoring

- Use `pip-audit` for continuous monitoring
- Subscribe to security advisories:
  - [GitHub Security Advisories](https://github.com/advisories)
  - [PyPI Security Feed](https://pypi.org/security/)
  - [Snyk Vulnerability Database](https://snyk.io/vuln)

### Update Policy

- **Critical vulnerabilities**: Patch within 24 hours
- **High vulnerabilities**: Patch within 7 days
- **Medium/Low vulnerabilities**: Patch within 30 days
- **Dependencies**: Review and update quarterly

## Security Checklist

### Pre-Production

- [ ] Change all default credentials/API keys
- [ ] Enable TLS/HTTPS
- [ ] Configure firewall rules
- [ ] Set up logging and monitoring
- [ ] Implement backup strategy
- [ ] Review and restrict file permissions
- [ ] Enable audit logging
- [ ] Implement rate limiting
- [ ] Set up intrusion detection
- [ ] Document incident response plan

### Regular Maintenance

- [ ] Review access logs weekly
- [ ] Update dependencies monthly
- [ ] Run security scans before each release
- [ ] Rotate API keys quarterly
- [ ] Review and update security policies annually
- [ ] Conduct penetration testing annually

## Compliance

### HIPAA (US Healthcare)

- Implement required safeguards
- Conduct risk assessments
- Maintain audit logs
- Sign Business Associate Agreements (BAA)

### GDPR (EU Data Protection)

- Implement data protection by design
- Support data subject rights (access, deletion, portability)
- Maintain data processing records
- Conduct Data Protection Impact Assessments (DPIA)

### FDA (Medical Devices - if applicable)

- Follow cybersecurity guidance
- Implement Software Bill of Materials (SBOM)
- Maintain post-market surveillance

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-17 | Initial security policy |

---

**Last Updated**: 2025-11-17
**Next Review**: 2026-05-17
