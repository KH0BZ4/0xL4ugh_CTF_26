import re

def main():
    with open('Sysmon.evtx', 'rb') as f:
        data = f.read()

    keywords = [
        "Grunt", "Beacon", "Stager", "Sliver", "Koadic", "PoshC2", "Merlin", "Deimos",
        "Apfell", "Empyre", "PowerShell Empire", "Empire", "Covenant", "Havoc", "Demon",
        "Meterpreter", "Metasploit", "Brute Ratel", "Badger", "Mythic", "Poseidon",
        "Apollo", "Satan", "Shadow", "Viper", "AsyncRAT", "Quasar", "NjRAT", "Cobalt"
    ]

    for kw in keywords:
        found = False
        # Search UTF-16LE
        pattern_utf16 = kw.encode('utf-16le')
        if re.search(re.escape(pattern_utf16), data, re.IGNORECASE):
            print(f"Found keyword (UTF-16LE): {kw}")
            found = True
        
        # Search ASCII/UTF-8
        pattern_ascii = kw.encode('utf-8')
        if re.search(re.escape(pattern_ascii), data, re.IGNORECASE):
            print(f"Found keyword (ASCII): {kw}")
            found = True
            
        if found:
            # Print context
            offsets = [m.start() for m in re.finditer(re.escape(pattern_ascii), data, re.IGNORECASE)]
            if not offsets:
                offsets = [m.start() for m in re.finditer(re.escape(pattern_utf16), data, re.IGNORECASE)]
            
            for offset in offsets[:3]: # first 3
                print(f"-- Context for {kw} at {offset} --")
                start = max(0, offset - 100)
                end = min(len(data), offset + 100)
                print(data[start:end])
                print("------")

if __name__ == "__main__":
    main()
