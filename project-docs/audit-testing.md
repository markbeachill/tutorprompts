# Audit and testing pack

Audit/testing source lives under:

```text
src/audit-library/
```

Generated audit/testing outputs live under:

```text
docs/audit-library/latest/
docs/audit-library/vX.X/
```

Build and check with:

```bash
python scripts/build_audit_pack.py
python scripts/build_audit_pack.py --ci
```

The audit/testing pack uses the same public release version as the prompt libraries. Do not create a separate public audit version unless the version policy changes.
