import os
from spleeter.separator import Separator

def separate_stems(input_path: str, output_dir: str, stems: int = 2) -> list[str]:
    """Separate audio into stems using Spleeter."""
    if stems not in (2, 4, 5):
        raise ValueError(f"Unsupported number of stems: {stems}")
    model = f"spleeter:{stems}stems"
    separator = Separator(model)
    separator.separate_to_file(input_path, output_dir, codec='wav')
    # Collect generated stem files
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    stems_folder = os.path.join(output_dir, base_name)
    files = []
    for root, _, filenames in os.walk(stems_folder):
        for fname in filenames:
            files.append(os.path.join(root, fname))
    return files
