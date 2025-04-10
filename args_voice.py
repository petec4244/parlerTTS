#!/usr/bin/env python3
"""
Example ParlerTTS Script with Additional Parameters
--------------------------------------------------
This script uses the ParlerTTS model to generate speech. It allows you to:
- Specify a model from a list of popular ParlerTTS variants.
- Provide a textual description of the speaker style.
- Provide a prompt for the speaker to say.
- Control the output filename strategy: default, increment, or random.
"""

import argparse
import logging
import sys
import os
import uuid

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
        "-m", "--model_name",
        default="parler-tts/parler-tts-mini-v1",
        choices=[
            "parler-tts/parler-tts-mini-v1",
            "parler-tts/parler-tts-medium-v1",
            "parler-tts/parler-tts-large-v1"
        ],
        help="Name of the ParlerTTS model to use."
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
        "-f", "--filename_strategy",
        default="default",
        choices=["default", "increment", "random"],
        help="How to handle filename conflicts or defaults: "
             "'default' (use exactly what's provided), "
             "'increment' (append a number if a file exists), "
             "'random' (use a random suffix)."
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


def apply_filename_strategy(
    filename: str,
    strategy: str
) -> str:
    """
    Applies the user-chosen filename strategy to determine
    the final output filename.

    If strategy is:
      - 'default': Use filename as is.
      - 'increment': If filename exists, add a suffix like '_1', '_2', etc.
      - 'random': If filename exists or is the default, append a random suffix.

    Note: For demonstration, we only apply increment/random if the filename
    is the default 'parler_tts_out.wav' (or if it already exists). If you want
    to always apply them, remove the relevant checks below.

    Args:
        filename (str): The proposed output filename.
        strategy (str): "default", "increment", or "random".

    Returns:
        str: The resolved filename after applying the strategy.
    """
    # If user specified a custom filename that doesn't match the default,
    # and the strategy is not "default", you can decide whether to skip or apply.
    default_name = "parler_tts_out.wav"
    is_default_name = (filename == default_name)

    # If strategy is 'default', do nothing:
    if strategy == "default":
        return filename

    # If user set 'increment' and the filename is the default or exists, rename incrementally.
    if strategy == "increment" and (is_default_name or os.path.exists(filename)):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(new_filename):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1
        return new_filename

    # If strategy is 'random' and the filename is the default or already exists, rename randomly.
    if strategy == "random" and (is_default_name or os.path.exists(filename)):
        base, ext = os.path.splitext(filename)
        suffix = uuid.uuid4().hex[:6]  # short random suffix
        random_filename = f"{base}_{suffix}{ext}"
        while os.path.exists(random_filename):
            # Keep generating until we find one that doesn't exist
            suffix = uuid.uuid4().hex[:6]
            random_filename = f"{base}_{suffix}{ext}"
        return random_filename

    return filename


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
    logger.info(f"Loading model '{args.model_name}'")
    model = ParlerTTSForConditionalGeneration.from_pretrained(args.model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    # Tokenize description and prompt
    logger.debug(f"Description: {args.description}")
    description_ids = tokenizer(args.description, return_tensors="pt").input_ids.to(device)

    logger.debug(f"Prompt: {args.prompt}")
    prompt_ids = tokenizer(args.prompt, return_tensors="pt").input_ids.to(device)

    # Generate the audio
    logger.info("Generating speech...")
    generation = model.generate(input_ids=description_ids, prompt_input_ids=prompt_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    # Determine final output filename based on user strategy
    output_file = apply_filename_strategy(args.output, args.filename_strategy)
    logger.info(f"Final output file: {output_file}")

    # Write to WAV file
    sampling_rate = model.config.sampling_rate
    sf.write(output_file, audio_arr, sampling_rate)
    logger.info("Speech generation complete.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted by user")
