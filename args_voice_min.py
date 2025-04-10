#!/usr/bin/env python3

"""
Example ParlerTTS Script
------------------------
This script uses the ParlerTTS model to generate speech. It takes a textual
description (speaker style) and a prompt (what the speaker says) and outputs
a .wav file.
"""

import argparse
import logging
import sys

import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the text-to-speech script.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate speech using ParlerTTS."
    )

    parser.add_argument(
        "-d", "--description",
        required=True,
        help="Describes the speaker's style (e.g., 'A female speaker ...')."
    )

    parser.add_argument(
        "-p", "--prompt",
        required=True,
        help="The text prompt that the speaker will say."
    )

    parser.add_argument(
        "-o", "--output",
        default="parler_tts_out.wav",
        help="Path to the output WAV file."
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging."
    )

    return parser.parse_args()


def configure_logging(verbose: bool) -> None:
    """
    Configure the logging level based on verbosity.
    
    Args:
        verbose (bool): If True, sets logging to DEBUG level; otherwise INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def main() -> None:
    """
    Main function to generate speech using the ParlerTTS model.
    """
    args = parse_arguments()
    configure_logging(args.verbose)

    logger = logging.getLogger(__name__)

    # Select device
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device}")

    # Load model and tokenizer
    model_name = "parler-tts/parler-tts-mini-v1"
    logger.info(f"Loading model and tokenizer from: {model_name}")
    model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenize description and prompt
    logger.debug(f"Description: {args.description}")
    description_ids = tokenizer(args.description, return_tensors="pt").input_ids.to(device)

    logger.debug(f"Prompt: {args.prompt}")
    prompt_ids = tokenizer(args.prompt, return_tensors="pt").input_ids.to(device)

    # Generate the audio
    logger.info("Generating speech...")
    generation = model.generate(input_ids=description_ids, prompt_input_ids=prompt_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    # Write to WAV file
    output_file = args.output
    sampling_rate = model.config.sampling_rate
    logger.info(f"Saving output to: {output_file}")
    sf.write(output_file, audio_arr, sampling_rate)

    logger.info("Speech generation complete.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted by user")
