import os
import argparse
from PIL import Image


def rgb2bin(tuple, bit_per_channel):
    binstr = ""
    print(tuple)
    if (bit_per_channel < 8):
        for i in tuple:
            scale = i >> (8 - bit_per_channel)
            form = "{0:0%dx}" % ((bit_per_channel + 3) // 4)
            binstr += form.format(scale)
    else:
        for i in tuple:
            form = "{0:0%dx}" % ((bit_per_channel + 3) // 4)
            binstr += form.format(i)
    return binstr


def main():
    parser = argparse.ArgumentParser(description="A tool to change picture to .coe file.")
    parser.add_argument('-w', '--width', type=int, default=8, help="Bit per channel, by default 8", )
    parser.add_argument('input_file', help="Input pic file name")
    parser.add_argument('-o', '--output', help="Output file name.")
    args = parser.parse_args()

    bit_per_channel = args.width
    input_filename = args.input_file
    output_filename = args.output

    if output_filename is None:
        output_filename = os.path.basename(input_filename).split('.')[0] + ".coe"

    print("> Running with depth %d, output file name '%s'" % (bit_per_channel, output_filename))

    im = Image.open(input_filename)
    pwidth, pheight = im.size
    print("> Reading pic. Width: %d, Height: %d" % (pwidth, pheight))

    
    coe_header = "memory_initialization_radix=16;\nmemory_initialization_vector=\n"

    outf = open(output_filename, 'w')
    outf.write(coe_header)

    count = 1
    for h in range(0, pheight):
        for w in range(0, pwidth):
            pixel = im.getpixel((w, h))
            if count == pwidth * pheight :
                line = "%s;" % (rgb2bin(pixel, bit_per_channel))
            else:
                line = "%s,\n" % (rgb2bin(pixel, bit_per_channel))
            print(line)
            outf.write(line)
            print(count)
            count += 1

    

    im.close()
    outf.close()

    print("> Done!")


if __name__ == "__main__":
    main()
