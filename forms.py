
from flaskext.wtf import Form, TextField, Required, FileField, \
    BooleanField, IntegerField, DecimalField, SelectField, RadioField, \
    SubmitField


class PDFForm(Form):
    #name = TextField(name, validators=[Required()])
    pdf = FileField("source pdf file")
    # URLField
    landscape = BooleanField("landscape")
    maxcol = IntegerField("max number of columns", default=2)
    bpc = IntegerField("bit per color", default=4)
    dithering = BooleanField("dithering", default=True)
    #
    m = DecimalField("default margin", default=0.25)
    mb = DecimalField("bottom margin", default=0)
    ml = DecimalField("left margin", default=0)
    mr = DecimalField("right margin", default=0)
    mt = DecimalField("top margin", default=0)
    #
    color = BooleanField("color", default=False)
    height = IntegerField("height", default=735)
    width = IntegerField("width", default=560)
    astraighten = BooleanField("automatically straighten", default=False)
    text_justification = RadioField(u'Output Text Justification',
                                    default = "1",
                                    choices=[("0", 'Left'), ("1", 'Center'), ("2", 'Right')])    
    idpi = IntegerField("pixels per inch for input file", default=300)
    odpi = IntegerField("pixels per inch for output file", default=167)
    #submit = SubmitField("submit")
