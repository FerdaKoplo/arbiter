from collections import defaultdict, deque

EFFECT_MULTIPLIER = {
    "supports": 1.0,
    "weakens": -0.7,
    "blocks": -2.0,
}


def score_option_with_propagation(claim_links, max_depth=2):
    graph = defaultdict(list)
    base_confidence = {}

    for link in claim_links:
        claim = link.claim
        graph[claim.id].extend(claim.outgoing_relations)  # outgoing ClaimRelation
        base_confidence[claim.id] = (
            claim.confidence * link.weight * EFFECT_MULTIPLIER[link.effect.value]
        )

    final_scores = defaultdict(float)
    visited = set()

    for link in claim_links:
        claim = link.claim
        base_confidence[claim.id] = (
            claim.confidence * link.weight * EFFECT_MULTIPLIER[link.effect.value]
        )

        propagate_claim(
            claim,
            base_confidence[claim.id],
            graph,
            final_scores,
            visited,
            depth=0,
            max_depth=max_depth,
        )

    reasons = []
    for link in claim_links:
        claim = link.claim
        contrib = base_confidence[claim.id]
        reasons.append(
            f"{link.effect.value.upper()}: {claim.text[:80]}... => {contrib:.3f}"
        )

    total_score = sum(final_scores.values())
    return total_score, reasons


def propagate_claim(claim, influence, graph, final_scores, visited, depth, max_depth):
    if depth > max_depth or (claim.id, depth) in visited:
        return

    visited.add((claim.id, depth))
    final_scores[claim.id] += influence

    for rel in graph.get(claim.id, []):
        next_influence = influence * 0.5
        propagate_claim(
            rel.to_claim,
            next_influence,
            graph,
            final_scores,
            visited,
            depth + 1,
            max_depth,
        )
