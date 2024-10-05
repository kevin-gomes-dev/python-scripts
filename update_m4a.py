# Takes in an .m4a file and outputs a new file with a "u" prefix.
# The new file's metadata is updated such that "title" tag is changed to the original filename.
# We encode with utf-8 to ensure any symbols or different languages remain intact.
# TODO: Allow other extensions besides .m4a. Create list of extensions, check against list and rename files as such.
import sys
import pydub
import os
import pydub.utils
import time

def update_m4a(input_file):
    # Full file path
    old_file_full = os.path.realpath(os.path.normpath(input_file)).encode('utf-8')
    
    # Full file dir
    old_file_dir = os.path.dirname(old_file_full)

    # Tuple for filename and ext
    old_file = os.path.splitext(os.path.basename(old_file_full))
    
    # Check if m4a
    if old_file[1].decode('utf-8') != ".m4a":
        print("File was not an m4a file:",old_file_full.decode('utf-8'))
        return
    
    # Open the audio file using AudioSegment
    audio = pydub.AudioSegment.from_file(old_file_full,"m4a")
    metadata = pydub.utils.mediainfo(old_file_full)
    
    # Extract the old filename
    new_title = old_file[0].decode('utf-8')
    
    # New filename
    output_filename = new_title + old_file[1].decode('utf-8')
    
    # Full new file
    output_file = os.path.join(old_file_dir.decode('utf-8'),output_filename)

    # Update metadata to have "title" in TAG dict replaced with new title.
    metadata["TAG"].update({"title": new_title})

    # Get bitrate for exporting
    bitrate = metadata["bit_rate"]
    print(output_file + " is ready to be exported. Now exporting...")

    # Export new file with all old metadata and bitrate, keeping the new title field
    audio.export(output_file, format="ipod", tags=metadata["TAG"],bitrate=bitrate)
    
    
# Takes in a path. For each .m4a file in this path and subfolders, update the title tag to the filename.
# NOTE this changes bitrates due to re-exporting.

def update_all_m4a(directory):
    directory = os.path.realpath(os.path.normpath(directory))
    # i is current folder, j is list of sub folders, k is list of files.
    num_gen = 0
    start = time.perf_counter()
    for i,j,k in os.walk(directory):
        # Are there files?
        if k:
            for file in k:
                file = os.path.join(i,file)
                file_start = time.perf_counter()
                # Try to export. If we can't, something happened.
                try:
                    update_m4a(file)
                    num_gen += 1
                except Exception:
                    print("Error: Failed to update or export " + file + ". Check it out.")
                    raise
                # Print time taken per file.
                file_time_taken = time.perf_counter() - file_start
                print("Time taken: "+ str(file_time_taken) + " seconds, "+str(file_time_taken/float(60.0)) + " minutes.")
    
    time_taken = time.perf_counter() - start
    print("\nDone! Total time taken: "+ str(time_taken) + " seconds, "+str(time_taken/float(60.0)) + " minutes.")
    print("Total exports: " + str(num_gen))
    
def main():
    args = sys.argv
    if len(args) != 2:
        print ("Incorrect number of args passed. Expected directory of m4a files.")
        return
    try:
        update_all_m4a((args[1]))
    except:
        print("exception")
        raise
main()
