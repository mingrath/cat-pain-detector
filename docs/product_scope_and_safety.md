# Product Scope and Safety Language

## Product Positioning

Cat Pain Detector is a **triage-support tool** for identifying visible feline acute pain indicators from cat face images using Feline Grimace Scale concepts.

It is designed to help:

- cat owners notice possible pain cues earlier
- shelters and foster homes prioritize which cats may need closer observation
- veterinary teams communicate visible pain indicators with structured evidence
- judges understand a concrete health/science use case for Gemma 4 multimodal reasoning

## What The Product Can Say

Approved language:

- “Possible pain indicators detected.”
- “This image shows visible cues associated with the Feline Grimace Scale.”
- “The model estimates a higher/lower FGS-style score based on visible facial cues.”
- “Consider contacting a veterinarian if these signs are new, severe, or paired with behavior changes.”
- “This result is uncertain because some action units are not clearly visible.”

## What The Product Must Not Say

Avoid:

- “Your cat is in pain.”
- “Your cat is healthy.”
- “No vet visit is needed.”
- “Give medication.”
- “This diagnoses injury, disease, dental pain, or surgical pain.”
- “Clinically validated” unless we have validation metrics on appropriate FGS-labeled data.

## Standard Disclaimer

Use this in the app, README, report, and generated analysis:

> This prototype is triage support only and is not a veterinary diagnosis. It estimates visible Feline Grimace Scale-style cues from an image. If your cat appears distressed, injured, unusually quiet, not eating, hiding, limping, struggling to breathe, or suddenly changed in behavior, contact a veterinarian promptly.

## Recommendation Tiers

The app may use these safety-framed tiers:

- **Low visible concern:** Few FGS-style indicators visible. Continue normal observation. If behavior has changed, contact a veterinarian.
- **Monitor closely:** Some visible pain indicators or medium uncertainty. Recheck in a calm setting and consider veterinary advice if signs persist.
- **Contact a veterinarian:** Multiple visible pain indicators, high FGS-style score, or concerning context supplied by the user.
- **Cannot assess:** Image is unclear, cat face is not visible, cat is sleeping/grooming, or key action units are occluded.

## Human Factors

- Show evidence for each action unit, not just a total score.
- Show uncertainty prominently.
- Make “contact a veterinarian” a safe next step, not a panic message.
- Never shame owners for missing subtle signs.
- Avoid false reassurance when the image is low quality or incomplete.

## Hackathon Claim Boundary

Until FGS-labeled validation data is available:

- allowed: “research prototype,” “validation-first design,” “FGS-inspired structured reasoning”
- not allowed: “accurate,” “validated detector,” “clinical-grade,” “diagnostic”

After validation data is available:

- claims must cite `metrics/*.json` and the exact validation set size/source.
- report false negatives visibly because missing pain indicators is the highest-risk error.

