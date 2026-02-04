import re

def main():
    with open('Sysmon.evtx', 'rb') as f:
        data = f.read()

    # Search for the filename bytes in UTF-16LE as Windows XML logs often use
    filename_utf16 = 'powershell'.encode('utf-16le')
    filename_ascii = b'powershell'

    print("Searching for UTF-16LE...")
    offsets = [m.start() for m in re.finditer(re.escape(filename_utf16), data)]
    
    encoding = 'utf-16le'
    if not offsets:
        print("Searching for ASCII...")
        offsets = [m.start() for m in re.finditer(re.escape(filename_ascii), data)]
        encoding = 'utf-8' # or ascii
    else:
        print(f"Found {len(offsets)} matches in UTF-16LE")

    for offset in offsets: # Look at all occurrences
        print(f'--- Offset {offset} ---')
        start = max(0, offset - 1000)
        end = min(len(data), offset + 1000)
        chunk = data[start:end]
        
        # Decode and handle errors
        try:
            text = chunk.decode(encoding, errors='ignore')
            # remove null bytes if any, just to clean up output
            text = text.replace('\x00', '') 
            print(text)
        except Exception as e:
            print(f"Error decoding: {e}")
        print('---')

if __name__ == '__main__':
    main()
