import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\n?#]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url if len(url) == 11 else None

def download_transcript(video_url, episode_name):
    """Download transcript using the correct API instance methods"""
    
    # Create transcripts folder if it doesn't exist
    if not os.path.exists("transcripts"):
        os.makedirs("transcripts")
    
    try:
        # Extract video ID
        video_id = extract_video_id(video_url)
        if not video_id:
            print(f"Invalid YouTube URL: {video_url}")
            return False
        
        print(f" Downloading transcript for: {episode_name}")
        print(f"   Video ID: {video_id}")
        
        # Create API instance
        api = YouTubeTranscriptApi()
        
        # Try to list available transcripts first
        try:
            transcript_list = api.list(video_id)
            languages = []
            for transcript_obj in transcript_list:
                languages.append(transcript_obj.language_code)
            print(f"   Available transcripts: {languages}")
        except Exception as e:
            print(f"   Could not list transcripts: {e}")
        
        # Try to fetch transcript
        transcript = None
        
        # Method 1: Try to fetch with English preference
        try:
            transcript = api.fetch(video_id, ['en'])
            print("   ✅ Found English transcript")
        except:
            # Method 2: Try to fetch any available transcript
            try:
                transcript = api.fetch(video_id)
                print("   ✅ Found default transcript")
            except Exception as e:
                raise Exception(f"Could not fetch transcript: {str(e)}")
        
        # Convert to text using TextFormatter
        formatter = TextFormatter()
        text = formatter.format_transcript(transcript)
        
        # Clean up formatting
        cleaned_text = text.replace('\n\n', '\n').strip()
        
        # Save to file
        filename = f"playdate{episode_name}.txt"
        filepath = os.path.join("transcripts", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        
        print(f"✅ Saved: {filepath}")
        print(f"   Length: {len(cleaned_text)} characters")
        return True
        
    except Exception as e:
        print(f"Failed to download {episode_name}: {str(e)}")
        print("   Possible reasons:")
        print("   - Video has no captions/transcript")
        print("   - Video is private or age-restricted")
        print("   - API access blocked")
        return False

def test_video(video_id):
    """Test if a video has transcripts available"""
    try:
        api = YouTubeTranscriptApi()
        
        print(f"Testing video ID: {video_id}")
        
        # List available transcripts
        transcript_list = api.list(video_id)
        languages = []
        for transcript_obj in transcript_list:
            languages.append(transcript_obj.language_code)
        
        print(f"Available transcripts: {languages}")
        
        # Try to fetch the first few lines
        transcript = api.fetch(video_id)
        if transcript and len(transcript) > 0:
            sample_text = transcript[0].get('text', 'No text available')[:100]
            print(f"   Sample text: {sample_text}...")
            return True
        else:
            print("Transcript is empty")
            return False
            
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def main():
    print("Will & Rusty's Playdate Transcript Downloader")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Download single episode")
        print("2. Download multiple episodes")
        print("3. Test a video")
        print("4. Exit")
        
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == "1":
            # Single episode
            url = input("\nEnter YouTube URL: ").strip()
            episode_num = input("Enter episode number (e.g., 137): ").strip()
            
            if url and episode_num:
                download_transcript(url, episode_num)
            else:
                print("Please provide both URL and episode number")
        
        elif choice == "2":
            # Multiple episodes
            print("\nEnter episodes (one per line)")
            print("Format: EPISODE_NUMBER,YOUTUBE_URL")
            print("Example: 137,https://www.youtube.com/watch?v=kfWJhDolNPY")
            print("Type 'done' when finished:")
            
            episodes = []
            while True:
                line = input().strip()
                if line.lower() == 'done':
                    break
                
                if ',' in line:
                    parts = line.split(',', 1)
                    episode_num = parts[0].strip()
                    url = parts[1].strip()
                    episodes.append((url, episode_num))
                else:
                    print("Invalid format. Use: EPISODE_NUMBER,URL")
            
            if episodes:
                print(f"\nDownloading {len(episodes)} episodes...")
                successful = 0
                for url, episode_num in episodes:
                    if download_transcript(url, episode_num):
                        successful += 1
                    print()  # Add spacing between downloads
                
                print(f"Complete! {successful}/{len(episodes)} episodes downloaded")
        
        elif choice == "3":
            # Test mode
            url_or_id = input("\nEnter YouTube URL or video ID: ").strip()
            video_id = extract_video_id(url_or_id) or url_or_id
            test_video(video_id)
        
        elif choice == "4":
            print("Done!")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()