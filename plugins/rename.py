import os

def apply_text_transforms(filename, prefix="", suffix="", replace_from="", replace_to=""):
    """
    Applies prefix, suffix, and word replacement to a filename while preserving its extension.
    """
    name, ext = os.path.splitext(filename)
    
    # Simple word replacement
    if replace_from:
        name = name.replace(replace_from, replace_to)
        
    # Append Prefix & Suffix
    new_filename = f"{prefix}{name}{suffix}{ext}"
    return new_filename
  
