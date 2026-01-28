EFFECT_MULTIPLIER = {
    "supports": 1.0,
    "weakens": -0.7,
    "blocks": -2.0,
}


def score_option(claim_links):
    score = 0.0
    reasons = []

    for link in claim_links:
        claim = link.claim

        m = EFFECT_MULTIPLIER[link.effect.value]
        contribution = claim.confidence * link.weight * m

        score += contribution

        reasons.append(
            f"{link.effect.value.upper()}: {claim.text[:80]}... => {contribution:.3f}"
        )

    return score, reasons
