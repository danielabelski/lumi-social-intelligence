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
