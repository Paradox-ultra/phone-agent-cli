# Android capability boundaries

Termux is a Linux userspace environment, not an Android system application. It cannot automatically inspect or control every other Android app.

## Available in this MVP

- Files below the configured Phone Agent workspace
- Shell commands only when explicitly enabled and allowlisted
- Selected Termux:API commands when the companion app is installed and Android permissions are granted

## Not included

- Arbitrary app UI inspection or tapping
- Notification access
- Screen capture or global touch injection
- Contacts, SMS, calls, microphone, camera, or location

These require purpose-built Android components, explicit user consent, and usually runtime permissions or accessibility-service approval. Future integrations should be opt-in modules that report their permission state to the calling agent.

## Termux:API setup

Install the Termux:API companion app from the same trusted distribution channel as Termux, then run:

```bash
pkg install termux-api
```

Grant Android permissions as needed. Battery and clipboard tools return errors when the companion executable or permission is unavailable.
