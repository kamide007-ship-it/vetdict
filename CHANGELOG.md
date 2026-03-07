# Changelog / 変更履歴

All notable changes to ShowDog Analysis Platform are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- Mobile UX: touch targets (44x44px), notch/safe-area support, scroll indicators
- Dark mode support (`prefers-color-scheme: dark`) for all pages
- Ultra-wide screen support (1920px+, 2560px+)
- Skeleton loading screen CSS components (`.sd-skeleton-*`)
- Skip-to-main-content accessibility link on all pages
- ARIA modal enhancements (auto-applied `role="dialog"`, `aria-modal`)
- CONTRIBUTING.md and CHANGELOG.md
- Expanded OpenAPI specification
- Pre-commit hook configuration
- pytest configuration in pyproject.toml

### Fixed
- Grade C badge color contrast (WCAG AA compliance)
- Touch target sizes below iOS Human Interface Guidelines minimum (44x44px)

## [4.1.0] - 2026-02

### Added
- Code aesthetics refactoring across entire codebase
- Stripe payment integration (JP/Global pricing: Free/Standard/Pro/MAX)
- Navbar PC display fix
- Symptom consultation chat (症状相談チャット) with AI differential diagnosis
- Diagnostic chat integration into navbar and features dashboard
- Algorithm-first architecture (AI non-dependent scoring engine)
- Comprehensive Japanese educational content for 43+ diseases
- Interactive breeds page, AI axes page, enhanced diseases page
- Mobile navbar tab display
- Function dashboard card navigation

### Changed
- Diagnostic chat renamed to symptom consultation chat (症状相談チャット)

## [4.0.0] - 2026-01

### Added
- ShowDog Design System v3.0
- 5-axis evaluation system (Skeletal, Gait, Muscle, Coat, Temperament)
- Photo and video analysis endpoints
- Genetic scoring and breeding compatibility
- Growth prediction models
- Pose estimation and gait analysis
- Judge validation scoring
- Health passport PDF generation (MAFF export compatible)
- Vet visit record system (60+ fields)
- PWA support (manifest, service worker, offline)
- Internationalization (Japanese + English)
- Tap feedback system ("Oxytocin UX" — ripple, scale, glow, haptic)
- Rate limiting and security hardening (Flask-Limiter)
- CI/CD pipeline with auto-merge and health checks
- Algorithm Declaration and Model Governance documentation

### Security
- Flask-Limiter rate limiting (200/day, 50/hour default)
- MIME type validation with magic number verification
- XSS protection (escapeHtml)
- Error message sanitization in production
- Session invalidation on password change
- Secure cookie flags in production
