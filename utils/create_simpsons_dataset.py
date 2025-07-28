import json
import os
import re
from collections import defaultdict
import pandas as pd
from datasets import Dataset

def get_conversations(df, col1='raw_character_text', col2='spoken_words'):
    """
    Split a DataFrame into sub-DataFrames using rows where both specified columns are NaN as separators.
    
    Args:
        df (pd.DataFrame): The original DataFrame.
        col1 (str): Name of the first column to evaluate.
        col2 (str): Name of the second column to evaluate.

    Returns:
        list: List of sub-DataFrames.
    """
    # Find rows where both columns are NaN
    nan_rows = df[df[[col1, col2]].isna().all(axis=1)].index
    boundaries = list(nan_rows) + [len(df)]

    # Build segments using start and end indices
    start = 0
    segments = []
    for end in boundaries:
        chunk = df.iloc[start:end]
        if not chunk.empty:
            segments.append(chunk.reset_index(drop=True))
        start = end + 1

    return segments

def concat_consecutive_speakers(df, speaker_col='raw_character_text', text_col='spoken_words'):
    """
    Group and concatenate consecutive rows where the same character is speaking.
    
    Args:
        df (pd.DataFrame): Input DataFrame with dialogue.
        speaker_col (str): Column name with character names.
        text_col (str): Column name with spoken text.

    Returns:
        pd.DataFrame: DataFrame with consecutive dialogues merged.
    """
    # Identify speaker change points
    group_id = (df[speaker_col] != df[speaker_col].shift()).cumsum()

    # Group by speaker blocks and join their text
    grouped = df.groupby(group_id).agg({
        speaker_col: 'first',
        text_col: lambda x: ' '.join(str(s) for s in x if pd.notna(s))
    }).reset_index(drop=True)

    return grouped

def keep_segments_with_only_allowed_characters(segments, allowed_characters, speaker_col='raw_character_text'):
    """
    Keep only segments that contain exclusively the allowed characters.
    
    Args:
        segments (list): List of DataFrames (dialogue segments).
        allowed_characters (list): Characters to retain.
        speaker_col (str): Column name for character names.

    Returns:
        list: Filtered list of DataFrames.
    """
    filtered = []
    for seg in segments:
        unique_chars = set(seg[speaker_col].dropna().unique())
        if unique_chars.issubset(set(allowed_characters)):
            filtered.append(seg.reset_index(drop=True))
    return filtered

def generate_response_pairs(conversations, responder_name, speaker_col='raw_character_text', text_col='spoken_words'):
    """
    Generate dialogue pairs where the specified responder replies directly after another character,
    for a list of DataFrames (conversations).

    Args:
        conversations (list of pd.DataFrame): List of DataFrames with speaker and dialogue columns.
        responder_name (str): Name of the character who responds.
        speaker_col (str): Column containing character names.
        text_col (str): Column containing spoken text.

    Returns:
        list of dict: Each dict contains character_1, words_1, character_2 (responder), words_2.
    """
    pairs = []
    for df in conversations:
        for i in range(len(df) - 1):
            current_speaker = df.loc[i, speaker_col]
            current_text = df.loc[i, text_col]
            next_speaker = df.loc[i + 1, speaker_col]
            next_text = df.loc[i + 1, text_col]

            if next_speaker == responder_name and current_speaker != responder_name:
                pairs.append({
                    "character_1": current_speaker,
                    "words_1": current_text,
                    "character_2": responder_name,
                    "words_2": next_text
                })

    return pairs


def group_by_character_1(pairs):
    """
    Group dialogue pairs by character_1.
    """
    grouped = defaultdict(list)
    for pair in pairs:
        character = pair.get('character_1')
        if character:
            grouped[character].append(pair)
    return dict(grouped)

def sanitize_filename(name):
    """
    Remove or replace invalid filename characters.
    """
    return re.sub(r'[^a-zA-Z0-9_\- ]', '', name).replace(' ', '_')

def save_dialogues_as_json(grouped_dialogues, output_dir='output_dialogues'):
    """
    Save each character_1 group as a separate JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    for character, dialogues in grouped_dialogues.items():
        filename = sanitize_filename(character) + ".json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dialogues, f, ensure_ascii=False, indent=4)
        print(f"Saved: {filepath}")

# --- Main execution ---
df = pd.read_csv('simpsons_dataset.csv')

# Define allowed characters
allowed_characters = ["Homer Simpson", "Marge Simpson", "Bart Simpson", "Lisa Simpson", "Maggie Simpson"]

# Extract conversations
conversations = get_conversations(df)

# Remove segments that include characters outside the allowed list
#clean_conversations = keep_segments_with_only_allowed_characters(conversations, allowed_characters)

# Remove empty lines and NaN values
clean_conversations = [seg.dropna(subset=['raw_character_text', 'spoken_words']).reset_index(drop=True) for seg in conversations]         

# Merge consecutive lines by the same character
clean_conversations = [concat_consecutive_speakers(seg) for seg in clean_conversations]

# Filter out segments with less than 2 dialogues
clean_conversations = [seg for seg in clean_conversations if len(seg) > 1]  

# filter segments with Homer Simpson is part of the conversation
clean_conversations = [seg for seg in clean_conversations if "Homer Simpson" in seg['raw_character_text'].values]

character_conversations = generate_response_pairs(clean_conversations, responder_name="Homer Simpson")

# Group dialogues by character_1
grouped = group_by_character_1(character_conversations)
#save_dialogues_as_json(grouped)

# Select a specific character

selected_character = "Bart Simpson"
if selected_character in grouped:
    data = grouped["Bart Simpson"]

    total_pairs = []
    for data_item in data:
        total_pairs.append(
                {
                    "conversations": [
                        {"role": "user", "content":  data_item['words_1'].strip()},
                        {"role": "assistant", "content": data_item['words_2'].strip()},
                    ]
                }
            )

    total_pairs_dataset = Dataset.from_list(total_pairs)

    print(f"Total pairs: {len(total_pairs)}")
    save_path = f"{selected_character} conversations.json"
    with open   (save_path, 'w', encoding='utf-8') as f:
        json.dump(total_pairs, f, ensure_ascii=False, indent=4)

    print("Pushing to hub...")
    total_pairs_dataset.push_to_hub("OscarIsmael47/Bart_Simpson_and_Homer_Simpson_conversations",
                                    token=os.getenv("HUGGINGFACE_TOKEN"))
    print("Done!")
