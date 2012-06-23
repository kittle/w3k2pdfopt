import os
import pexpect

"""
 a. Autostraighten (-as)             l. Landscape mode (-ls)
 b. Bitmap encoding (-jpg,-png,-bpc) m. Margin to ignore (-m)
 c. Color output (-c)               mc. Mark corners (-mc)
cg. Column gap threshold (-cg)       o. Output device dpi (-odpi)
ch. Column height threshold (-ch)   om. Output margins (-om)
co. Columns max allowed (-col)       p. Page range (-p)
cm. Contrast max (-cmax)            pd. Padding on output (-pl,...)
 d. Display resolution (-h,-w)       s. Sharpening (-s)
 f. Fit to single column (-fc)       u. Usage (command line opts)
 g. Gamma value (-g)                 w. Wrap text option (-wrap)
gs. Ghostscript interpreter (-gs)   ws. Word spacing threshold (-ws)
 i. Input file dpi (-idpi)          wt. White threshold (-wt)
 j. Justification (-j)              
"""

"""
k2pdfopt v1.22 http://willus.com, (compiled 15:23:03, Sep 10 2011)

usage:  k2pdfopt [opts] <input pdf | folder>

(Or just drag a PDF file to this icon.)

Attempts to optimize PDF files (especially two-column ones) for display on
the Kindle-2 (or other mobile readers/smartphones) by looking for rectangular
regions in the file and re-paginating them without margins and excess white
space.  Works on any PDF file, but assumes it has a mostly-white background.
Native PDF files (not scanned) work best.

If given a folder, k2pdfopt first looks for bitmaps in the folder and if
any are found, converts those bitmaps to a PDF as if they were pages of a
PDF file.  If there are no bitmaps in the folder and if PDF files are in
the folder, then each PDF file will be converted in sequence.

You can override the defulat amount of margin to ignore by setting the
K2PDFOPT_MARGINS environment variable to the number of inches to ignore.
The default is 0.25 inches to avoid any edge artifacts from scanned pages.
You can set specific variables: K2PDFOPT_LEFTMARGIN, K2PDFOPT_RIGHTMARGIN,
K2PDFOPT_BOTTOMMARGIN, K2PDFOPT_TOPMARGIN.

Command Line Options
--------------------
-a[-]             Turn on [off] text coloring.  Default is on.  Also can
                  use the K2PDFOPT_NO_TEXT_COLORING env var.
-as [<maxdeg>]    Attempt to automatically straighten tilted source pages.
                  Will rotate up to +/-<maxdegrees> degrees if a value is
                  specified, otherwise defaults to 4 degrees max.  Use -1 to
                  turn off. Default is off (-as -1).
-bpc <nn>         Set the bits per color plane on the output device to <nn>.
                  The value of <nn> can be 1, 2, 4, or 8.  The default is 4
                  to match the kindle's display capability.
-c[-]             Output in color [grayscale].  Default is grayscale.
-col <maxcol>     Set max number of columns.  <maxcol> can be 1, 2, or 4.
                  Default is -col 4.  -col 1 disables column searching.
-cg <inches>      Minimum column gap width in inches for detecting multiple
                  columns.  Default = 0.125 inches.  Setting this too large
                  will give very poor results for multicolumn files.
-ch <inches>      Minimum column height in inches for detecting multiple
                  columns.  Default = 1.5 inches.
-cmax <max>       Set max contrast increase on source pages.  1.0 keeps
                  contrast from being adjusted.  Def = 2.0.

-d[-]             Turn on [off] dithering for bpc values < 8.  See -bpc.
                  Default is on.
-fc[-]            For multiple column documents, fit [don't fit] columns to
                  the width of the reader screen regardless of -odpi.
                  Default is to fit the columns to the reader.
-g <gamma>        Set gamma value of output bitmaps. A value less than 1.0
                  makes the page darker and may make the font more readable.
                  Default is 0.5.
-h <height>       Set height of output in pixels (def=735).  See -hq.
-hq               Higher quality (convert PDF to higher res bitmaps).
                  Equivalent to -idpi 400 -odpi 333 -w 1120 -h 1470.
-gs               Force use of Ghostscript instead of mupdf to read PDFs.
-idpi <dpi>       Set pixels per inch for input file (def=300). See -hq.
-j [0|1|2]        Set output text justification.  0 = left, 1 = center,
                  2 = right.  Default = centered.
-jpg [<quality>]  Use JPEG compression in PDF file with quality level
                  <quality> (def=90).  A lower quality value will make your
                  file smaller.  See also -png.
-ls[-]            Set output to be in landscape [portrait] mode.  The
                  default is portrait.

-m <inches>       Ignore <inches> inches around the margins of the source
                  file.  Default = 0.25 inches.
-mb <inches>      Same as -m, but for bottom margin only.  Overrides -m.
-ml <inches>      Same as -m, but for left margin only.  Overrides -m.
-mr <inches>      Same as -m, but for right margin only.  Overrides -m.
-mt <inches>      Same as -m, but for top margin only.  Overrides -m.
-mc[-]            Mark [don't mark] corners of the output bitmaps with a
                  small dot to prevent the reading device from re-scaling.
                  Default = mark.
-om <inches>      Set all margins on output device in inches.  Def = 0.02.
-omb <inches>     Set bottom margin on output device.  Overrides -om.
-oml <inches>     Set left margin on output device.  Overrides -om.
-omr <inches>     Set right margin on output device.  Overrides -om.
-omt <inches>     Set top margin on output device.  Overrides -om.
-odpi <dpi>       Set pixels per inch of output screen (def=167). See also
                  -fc and -hq.
-p <pagelist>     Specify pages to convert.  <pagelist> must not have any
                  spaces.  E.g. -p 1-3,5,9,10- would do pages 1 through 3,
                  page 5, page 9, and pages 10 through the end.

-pb <nn>          Pad bottom side of destination bitmap with <nn> rows.
                  Def = 4.
-pl <nn>          Pad left side of destination bitmap with <nn> columns.
                  Def = 0.
-pr <nn>          Pad right side of destination bitmap with <nn> columns.
                  Def = 3.
-pt <nn>          Pad top side of destination bitmap with <nn> rows.
                  Def = 0.
-png              (Default) Use PNG compression in PDF file.  See also -jpeg.
-s[-]             Sharpen [don't sharpen] images.  Default is to sharpen.
-ui[-]            User input query turned on [off].  Default = on for linux or
                  if not run from command line in Windows.
-v                Verbose output.
-w <width>        Set width of output in pixels (def=560). See -hq.
-wrap[-]          Enable [disable] text wrapping.  Default = enabled.
                  See also -ws.
-ws <spacing>     Set minimum word spacing for line breaking.  Use a
                  larger value to make it harder break lines.  Def = 0.25.
                  See also -wrap.

-wt <whitethresh> Any pixels whiter than <whitethresh> (0-255) are made pure
                  white.  Setting this lower can help k2pdfopt better process
                  some poorly-quality scanned pages.  Def = 255 (not used).
"""
 
def arg_by_form(form):
    arg = []
    assert form.maxcol.data in (1,2,4), form.maxcol
    arg.append("-col %s" % form.maxcol.data)
    if form.landscape.data:
        arg.append("-ls")
    if form.height.data:
        arg.append("-h %s" % form.height.data)
    if form.width.data:
        arg.append("-w %s" % form.width.data)
    if form.m.data != 0.25:
        arg.append("-m %s" % form.m.data)
    if form.mb.data:
        arg.append("-mb %s" % form.mb.data)
    if form.ml.data:
        arg.append("-ml %s" % form.ml.data)
    if form.mr.data:
        arg.append("-mr %s" % form.mr.data)
    if form.mt.data:
        arg.append("-mt %s" % form.mt.data)
    if form.color.data:
        arg.append("-c")
    assert form.bpc.data in (1, 2, 4, 8)
    if form.bpc.data != 4 :
        arg.append("-bpc %s" % form.bpc.data)
    if form.astraighten.data:
        arg.append("-as")
    if form.text_justification.data and int(form.text_justification.data) != 1:
        arg.append("-j %s" % int(form.text_justification.data))
    if form.idpi.data and form.idpi.data != 300:
        arg.append("-idpi %s" % form.idpi.data)
    if form.odpi.data and form.odpi.data != 167:
        arg.append("-odpi %s" % form.odpi.data)
    
    return " ".join(arg)


def convert_pdf(filepath, filename, arg = "-col 2"):
    assert filename.lower().endswith(".pdf")
    p1, p2 = filename.rsplit(".", 1)
    suffix = arg.replace("-","").replace(" ", "_") # "w3k2pdfopt"
    new_filename = ".".join((p1, suffix, p2))
    new_filepath = filepath.rsplit(".", 1)[0] + "_k2opt.pdf"
    #
    cmd = "/usr/local/bin/k2pdfopt %s %s" % (arg, filepath)
    print cmd
    child = pexpect.spawn(cmd)
    child.expect("Press <ENTER> to exit", timeout=300)
    child.sendline("\n")
    child.close()
    os.remove(filepath)
    return new_filename, new_filepath


def test():
    filepath = "/tmp/xyz.pdf"
    filename = "The Realization of Shri Hevajra - Unknown.pdf"
    new_filepath, new_filename = convert_pdf(filepath, filename)
    print new_filepath, new_filename
    assert new_filename == "/tmp/xyz_k2opt.pdf"


if __name__ == "__main__":
    test()
    
