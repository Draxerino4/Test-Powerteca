import os
import json

# --- Configuration ---
ROOT = "flows"
OUTPUT = "flows.json"
DESCRIPTION_FILENAME = "description.txt"
INSTRUCTIONS_FILENAME = "instructions.txt"
# --- End Configuration ---

def _read_file_content(file_path: str) -> str:
    """Reads the full content of a file, returning an empty string on error."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Warning: Could not read file '{file_path}': {e}")
    return ""

result = []

# Check if the root directory exists
if not os.path.isdir(ROOT):
    print(f"Error: The directory '{ROOT}' does not exist.")
    # Create the directory to avoid errors on the next run
    os.makedirs(ROOT)
    print(f"Created an empty '{ROOT}' directory for you.")
else:
    for folder in sorted(os.listdir(ROOT)):
        full_folder = os.path.join(ROOT, folder)
        if not os.path.isdir(full_folder):
            continue

        # Define the paths for the description and instructions files
        desc_file_path = os.path.join(full_folder, DESCRIPTION_FILENAME)
        instr_file_path = os.path.join(full_folder, INSTRUCTIONS_FILENAME)

        flow = {
            "name": folder,
            "description": _read_file_content(desc_file_path),
            "instructions": _read_file_content(instr_file_path),
            "tabs": []
        }

        for file in sorted(os.listdir(full_folder)):
            # Make sure we don't process the description/instructions files as tabs
            if file.lower().endswith(".txt") and file not in [DESCRIPTION_FILENAME, INSTRUCTIONS_FILENAME]:
                full_path = os.path.join(full_folder, file)

                # Get first line as description for the tab
                tab_description = ""
                try:
                    with open(full_path, "r", encoding="utf8") as f:
                        tab_description = f.readline().strip()
                except Exception as e:
                    print(f"Warning: Could not read tab file '{full_path}': {e}")
                    tab_description = ""

                flow["tabs"].append({
                    "tabName": os.path.splitext(file)[0],
                    "file": f"{ROOT}/{folder}/{file}",
                    "description": tab_description
                })

        # Only add the flow if it has tabs, a description, or instructions
        if flow["tabs"] or flow["description"] or flow["instructions"]:
            result.append(flow)

    with open(OUTPUT, "w", encoding="utf8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Successfully generated {OUTPUT} with {len(result)} flow(s).")
