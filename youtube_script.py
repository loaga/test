import argparse
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

if __name__ == '__main__':
    print("--- YouTube Transcript and Video Downloader ---")
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest='url',
                        help='YouTube url')
    parser.add_argument('-l', '--lan', dest='lan',
                        help='language')
    # parser.add_argument('-d', '--dbg', dest='dbg', action='store_true', help='debug mode') # REMOVED
    parser.add_argument('-v', '--video', dest='video', action='store_true',
                        help='Download the video file') # Corrected help message

    opt = parser.parse_args()
    # dbg = opt.dbg # REMOVED
    url = opt.url
    lan = opt.lan
    video = opt.video

    #t=5576s - jump to matched word starting time
    #url=https://www.youtube.com/watch?v=EVQSjDE70b8&t=5576s"

    # tmp = '/tmp/' # REMOVED
    yt = None # Initialize yt

    try:
        # === MODIFICATION START ===
        # Get the video ID using pytube
        if not url: # url comes from opt.url
            print("Error: YouTube URL is required. Use -u or --url.")
            exit(1)
        try:
            yt = YouTube(url)
            id = yt.video_id
        except Exception as e:
            print(f"Error processing YouTube URL '{url}': {str(e)}. Please ensure it's a valid YouTube video URL.")
            exit(1)

        print(f"Successfully extracted Video ID: {id}.")

        # === MODIFICATION START for output file handling ===
        # Define transcript filepath in current directory
        transcript_filename = f"{id}_transcript.txt"
        # No need for 'out' variable anymore. 'out1' is now 'transcript_filename'
        # === MODIFICATION END ===

        # Get the video transcript (original logic using the new 'id')
        cc = None # Initialize cc
        try:
            if lan is None or len(lan) == 0:
               print("No language specified. Attempting to fetch available transcript...")
               # Fetch available transcripts and take the first one.
               transcript_list = YouTubeTranscriptApi.list_transcripts(id)
               # The line above populates transcript_list. No need to call it again here.
               chosen_transcript = None
               # Prefer manual transcripts
               for tr in transcript_list:
                   if not tr.is_generated:
                       chosen_transcript = tr
                       break

               # If no manual transcript found, try to find any generated one
               if not chosen_transcript:
                   for tr in transcript_list:
                       if tr.is_generated:
                           chosen_transcript = tr
                           break

               if chosen_transcript:
                   print(f"Found transcript: Language - {chosen_transcript.language_code}, Generated - {chosen_transcript.is_generated}.")
                   cc = chosen_transcript.fetch()
               else:
                   # This will likely be caught by NoTranscriptFound if list_transcripts itself raises it,
                   # or if the list is empty.
                   print(f"No suitable transcript found for video ID: {id}.") # Already good.

            else: # Language specified
                print(f"Attempting to fetch transcript in language: {lan}.") # Removed \n, added period.
                cc = YouTubeTranscriptApi.get_transcript(id, languages=[lan])

            if cc:
               # === MODIFICATION START for transcript writing ===
               # Remove the block that wrote to 'out' (done by not including it here)
               #
               # Write only the plain text transcript
               sub = "\n".join([entry["text"] for entry in cc])
               with open (transcript_filename, 'w') as outf1: # Use the new filename
                   outf1.write(sub)
               print(f"Transcript successfully saved to: ./{transcript_filename}.") # Added colon and period.
               # === MODIFICATION END ===
            # else case for cc: Handled by the print statement in transcript fetching logic or exceptions.

        except TranscriptsDisabled:
            print(f"Transcripts are disabled for video ID: {id}.") # Added period.
        except NoTranscriptFound:
            if lan:
                print(f"No transcript found for language '{lan}' for video ID: {id}. Try fetching without specifying a language to see available transcripts.") # Added period.
            else:
                print(f"No transcripts found for video ID: {id}.") # Already good.
        except Exception as e: # General catch for other youtube_transcript_api errors or issues
            print(f"An error occurred during transcript fetching: {str(e)}.") # Added period.

    # This outer except block was for the whole process including ID extraction.
    # ID extraction has its own exit(1) for critical errors.
    # This block will now catch other unexpected errors post-ID extraction but outside transcript/video download.
    except Exception as e:
        print(f"An unexpected overall error occurred: {str(e)}.") # Added period.


    # Video download section
    if video:
        if not yt:
            # This case should ideally not be reached if URL processing was successful.
            # If yt is None here, it means the ID extraction failed and exited,
            # or there's a logic flaw. The earlier exit in case of bad URL should prevent this.
            print("Error: YouTube object not available for download. URL might have been invalid.") # Added period.
            # exit(1) # Consider exiting if yt is None
        else:
            try:
                print(f"Attempting to download video: {yt.title}...") # Already good.
                video_stream = yt.streams.get_highest_resolution()

                # === MODIFICATION START ===
                print(f"Selected video stream for download: {video_stream}.") # More descriptive, added period.
                downloaded_filepath = video_stream.download()
                # By default, downloads to current working directory.
                # We can allow specifying a path later if needed.
                print(f"Video successfully downloaded to: {downloaded_filepath}.") # Added period.
                # === MODIFICATION END ===

            except Exception as e:
                print(f"An error occurred during video download: {str(e)}.") # Added period.
                # Consider more specific exceptions if pytube raises them for downloads
