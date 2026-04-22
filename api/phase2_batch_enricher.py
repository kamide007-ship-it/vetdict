#!/usr/bin/env python3
"""
Phase 2 Batch Enricher Module - Treatment, Prevention, and Prognosis Enrichment

Extends Phase 1 enrichment with three critical medical fields:
- treatment (治療): treatment protocols and approaches
- prevention (予防): preventive measures and vaccines
- prognosis (予後): expected outcomes and recovery timelines

Uses Claude Batches API for cost-effective bulk processing.
"""

import json
import os
from typing import List

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request


class Phase2BatchEnricher:
    """Batch enrichment of Phase 2 fields (treatment, prevention, prognosis)."""

    def __init__(self, model: str = "claude-opus-4-6"):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def _build_treatment_prompt(self, disease: dict) -> str:
        """Build prompt for treatment field enrichment."""
        disease_name = disease.get("name", "Unknown")
        disease_name_ja = disease.get("name_ja", disease_name)
        species = disease.get("species", "Unknown")

        # Use existing Phase 1 data as context if available
        pathophysiology = disease.get("pathophysiology", "")
        causes = disease.get("causes", "")

        context = "\nPhase 1 Context (if available):\n"
        if pathophysiology:
            context += f"- Pathophysiology: {pathophysiology[:300]}...\n"
        if causes:
            context += f"- Causes: {causes[:300]}...\n"

        return f"""You are a veterinary medicine expert specializing in {species} species medicine.

Disease: {disease_name} ({species}) / {disease_name_ja}{context}

Generate ONLY a JSON object with exactly these two fields:
{{
  "treatment": "Concise treatment protocol (2-3 sentences, 150-250 chars). Include specific medications, procedures, or supportive care. Focus on veterinary practice.",
  "treatment_ja": "獣医学的な治療法（2-3文、150～250文字）。具体的な薬剤、手術、または対症療法を含めてください。"
}}

Important:
1. Return ONLY valid JSON, no markdown or extra text
2. Both fields must be non-empty strings
3. Focus on practical veterinary applications
4. Include specific medications/procedures when applicable
5. Keep consistent terminology with Phase 1 pathophysiology
6. Ensure Japanese is natural and accurate
7. Translation should be 80-120% of English length"""

    def _build_prevention_prompt(self, disease: dict) -> str:
        """Build prompt for prevention field enrichment."""
        disease_name = disease.get("name", "Unknown")
        disease_name_ja = disease.get("name_ja", disease_name)
        species = disease.get("species", "Unknown")
        causes = disease.get("causes", "")

        context = f"\nPhase 1 Context - Causes: {causes[:300]}...\n" if causes else ""

        return f"""You are a veterinary medicine expert specializing in {species} species disease prevention.

Disease: {disease_name} ({species}) / {disease_name_ja}{context}

Generate ONLY a JSON object with exactly these two fields:
{{
  "prevention": "Prevention strategies (2-3 sentences, 150-250 chars). Include vaccination protocols, management, dietary measures, and risk reduction.",
  "prevention_ja": "予防戦略（2-3文、150～250文字）。ワクチン接種プログラム、環境管理、栄養対策を含めてください。"
}}

Important:
1. Return ONLY valid JSON, no markdown or extra text
2. Both fields must be non-empty strings
3. Include vaccine schedules if applicable
4. Focus on environmental management and risk mitigation
5. Be species-specific and practical
6. Provide timeline information where relevant
7. Japanese should match English intent and length"""

    def _build_prognosis_prompt(self, disease: dict) -> str:
        """Build prompt for prognosis field enrichment."""
        disease_name = disease.get("name", "Unknown")
        disease_name_ja = disease.get("name_ja", disease_name)
        species = disease.get("species", "Unknown")
        pathophysiology = disease.get("pathophysiology", "")

        context = f"\nPhase 1 Context - Pathophysiology: {pathophysiology[:300]}...\n" if pathophysiology else ""

        return f"""You are a veterinary medicine expert with experience in {species} species prognosis assessment.

Disease: {disease_name} ({species}) / {disease_name_ja}{context}

Generate ONLY a JSON object with exactly these two fields:
{{
  "prognosis": "Expected outcomes (2-3 sentences, 150-250 chars). Include recovery timeline, survival rates, potential complications, and prognostic factors.",
  "prognosis_ja": "予後（2-3文、150～250文字）。回復期間、生存率、潜在的な合併症、予後因子を含めてください。"
}}

Important:
1. Return ONLY valid JSON, no markdown or extra text
2. Both fields must be non-empty strings
3. Include estimated recovery timeframes
4. Mention survival rates or outcomes where known
5. Note complications and unfavorable factors
6. Be evidence-based and realistic
7. Japanese should be medically accurate and appropriate length"""

    def create_phase2_batch_requests(
        self, diseases: List[dict], stage: str = "treatment", batch_size: int = 100
    ) -> List[List[Request]]:
        """Create batch requests for Phase 2 enrichment.

        Args:
            diseases: List of disease dictionaries to enrich
            stage: Which field to enrich: "treatment", "prevention", or "prognosis"
            batch_size: Max requests per batch (Anthropic limit: 100,000)

        Returns:
            List of batch request lists
        """
        if stage not in ["treatment", "prevention", "prognosis"]:
            raise ValueError(f"Invalid stage: {stage}. Must be treatment, prevention, or prognosis")

        batches = []
        current_batch = []
        prompt_builder = {
            "treatment": self._build_treatment_prompt,
            "prevention": self._build_prevention_prompt,
            "prognosis": self._build_prognosis_prompt,
        }[stage]

        for i, disease in enumerate(diseases):
            # Skip if field already has content
            if disease.get(stage) and disease.get(f"{stage}_ja"):
                continue

            prompt = prompt_builder(disease)
            request = Request(
                custom_id=f"disease-{disease.get('id', i)}-{stage}",
                params=MessageCreateParamsNonStreaming(
                    model=self.model, max_tokens=768, messages=[{"role": "user", "content": prompt}]
                ),
            )
            current_batch.append(request)

            if len(current_batch) >= batch_size:
                batches.append(current_batch)
                current_batch = []

        if current_batch:
            batches.append(current_batch)

        return batches

    def submit_batch(self, requests: List[Request], description: str = "") -> str:
        """Submit a batch to the Anthropic Batches API.

        Args:
            requests: List of Request objects
            description: Human-readable description for tracking

        Returns:
            Batch ID string
        """
        if not requests:
            raise ValueError("No requests to submit")

        batch = self.client.messages.batches.create(requests=requests)

        print(f"✓ Submitted batch {batch.id}: {description}")
        print(f"  Requests: {len(requests)}")
        print(f"  Model: {self.model}")

        return batch.id

    def check_batch_status(self, batch_id: str) -> dict:
        """Check the status of a submitted batch.

        Args:
            batch_id: Batch ID to check

        Returns:
            Batch status dictionary
        """
        batch = self.client.messages.batches.retrieve(batch_id)

        # Build request counts - only include attributes that exist
        request_counts = {
            "succeeded": getattr(batch.request_counts, "succeeded", 0),
            "errored": getattr(batch.request_counts, "errored", 0),
        }

        # Add optional fields if they exist
        if hasattr(batch.request_counts, "expired"):
            request_counts["expired"] = batch.request_counts.expired
        if hasattr(batch.request_counts, "cancel_requested"):
            request_counts["cancel_requested"] = batch.request_counts.cancel_requested

        return {"id": batch.id, "status": batch.processing_status, "request_counts": request_counts}

    def retrieve_batch_results(self, batch_id: str) -> List[dict]:
        """Retrieve results from a completed batch.

        Args:
            batch_id: Batch ID to retrieve

        Returns:
            List of result dictionaries with custom_id and parsed content
        """
        batch = self.client.messages.batches.retrieve(batch_id)

        if batch.processing_status not in ["ended"]:
            raise ValueError(f"Batch {batch_id} is still processing (status: {batch.processing_status})")

        results = []

        # Iterate through batch results
        for result in self.client.messages.batches.results(batch_id):
            if result.result.type == "succeeded":
                # Parse the response content
                message_content = result.result.message.content[0]

                if message_content.type == "text":
                    try:
                        # Extract JSON from response text
                        text = message_content.text

                        # Try to parse as JSON directly
                        if text.startswith("{"):
                            parsed_json = json.loads(text)
                        else:
                            # Try to extract JSON from markdown code blocks
                            if "```json" in text:
                                json_str = text.split("```json")[1].split("```")[0].strip()
                            elif "```" in text:
                                json_str = text.split("```")[1].split("```")[0].strip()
                            else:
                                json_str = text

                            parsed_json = json.loads(json_str)

                        results.append({"custom_id": result.custom_id, "status": "succeeded", "data": parsed_json})
                    except (json.JSONDecodeError, IndexError) as e:
                        results.append(
                            {
                                "custom_id": result.custom_id,
                                "status": "parse_error",
                                "error": str(e),
                                "raw_text": message_content.text,
                            }
                        )
                else:
                    results.append(
                        {
                            "custom_id": result.custom_id,
                            "status": "unexpected_content_type",
                            "content_type": message_content.type,
                        }
                    )

            elif result.result.type == "errored":
                results.append(
                    {
                        "custom_id": result.custom_id,
                        "status": "errored",
                        "error": result.result.error.message
                        if hasattr(result.result.error, "message")
                        else str(result.result.error),
                    }
                )

            elif result.result.type == "expired":
                results.append({"custom_id": result.custom_id, "status": "expired"})

        return results
