"""
RECO3 integration for photo/video analysis in ShowDog API.

Analyzes input requests and output analysis results using RECO2's input_gate and output_gate.
"""

import datetime
import logging

try:
    from reco2 import input_gate, output_gate
    RECO3_AVAILABLE = True
except ImportError:
    RECO3_AVAILABLE = False
    logging.warning("RECO3 (reco2) module not available - analysis will proceed without AI self-control")

logger = logging.getLogger(__name__)


def analyze_request_input(breed_id: str, form_data: dict = None) -> dict:
    """
    Analyze user input (breed selection and request metadata).

    Args:
        breed_id: Selected breed ID
        form_data: Optional form data dict

    Returns:
        dict with analysis results (or empty dict if RECO3 unavailable)
    """
    if not RECO3_AVAILABLE:
        return {}

    # Simple text representation of the request
    text = f"Analyzing breed: {breed_id}"
    if form_data:
        text += f". Request details: {str(form_data)[:100]}"

    try:
        result = input_gate.analyze(text)
        logger.debug(f"Input analysis for {breed_id}: {result}")
        return result
    except Exception as e:
        logger.error(f"Input gate analysis failed: {e}", exc_info=True)
        return {"error": "input_analysis_failed"}


def analyze_photo_output(structure_result: dict, coat_result: dict) -> dict:
    """
    Analyze photo analysis output for assertions/contradictions.

    Args:
        structure_result: Output from analyze_photo_structure
        coat_result: Output from analyze_photo_coat

    Returns:
        dict with analysis results (or empty dict if RECO3 unavailable)
    """
    if not RECO3_AVAILABLE:
        return {}

    # Combine comments from both analyses
    comments = []
    if structure_result and "comments" in structure_result:
        comments.append(structure_result["comments"])
    if coat_result and "comments" in coat_result:
        comments.append(coat_result["comments"])

    output_text = " ".join(comments) if comments else "Photo analysis completed."

    try:
        result = output_gate.analyze(output_text)
        logger.debug(f"Photo output analysis: {result}")
        return result
    except Exception as e:
        logger.error(f"Output gate analysis failed: {e}", exc_info=True)
        return {"error": "output_analysis_failed"}


def analyze_video_output(video_result: dict) -> dict:
    """
    Analyze video analysis output for assertions/contradictions.

    Args:
        video_result: Output from analyze_video_frames

    Returns:
        dict with analysis results (or empty dict if RECO3 unavailable)
    """
    if not RECO3_AVAILABLE:
        return {}

    # Combine comments from all video analysis dimensions
    comments = []
    for key in ["gait", "temperament", "coat_motion"]:
        if key in video_result and "comments" in video_result[key]:
            comments.append(video_result[key]["comments"])

    output_text = " ".join(comments) if comments else "Video analysis completed."

    try:
        result = output_gate.analyze(output_text)
        logger.debug(f"Video output analysis: {result}")
        return result
    except Exception as e:
        logger.error(f"Output gate analysis failed: {e}", exc_info=True)
        return {"error": "output_analysis_failed"}


def add_reco3_metadata(response_data: dict, input_analysis: dict, output_analysis: dict) -> dict:
    """
    Augment API response with RECO3 analysis metadata.

    Args:
        response_data: The API response dict
        input_analysis: Results from analyze_request_input
        output_analysis: Results from analyze_*_output

    Returns:
        Modified response dict with reco3 metadata added
    """
    if not RECO3_AVAILABLE:
        return response_data

    response_data["reco3"] = {
        "input_analysis": input_analysis,
        "output_analysis": output_analysis,
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }
    return response_data
