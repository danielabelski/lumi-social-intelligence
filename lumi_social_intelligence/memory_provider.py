"""Provider-neutral memory compatibility packets.

This module is deliberately small and public-safe. It models the Sprint 1
boundary: hosts keep owning storage, Lumi receives explicit context packets,
and Presence returns decisions/proposals/receipts instead of mutating providers.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any


class CompatibilityPacketError(ValueError):
    """Raised when provider context cannot safely enter the Lumi path."""


class CompatibilityPacketSchemaError(CompatibilityPacketError):
    """Raised when a packet violates the frozen compatibility-packet contract."""


# The frozen v1 contract. ``build_compatibility_packet`` must produce exactly these keys with
# exactly these value types; ``validate_compatibility_packet`` enforces that. Keeping the key
# sets here — one named place — is what makes the ``v1`` schema id a checkable promise rather
# than a label. Adding a key to the packet means adding it here and bumping ``v1``.
COMPATIBILITY_PACKET_SCHEMA = 'lumi.memory_provider.compatibility_packet.v1'

COMPATIBILITY_PACKET_KEYS = frozenset({
    'schema',
    'source',
    'compatibility_view',
    'requested_effect',
    'write_mode',
})

COMPATIBILITY_PACKET_SOURCE_KEYS = frozenset({
    'provider',
    'source_id',
    'timestamp',
    'confidence',
})

COMPATIBILITY_PACKET_PROVENANCE_KEYS = frozenset({
    'provider',
    'source_id',
    'timestamp',
    'confidence',
})

COMPATIBILITY_PACKET_VIEW_KEYS = frozenset({
    'normalized_summary',
    'provenance',
    'ambiguity',
    'conflicts',
    'merged_fact',
})


@dataclass(frozen=True)
class _SourceContext:
    provider: str
    source_id: str
    text: str
    confidence: float
    timestamp: str | None
    requested_effect: str | None
    write_mode: str
    conflicts: tuple[dict[str, Any], ...]


def build_compatibility_packet(source: dict[str, Any]) -> dict[str, Any]:
    """Build a provider-neutral Lumi compatibility packet.

    The input mapping is copied and never mutated. Missing provider/source/text
    metadata fails closed because provenance is part of the compatibility
    contract, not decoration.
    """

    context = _parse_source(source)
    normalized_summary = _normalize_summary(context.text)
    conflicts = [deepcopy(item) for item in context.conflicts]
    has_conflict = bool(conflicts)

    return {
        'schema': 'lumi.memory_provider.compatibility_packet.v1',
        'source': {
            'provider': context.provider,
            'source_id': context.source_id,
            'timestamp': context.timestamp,
            'confidence': context.confidence,
        },
        'compatibility_view': {
            'normalized_summary': normalized_summary,
            'provenance': {
                'provider': context.provider,
                'source_id': context.source_id,
                'timestamp': context.timestamp,
                'confidence': context.confidence,
            },
            'ambiguity': 'preserved' if has_conflict else 'none_detected',
            'conflicts': conflicts,
            'merged_fact': None if has_conflict else normalized_summary,
        },
        'requested_effect': context.requested_effect,
        'write_mode': context.write_mode,
    }


def validate_compatibility_packet(payload: Any) -> dict[str, Any]:
    """Enforce the frozen v1 compatibility-packet contract on ``payload``.

    Raises :class:`CompatibilityPacketSchemaError` on a missing key, an unknown/extra key, a
    wrong-typed value, or a schema id that is not the frozen ``v1`` one. Returns the payload
    unchanged on success so callers may chain it.

    This is for tests and explicit callers. It is deliberately **not** called from the live
    turn path: a validation failure there could break a real turn, which is not a risk worth
    the safety it would buy. Validation is opt-in.
    """

    if not isinstance(payload, dict):
        raise CompatibilityPacketSchemaError(
            f'compatibility packet must be a mapping, got {type(payload).__name__}'
        )

    _require_key_set('packet', payload, COMPATIBILITY_PACKET_KEYS)

    schema = payload['schema']
    _require_type('schema', schema, str)
    if schema != COMPATIBILITY_PACKET_SCHEMA:
        raise CompatibilityPacketSchemaError(
            f"schema must be {COMPATIBILITY_PACKET_SCHEMA!r}, got {schema!r}"
        )

    source = payload['source']
    _require_type('source', source, dict)
    _require_key_set('source', source, COMPATIBILITY_PACKET_SOURCE_KEYS)
    _require_type('source.provider', source['provider'], str)
    _require_type('source.source_id', source['source_id'], str)
    _require_optional_type('source.timestamp', source['timestamp'], str)
    _require_type('source.confidence', source['confidence'], (int, float))

    view = payload['compatibility_view']
    _require_type('compatibility_view', view, dict)
    _require_key_set('compatibility_view', view, COMPATIBILITY_PACKET_VIEW_KEYS)
    _require_type('compatibility_view.normalized_summary', view['normalized_summary'], str)
    _require_type('compatibility_view.ambiguity', view['ambiguity'], str)
    _require_type('compatibility_view.conflicts', view['conflicts'], list)

    provenance = view['provenance']
    _require_type('compatibility_view.provenance', provenance, dict)
    _require_key_set(
        'compatibility_view.provenance',
        provenance,
        COMPATIBILITY_PACKET_PROVENANCE_KEYS,
    )
    _require_type('compatibility_view.provenance.provider', provenance['provider'], str)
    _require_type('compatibility_view.provenance.source_id', provenance['source_id'], str)
    _require_optional_type('compatibility_view.provenance.timestamp', provenance['timestamp'], str)
    _require_type(
        'compatibility_view.provenance.confidence',
        provenance['confidence'],
        (int, float),
    )

    _require_optional_type('requested_effect', payload['requested_effect'], str)
    _require_type('write_mode', payload['write_mode'], str)

    return payload


def _require_key_set(name: str, mapping: dict[str, Any], expected: frozenset[str]) -> None:
    actual = set(mapping)
    missing = expected - actual
    if missing:
        raise CompatibilityPacketSchemaError(
            f'{name} is missing required key(s): {sorted(missing)}'
        )
    extra = actual - expected
    if extra:
        raise CompatibilityPacketSchemaError(
            f'{name} has unknown key(s): {sorted(extra)}'
        )


def _require_type(name: str, value: Any, expected: type | tuple[type, ...]) -> None:
    if not isinstance(value, expected):
        raise CompatibilityPacketSchemaError(
            f'{name} must be {_type_name(expected)}, got {type(value).__name__}'
        )


def _require_optional_type(name: str, value: Any, expected: type | tuple[type, ...]) -> None:
    if value is None:
        return
    _require_type(name, value, expected)


def _type_name(expected: type | tuple[type, ...]) -> str:
    if isinstance(expected, tuple):
        return ' or '.join(item.__name__ for item in expected)
    return expected.__name__


def decide_presence_from_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Return a fail-closed Presence decision for a compatibility packet."""

    view = packet.get('compatibility_view') or {}
    requested_effect = packet.get('requested_effect')
    write_mode = packet.get('write_mode', 'none')

    if view.get('conflicts'):
        return {
            'decision': 'ask_or_wait',
            'reason': 'Conflicting provider context: preserve ambiguity; do not invent a merged fact.',
            'provider_mutation': False,
            'proposal': None,
            'receipt': _receipt(packet, 'ambiguity_preserved'),
        }

    if requested_effect == 'write' and write_mode == 'none':
        return {
            'decision': 'blocked',
            'reason': 'Write requested while adapter write_mode is none.',
            'provider_mutation': False,
            'proposal': None,
            'receipt': _receipt(packet, 'no_write'),
        }

    if write_mode in {'proposal', 'receipt', 'reviewed-write'}:
        proposal = {
            'summary': view.get('normalized_summary'),
            'requires_review': True,
            'target_provider': (packet.get('source') or {}).get('provider'),
        }
    else:
        proposal = {
            'summary': view.get('normalized_summary'),
            'requires_review': True,
            'target_provider': None,
        }

    return {
        'decision': 'review_proposal',
        'reason': 'Context can inform a reviewable Lumi decision without mutating provider storage.',
        'provider_mutation': False,
        'proposal': proposal,
        'receipt': _receipt(packet, 'proposal_only'),
    }


def _parse_source(source: dict[str, Any]) -> _SourceContext:
    if not isinstance(source, dict):
        raise CompatibilityPacketError('source must be a mapping')

    copied = deepcopy(source)
    provider = _required_text(copied, 'provider')
    source_id = _required_text(copied, 'source_id')
    text = _required_text(copied, 'text')

    confidence = copied.get('confidence', 0.5)
    if not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
        raise CompatibilityPacketError('confidence must be a number between 0 and 1')

    conflicts_value = copied.get('conflicts', [])
    if conflicts_value is None:
        conflicts_value = []
    if not isinstance(conflicts_value, list):
        raise CompatibilityPacketError('conflicts must be a list when provided')

    return _SourceContext(
        provider=provider,
        source_id=source_id,
        text=text,
        confidence=float(confidence),
        timestamp=copied.get('timestamp'),
        requested_effect=copied.get('requested_effect'),
        write_mode=copied.get('write_mode', 'none'),
        conflicts=tuple(deepcopy(conflicts_value)),
    )


def _required_text(source: dict[str, Any], field: str) -> str:
    value = source.get(field)
    if not isinstance(value, str) or not value.strip():
        raise CompatibilityPacketError(f'missing required {field}')
    return value.strip()


def _normalize_summary(text: str) -> str:
    return ' '.join(text.strip().split()).rstrip('.')


def _receipt(packet: dict[str, Any], effect: str) -> dict[str, Any]:
    source = packet.get('source') or {}
    return {
        'effect': effect,
        'provider': source.get('provider'),
        'source_id': source.get('source_id'),
        'provider_mutation': False,
    }
