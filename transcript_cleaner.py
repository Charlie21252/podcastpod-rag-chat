import os
import re

def clean_existing_transcripts():
    """Clean up existing transcript files to remove >> markers and improve formatting"""
    
    transcript_folder = "transcripts"
    if not os.path.exists(transcript_folder):
        print(" No transcripts folder found")
        return
    
    files_cleaned = 0
    
    for filename in os.listdir(transcript_folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(transcript_folder, filename)
            
            try:
                # Read the file
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"   Cleaning {filename}...")
                print(f"   Original length: {len(content)} characters")
                
                # Clean up the content
                cleaned = clean_transcript_text(content)
                
                # Save the cleaned version
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                
                print(f"   Cleaned length: {len(cleaned)} characters")
                print(f"   Reduction: {len(content) - len(cleaned)} characters")
                files_cleaned += 1
                
            except Exception as e:
                print(f"Error cleaning {filename}: {e}")
    
    print(f"\Cleaned {files_cleaned} transcript files")

def clean_transcript_text(text):
    """Clean transcript text by removing markers and improving formatting"""
    
    # Remove >> markers
    cleaned = text.replace('>>', '')
    
    # Remove multiple spaces
    cleaned = re.sub(r' +', ' ', cleaned)
    
    # Fix newlines - remove excessive newlines but keep paragraph breaks
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)  # Max 2 newlines
    cleaned = re.sub(r'\n ', '\n', cleaned)               # Remove spaces after newlines
    
    # Try to create better paragraphs by looking for sentence endings
    # Split into sentences and group them better
    sentences = re.split(r'([.!?]+)', cleaned)
    
    result_parts = []
    current_paragraph = ""
    sentence_count = 0
    
    for i in range(0, len(sentences), 2):
        if i + 1 < len(sentences):
            sentence = sentences[i].strip()
            punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""
            
            if sentence:
                current_paragraph += sentence + punctuation + " "
                sentence_count += 1
                
                # Start new paragraph every 3-5 sentences or at natural breaks
                if (sentence_count >= 4 or 
                    any(word in sentence.lower() for word in ['anyway', 'so', 'but', 'well', 'okay', 'alright']) and sentence_count >= 2):
                    result_parts.append(current_paragraph.strip())
                    current_paragraph = ""
                    sentence_count = 0
    
    # Add any remaining text
    if current_paragraph.strip():
        result_parts.append(current_paragraph.strip())
    
    # Join paragraphs with double newlines
    final_text = '\n\n'.join(result_parts)
    
    # Final cleanup
    final_text = re.sub(r'\n\s+', '\n', final_text)  # Remove indentation
    final_text = re.sub(r' +', ' ', final_text)      # Remove double spaces
    final_text = final_text.strip()
    
    return final_text

def preview_cleaning():
    """Preview what cleaning would do to a file"""
    
    transcript_folder = "transcripts"
    if not os.path.exists(transcript_folder):
        print("No transcripts folder found")
        return
    
    files = [f for f in os.listdir(transcript_folder) if f.endswith('.txt')]
    if not files:
        print("No transcript files found")
        return
    
    print("Available files:")
    for i, filename in enumerate(files, 1):
        print(f"  {i}. {filename}")
    
    try:
        choice = int(input("\nChoose a file to preview (number): ")) - 1
        if 0 <= choice < len(files):
            filename = files[choice]
            filepath = os.path.join(transcript_folder, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n--- ORIGINAL ({len(content)} chars) ---")
            print(content[:500] + "..." if len(content) > 500 else content)
            
            cleaned = clean_transcript_text(content)
            
            print(f"\n--- CLEANED ({len(cleaned)} chars) ---")
            print(cleaned[:500] + "..." if len(cleaned) > 500 else cleaned)
            
            if input("\nApply this cleaning to the file? (y/n): ").lower() == 'y':
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                print(f"Updated {filename}")
        else:
            print("Invalid choice")
    except ValueError:
        print("Please enter a number")

def main():
    print("Transcript Cleaner")
    print("=" * 25)
    print("1. Clean all transcript files")
    print("2. Preview cleaning on one file")
    print("3. Exit")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        clean_existing_transcripts()
    elif choice == "2":
        preview_cleaning()
    elif choice == "3":
        print("Done!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()