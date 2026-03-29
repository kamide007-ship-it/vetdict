#!/usr/bin/env python3
"""
Disease Batch Enricher Module

Uses Claude Batches API (50% cost reduction) to enrich disease data in bulk.
Processes up to 100,000 requests per batch for maximum cost efficiency.
"""

import json
import os
import time
from typing import List

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request


class DiseaseBatchEnricher:
    """Batch enrichment of disease data using Claude API."""

    def __init__(self, model: str = "claude-opus-4-6"):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def _build_enrichment_prompt(self, disease: dict) -> str:
        """Build prompt for enriching a disease."""
        disease_name = disease.get("name", "Unknown")
        disease_name_ja = disease.get("name_ja", disease_name)
        description = disease.get("description", "")

        return f"""You are a veterinary medicine expert. For this disease, generate missing medical information.

Disease: {disease_name} / {disease_name_ja}
Description: {description}

Generate JSON with these fields (use empty string "" if unable to generate):
{{
  "pathophysiology": "mechanism of disease",
  "pathophysiology_ja": "病態生理",
  "causes": "primary and secondary causes",
  "causes_ja": "原因",
  "treatment": "treatment approaches",
  "treatment_ja": "治療法",
  "prevention": "prevention strategies",
  "prevention_ja": "予防法",
  "prognosis": "expected outcomes",
  "prognosis_ja": "予後"
}}

Return ONLY valid JSON. Be concise (2-3 sentences each)."""

    def create_batch_requests(
        self, diseases: List[dict], batch_size: int = 100000
    ) -> List[List[Request]]:
        """Create batch requests for disease enrichment."""
        batches = []
        current_batch = []

        for i, disease in enumerate(diseases):
            # Skip if all fields present
            if all(
                disease.get(f)
                for f in [
                    "pathophysiology",
                    "pathophysiology_ja",
                    "causes",
                    "causes_ja",
                    "treatment",
                    "treatment_ja",
                    "prevention",
                    "prevention_ja",
                    "prognosis",
                    "prognosis_ja",
                ]
            ):
                continue

            prompt = self._build_enrichment_prompt(disease)
            request = Request(
                custom_id=f"disease-{i}",
                params=MessageCreateParamsNonStreaming(
                    model=self.model,
                    max_tokens=512,
                    messages=[{"role": "user", "content": prompt}],
                ),
            )
            current_batch.append(request)

            if len(current_batch) >= batch_size:
                batches.append(current_batch)
                current_batch = []

        if current_batch:
            batches.append(current_batch)

        return batches

    def submit_batch(self, requests: List[Request]) -> str:
        """Submit a batch for processing."""
        batch = self.client.messages.batches.create(requests=requests)
        print(f"Created batch {batch.id} with {len(requests)} requests")
        return batch.id

    def wait_for_batch(self, batch_id: str, poll_interval: int = 30) -> dict:
        """Wait for batch to complete."""
        while True:
            batch = self.client.messages.batches.retrieve(batch_id)
            print(
                f"Batch {batch_id}: {batch.processing_status} "
                f"(processing: {batch.request_counts.processing}, "
                f"succeeded: {batch.request_counts.succeeded})"
            )

            if batch.processing_status == "ended":
                return {
                    "id": batch_id,
                    "succeeded": batch.request_counts.succeeded,
                    "errored": batch.request_counts.errored,
                }

            time.sleep(poll_interval)

    def process_batch_results(
        self, batch_id: str, diseases: List[dict]
    ) -> List[dict]:
        """Process batch results and apply to disease records."""
        {d.get("name"): d for d in diseases}
        updated_count = 0

        for result in self.client.messages.batches.results(batch_id):
            if result.result.type != "succeeded":
                continue

            custom_id = result.custom_id
            message = result.result.message

            try:
                # Extract JSON from response
                response_text = next(
                    (b.text for b in message.content if b.type == "text"), ""
                )
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1

                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    enriched_data = json.loads(json_str)

                    # Find and update disease (simple lookup by index)
                    disease_index = int(custom_id.split("-")[1])
                    if disease_index < len(diseases):
                        disease = diseases[disease_index]
                        for key, value in enriched_data.items():
                            if value and not disease.get(key):
                                disease[key] = value
                        updated_count += 1

            except (json.JSONDecodeError, ValueError, IndexError) as e:
                print(f"Error processing result {custom_id}: {e}")

        print(f"Updated {updated_count} diseases from batch {batch_id}")
        return diseases

    def enrich_diseases_batch(
        self, diseases: List[dict], wait: bool = True
    ) -> dict:
        """Enrich diseases using batch API."""
        batches = self.create_batch_requests(diseases)
        print(f"Created {len(batches)} batch(es)")

        batch_ids = []
        for batch_requests in batches:
            batch_id = self.submit_batch(batch_requests)
            batch_ids.append(batch_id)

        if not wait:
            return {"batch_ids": batch_ids, "status": "submitted"}

        results = []
        for batch_id in batch_ids:
            result = self.wait_for_batch(batch_id)
            results.append(result)
            self.process_batch_results(batch_id, diseases)

        return {
            "batch_ids": batch_ids,
            "results": results,
            "status": "completed",
        }


def main():
    """Example batch enrichment."""
    from api.species.dog_diseases import DISEASES as _DISEASE_DB

    enricher = DiseaseBatchEnricher()

    # Create batch requests
    batches = enricher.create_batch_requests(_DISEASE_DB)
    print(f"Will process {len(batches)} batch(es)")
    print(f"Total requests: {sum(len(b) for b in batches)}")

    # Submit first batch as demo (set wait=False to submit without waiting)
    if batches:
        batch_id = enricher.submit_batch(batches[0])
        print(f"\nBatch submitted: {batch_id}")
        print("Note: Set wait=True to poll for completion (may take hours)")


if __name__ == "__main__":
    main()
