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
