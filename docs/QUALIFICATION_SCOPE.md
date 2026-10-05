# Qualification Scope

GOVQ uses deliberately narrow claims.

## What the initial public baseline establishes

For the files documented in `PROVENANCE.md`, the project records:

- reviewed source identity;
- controlled extraction;
- controlled sanitization;
- absence of intentional behavior changes in the sanitized protocol wording;
- byte identity for the initial `model_input.py` extraction.

## What it does not establish

Source provenance must not be confused with runtime qualification.

This public repository does not, by itself, establish:

- complete production readiness;
- complete Governed AI Core acceptance;
- zero-bypass guarantees for modules not present here;
- correctness of third-party provider adapters;
- correctness of concrete network transports;
- durability across process restart;
- production service availability; or
- research-baseline status.

## Rule for future public additions

Before adding a new architectural slice:

1. establish exact source identity;
2. inspect transitive dependencies;
3. remove private or organization-specific coupling;
4. review the sanitization diff;
5. execute appropriate tests;
6. record known limitations;
7. avoid expanding claims beyond evidence.