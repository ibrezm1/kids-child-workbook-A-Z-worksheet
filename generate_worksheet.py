from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Dotted Font
try:
    pdfmetrics.registerFont(TTFont('KGPrimaryDots', 'KGPrimaryDots.ttf'))
    DOTTED_FONT_NAME = 'KGPrimaryDots'
except Exception as e:
    print(f"Warning: Could not load KGPrimaryDots font: {e}. Falling back to outline.")
    DOTTED_FONT_NAME = 'Helvetica-Bold'

# Register Solid Font (for single-story 'a' etc.)
try:
    pdfmetrics.registerFont(TTFont('Andika', 'Andika-Regular.ttf'))
    SOLID_FONT_NAME = 'Andika'
except Exception as e:
    print(f"Warning: Could not load Andika font: {e}. Falling back to Helvetica.")
    SOLID_FONT_NAME = 'Helvetica-Bold'

def draw_tracing_lines(c, y_start, width, line_height=0.5*inch):
    """Draws a set of 3 lines for writing: top, middle (dashed), bottom. Also adds vertical separators."""
    # Top line
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(0.5*inch, y_start + line_height, 0.5*inch + width, y_start + line_height)
    
    # Middle line (dashed)
    c.setStrokeColor(colors.lightgrey)
    c.setDash(4, 4)
    c.line(0.5*inch, y_start + line_height/2, 0.5*inch + width, y_start + line_height/2)
    c.setDash([]) # reset dash
    
    # Bottom line
    c.setStrokeColor(colors.black)
    c.line(0.5*inch, y_start, 0.5*inch + width, y_start)
    
    # Vertical lines (to create boxes)
    c.setStrokeColor(colors.lightgrey)
    c.setLineWidth(0.5)
    
    x_start = 0.5 * inch
    num_sections = int(width / inch)
    
    for i in range(num_sections + 1):
        x = x_start + (i * inch)
        c.line(x, y_start, x, y_start + line_height)
        
    c.setStrokeColor(colors.black) # Reset to black

def draw_text(c, text, x, y, font_size=50, is_dotted=False, font_name="Helvetica-Bold"):
    """Draws text. Uses dotted font if is_dotted is True and font matches DOTTED_FONT_NAME, otherwise outlines."""
    t = c.beginText()
    t.setTextOrigin(x, y)
    
    # Check if this is our special dotted font 
    # (Assuming DOTTED_FONT_NAME is global for now, or just check string)
    if 'Dots' in font_name and is_dotted:
        # Use the specialized dotted font directly
        t.setFont(font_name, font_size)
        t.setFillColor(colors.black) # It's a "solid" font made of dots, so just fill it
        t.textOut(text)
        c.drawText(t)
    elif is_dotted:
        # Fallback: Instead of an outline boundary, use a solid light gray color for tracing
        t.setFont(font_name, font_size)
        t.setTextRenderMode(0) # Fill text
        t.setFillColor(colors.lightgrey)
        t.textOut(text)
        c.drawText(t)
    else:
        # Standard solid text
        t.setFont(font_name, font_size)
        t.setTextRenderMode(0) # Fill text
        t.setFillColor(colors.black)
        t.textOut(text)
        c.drawText(t)

import string

def create_page(c, letter_char):
    width, height = letter
    margin = 0.5 * inch
    content_width = width - 2 * margin
    
    # Title - Big Letter (Single)
    target_char = letter_char.upper() if letter_char.isalpha() else letter_char
    
    c.setFont(SOLID_FONT_NAME, 60)
    c.drawString(margin, height - 1.0*inch, target_char)
    
    # Instruction
    c.setFont("Helvetica", 14)
    c.drawString(width - 3*inch, height - 0.7*inch, "Trace and Write")

    # Start drawing lines
    start_y = height - 2.0 * inch
    line_spacing = 0.85 * inch
    line_height = 0.6 * inch
    
    rows = 10
    
    for i in range(rows):
        y_pos = start_y - (i * line_spacing)
        draw_tracing_lines(c, y_pos, content_width, line_height)
        
        # Text positioning
        text_y = y_pos + (line_height * 0.15)
        
        # Pattern for this letter
        if letter_char.isalpha():
            pattern_str = " ".join([target_char.upper()] * 4 + [letter_char.lower()] * 3)
        else:
            pattern_str = " ".join([target_char] * 7)
        
        if i < 2:
            x_pos = margin + 0.5 * inch
            # We iterate over the characters in the pattern string
            for char in pattern_str.replace(" ", ""):
                if i == 0:
                     # Row 0: All Solid check
                     draw_text(c, char, x_pos, text_y, font_size=55, is_dotted=False, font_name=SOLID_FONT_NAME)
                else:
                     # Row 1: All Dotted
                     draw_text(c, char, x_pos, text_y, font_size=55, is_dotted=True, font_name=DOTTED_FONT_NAME)
                
                x_pos += 1 * inch

        elif i < 4:
            # More dotted practice
             x_pos = margin + 0.5 * inch
             for char in pattern_str.replace(" ", ""):
                draw_text(c, char, x_pos, text_y, font_size=55, is_dotted=True, font_name=DOTTED_FONT_NAME)
                x_pos += 1 * inch
        
        # Remaining rows empty
        
    # End of page content processing
    c.showPage() # Finalize this page and prepare for next

def create_workbook(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Loop through A-Z and 0-9
    characters = string.ascii_uppercase + string.digits
    for letter_char in characters:
        create_page(c, letter_char)
        print(f"Processed page for {letter_char}")
        
    c.save()
    print(f"Generated workbook: {filename}")

if __name__ == "__main__":
    create_workbook("alphabet_workbook.pdf")
