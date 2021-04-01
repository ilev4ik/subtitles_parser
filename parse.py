from collections import defaultdict
import json, re, sys

d = defaultdict(int)

def main():
    if len(sys.argv) > 3:
        print(sys.argv)
        return
        
    fname = sys.argv[1]
    unique = "-u" in sys.argv
    
    basefname = fname.split('.')[0]
    ifname = basefname + ".srt"
    if unique:
        basefname += "_u"
    ofname = basefname + "_parsed.txt"

    with open(ifname, "r", encoding='cp1251') as ifile:
        lines = ifile.readlines()
        
        # split up to blocks
        blocks = []
        currentBlock = []

        for line in lines:
            if line == '\n':
                blocks.extend(currentBlock[2:])
                currentBlock.clear()
                continue
            else:
                currentBlock.append(line)

        # split up words
        for scene in blocks:
            bareWords = scene.split()
            for word in bareWords:
                word.strip()
                word = re.sub("[\)\(+-«»\".,:?!<>\\\/i]", "", word).lower()
                if (len(word)):
                    d[word] += 1

        sd = sorted(d.items(), key=lambda x: x[1], reverse=True)
        if unique:
            sd = [w for w in sd if w[1] == 1]

        # print to file 
        with open(ofname, "w", encoding='cp1251') as ofile:
            ofile.write("Total words = " + str(len(d)) + "\n")
            if unique:
                ofile.write("Unique words = " + str(len(sd)) + "\n")
            ofile.write(json.dumps(sd))
            print("Written to: " + ofname)

if __name__ == "__main__":
    main()
    