from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


REQUIRED_PUBLIC_PRODUCT_NAMES = (
    'Lumi Layered Memory',
    'Nuances',
    'Presence',
)


def test_required_playground_structure_exists():
    required = [
        'core/layered-memory',
        'core/nuances',
        'core/presence',
        'adapters/hermes',
        'installers/lumi-for-hermes',
        'docs/README.md',
        'docs/architecture.md',
        'docs/host-compatibility.md',
        'docs/memory-provider-compatibility.md',
        'docs/release-boundary.md',
        'docs/product-brief.md',
        'docs/licensing.md',
        'docs/release-checklist.md',
        'LICENSE',
        'LICENSE-DOCS.md',
        'NOTICE.md',
        'scripts/release_check.sh',
        'scripts/public_secret_scan.py',
    ]
    missing = [p for p in required if not (ROOT / p).exists()]
    assert not missing, missing


def test_openclaw_adapter_is_not_added_before_compatibility_research():
    assert not (ROOT / 'adapters/openclaw').exists()
    assert not (ROOT / 'installers/lumi-for-openclaw').exists()


def test_public_docs_use_product_names():
    docs = [
        ROOT / 'README.md',
        ROOT / 'docs' / 'README.md',
        ROOT / 'docs' / 'architecture.md',
        ROOT / 'docs' / 'product-brief.md',
        ROOT / 'docs' / 'host-compatibility.md',
        ROOT / 'docs' / 'memory-provider-compatibility.md',
        ROOT / 'docs' / 'release-boundary.md',
    ]
    for doc in docs:
        text = doc.read_text(encoding='utf-8')
        missing = [name for name in REQUIRED_PUBLIC_PRODUCT_NAMES if name not in text]
        assert not missing, f'{doc.relative_to(ROOT)} missing product names: {missing}'


def test_license_model_matches_related_lumi_repos():
    assert 'MIT License' in (ROOT / 'LICENSE').read_text(encoding='utf-8')
    docs_license = (ROOT / 'LICENSE-DOCS.md').read_text(encoding='utf-8')
    assert 'Creative Commons Attribution 4.0 International License' in docs_license
    notice = (ROOT / 'NOTICE.md').read_text(encoding='utf-8')
    assert 'split license model' in notice


def test_memory_provider_compatibility_keeps_main_memory_authoritative():
    contract = (ROOT / 'docs' / 'memory-provider-compatibility.md').read_text(encoding='utf-8')
    required_claims = [
        'The underlying memory provider remains authoritative',
        'The default write mode is **no write**',
        'direct silent edits to Obsidian notes',
        'direct silent edits to Hermes durable memory files',
        'A Lumi compatibility run must not change the canonical memory provider',
    ]
    missing = [claim for claim in required_claims if claim not in contract]
    assert not missing, missing


def test_hermes_adapter_documents_read_only_preview_boundary():
    adapter = (ROOT / 'adapters' / 'hermes' / 'README.md').read_text(encoding='utf-8')
    required_claims = [
        "Hermes' selected memory provider remains authoritative",
        'Lumi reads selected context only through explicit host configuration',
        'Lumi emits proposals and receipts before any durable write',
        'Default preview mode is read-only plus reviewable proposal/receipt output',
    ]
    missing = [claim for claim in required_claims if claim not in adapter]
    assert not missing, missing


def test_memory_provider_conflicts_preserve_ambiguity_instead_of_merging():
    contract = (ROOT / 'docs' / 'memory-provider-compatibility.md').read_text(encoding='utf-8')
    assert 'Multiple memory providers disagree' in contract
    assert 'preserves ambiguity' in contract or 'preserve ambiguity' in contract
    assert 'do not invent a merged fact' in contract
