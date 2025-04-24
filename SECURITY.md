# Security Policy for Esource.gg Python SDK

The Esource.gg team and community take the security of the `esource-client-api` SDK seriously. We appreciate your efforts to responsibly disclose your findings, and we will make every effort to acknowledge your contributions.

## Supported Versions

We are committed to providing security updates for the most recent **minor** release of each **major** version series. Please ensure you are using an up-to-date version before reporting a vulnerability.

| Version | Supported          |
| ------- | ------------------ |
| 1.x.y   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report sensitive security issues directly to us via one of the following methods:

1.  **(Recommended) GitHub Private Vulnerability Reporting:** Use the "Report a vulnerability" feature under the "Security" tab of the repository (`https://github.com/Eppop-bet/client-api-sdk/security/advisories`). This allows for secure communication and tracking directly within GitHub.
2.  **(Alternative) Email:** Send an email to `info@esource.gg` (or a dedicated security email if you have one) with the subject line starting with `[SECURITY]`. Please include the information requested below.

**What to Include:**

Please include the following details with your report:

*   A clear description of the vulnerability and its potential impact.
*   The specific version(s) of the `esource-client-api` SDK affected.
*   Detailed steps to reproduce the vulnerability.
*   Any proof-of-concept code or examples that demonstrate the issue.
*   Any potential mitigations or suggested fixes, if known.

## Scope

This policy applies only to the code within the `esource-client-api` SDK itself (`https://github.com/Eppop-bet/client-api-sdk`).

The following are generally considered **out of scope**:

*   The Esource.gg API service itself (vulnerabilities in the backend API should be reported through Esource.gg's official channels, if available).
*   Vulnerabilities in third-party dependencies (unless they are directly exploitable through a flaw in how this SDK uses the dependency). Please report these to the maintainers of the dependency directly.
*   Issues related to rate limiting or denial of service against the Esource.gg API.
*   Social engineering or phishing attempts related to the project.

## Our Commitment

When you report a vulnerability through the recommended channels:

1.  We will strive to acknowledge receipt of your report within 3 business days.
2.  We will investigate the report and determine its validity and impact.
3.  We will work to remediate the vulnerability in a timely manner.
4.  We will maintain communication with you regarding the status of the report and the remediation efforts.
5.  Once the vulnerability is fixed, we will coordinate with you on public disclosure, typically through a GitHub Security Advisory and a new release. We aim to credit reporters who responsibly disclose vulnerabilities.

Thank you for helping keep the Esource.gg Python SDK and its users safe.
