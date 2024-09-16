import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab, ImageEnhance
import pytesseract
from googletrans import Translator, LANGUAGES
import pyautogui
import cv2
import numpy as np

# Make sure you have Tesseract installed and set the path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Masked programmer\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Update this path

class OnScreenTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("On-Screen Translator")
        
        self.screenshot_button = ttk.Button(root, text="Take Screenshot", command=self.take_screenshot)
        self.screenshot_button.pack(pady=10)
        
        # Mapping between Tesseract and Google Translate language codes
        self.lang_mapping = {
            'afr': 'af', 'amh': 'am', 'ara': 'ar', 'asm': 'as', 'aze': 'az', 'aze_cyrl': 'az', 'bel': 'be',
            'ben': 'bn', 'bod': 'bo', 'bos': 'bs', 'bre': 'br', 'bul': 'bg', 'cat': 'ca', 'ceb': 'ceb',
            'ces': 'cs', 'chi_sim': 'zh-cn', 'chi_tra': 'zh-tw', 'chr': 'chr', 'cym': 'cy', 'dan': 'da',
            'deu': 'de', 'dzo': 'dz', 'ell': 'el', 'eng': 'en', 'enm': 'en', 'epo': 'eo', 'est': 'et',
            'eus': 'eu', 'fas': 'fa', 'fin': 'fi', 'fra': 'fr', 'frk': 'fr', 'frm': 'fr', 'gle': 'ga',
            'glg': 'gl', 'grc': 'el', 'guj': 'gu', 'hat': 'ht', 'heb': 'he', 'hin': 'hi', 'hrv': 'hr',
            'hun': 'hu', 'iku': 'iu', 'ind': 'id', 'isl': 'is', 'ita': 'it', 'ita_old': 'it', 'jav': 'jw',
            'jpn': 'ja', 'kan': 'kn', 'kat': 'ka', 'kat_old': 'ka', 'kaz': 'kk', 'khm': 'km', 'kir': 'ky',
            'kor': 'ko', 'kur': 'ku', 'lao': 'lo', 'lat': 'la', 'lav': 'lv', 'lit': 'lt', 'mal': 'ml',
            'mar': 'mr', 'mkd': 'mk', 'mlt': 'mt', 'msa': 'ms', 'mya': 'my', 'nep': 'ne', 'nld': 'nl',
            'nor': 'no', 'ori': 'or', 'pan': 'pa', 'pol': 'pl', 'por': 'pt', 'pus': 'ps', 'ron': 'ro',
            'rus': 'ru', 'san': 'sa', 'sin': 'si', 'slk': 'sk', 'slv': 'sl', 'spa': 'es', 'spa_old': 'es',
            'sqi': 'sq', 'srp': 'sr', 'srp_latn': 'sr', 'swa': 'sw', 'swe': 'sv', 'syr': 'sy', 'tam': 'ta',
            'tel': 'te', 'tgk': 'tg', 'tgl': 'tl', 'tha': 'th', 'tir': 'ti', 'tur': 'tr', 'uig': 'ug',
            'ukr': 'uk', 'urd': 'ur', 'uzb': 'uz', 'uzb_cyrl': 'uz', 'vie': 'vi', 'yid': 'yi'
        }

        # Updated language list with all Tesseract-supported languages
        self.languages = [
            ('auto', 'Auto Detect'),
            ('afr', 'Afrikaans'), ('amh', 'Amharic'), ('ara', 'Arabic'), ('asm', 'Assamese'), ('aze', 'Azerbaijani'),
            ('aze_cyrl', 'Azerbaijani - Cyrillic'), ('bel', 'Belarusian'), ('ben', 'Bengali'), ('bod', 'Tibetan'),
            ('bos', 'Bosnian'), ('bre', 'Breton'), ('bul', 'Bulgarian'), ('cat', 'Catalan; Valencian'),
            ('ceb', 'Cebuano'), ('ces', 'Czech'), ('chi_sim', 'Chinese - Simplified'), ('chi_tra', 'Chinese - Traditional'),
            ('chr', 'Cherokee'), ('cym', 'Welsh'), ('dan', 'Danish'), ('deu', 'German'), ('dzo', 'Dzongkha'),
            ('ell', 'Greek, Modern (1453-)'), ('eng', 'English'), ('enm', 'English, Middle (1100-1500)'),
            ('epo', 'Esperanto'), ('est', 'Estonian'), ('eus', 'Basque'), ('fas', 'Persian'), ('fin', 'Finnish'),
            ('fra', 'French'), ('frk', 'German Fraktur'), ('frm', 'French, Middle (ca. 1400-1600)'),
            ('gle', 'Irish'), ('glg', 'Galician'), ('grc', 'Greek, Ancient (-1453)'), ('guj', 'Gujarati'),
            ('hat', 'Haitian; Haitian Creole'), ('heb', 'Hebrew'), ('hin', 'Hindi'), ('hrv', 'Croatian'),
            ('hun', 'Hungarian'), ('iku', 'Inuktitut'), ('ind', 'Indonesian'), ('isl', 'Icelandic'),
            ('ita', 'Italian'), ('ita_old', 'Italian - Old'), ('jav', 'Javanese'), ('jpn', 'Japanese'),
            ('kan', 'Kannada'), ('kat', 'Georgian'), ('kat_old', 'Georgian - Old'), ('kaz', 'Kazakh'),
            ('khm', 'Central Khmer'), ('kir', 'Kirghiz; Kyrgyz'), ('kor', 'Korean'), ('kur', 'Kurdish'),
            ('lao', 'Lao'), ('lat', 'Latin'), ('lav', 'Latvian'), ('lit', 'Lithuanian'), ('mal', 'Malayalam'),
            ('mar', 'Marathi'), ('mkd', 'Macedonian'), ('mlt', 'Maltese'), ('msa', 'Malay'), ('mya', 'Burmese'),
            ('nep', 'Nepali'), ('nld', 'Dutch; Flemish'), ('nor', 'Norwegian'), ('ori', 'Oriya'),
            ('pan', 'Panjabi; Punjabi'), ('pol', 'Polish'), ('por', 'Portuguese'), ('pus', 'Pushto; Pashto'),
            ('ron', 'Romanian; Moldavian; Moldovan'), ('rus', 'Russian'), ('san', 'Sanskrit'),
            ('sin', 'Sinhala; Sinhalese'), ('slk', 'Slovak'), ('slv', 'Slovenian'), ('spa', 'Spanish; Castilian'),
            ('spa_old', 'Spanish; Castilian - Old'), ('sqi', 'Albanian'), ('srp', 'Serbian'), ('srp_latn', 'Serbian - Latin'),
            ('swa', 'Swahili'), ('swe', 'Swedish'), ('syr', 'Syriac'), ('tam', 'Tamil'), ('tel', 'Telugu'),
            ('tgk', 'Tajik'), ('tgl', 'Tagalog'), ('tha', 'Thai'), ('tir', 'Tigrinya'), ('tur', 'Turkish'),
            ('uig', 'Uighur; Uyghur'), ('ukr', 'Ukrainian'), ('urd', 'Urdu'), ('uzb', 'Uzbek'),
            ('uzb_cyrl', 'Uzbek - Cyrillic'), ('vie', 'Vietnamese'), ('yid', 'Yiddish')
        ]
        
        self.from_lang_var = tk.StringVar()
        self.from_lang_var.set('Auto Detect')
        self.from_lang_label = ttk.Label(root, text="From Language:")
        self.from_lang_label.pack()
        self.from_lang_combo = ttk.Combobox(root, textvariable=self.from_lang_var, values=[lang[1] for lang in self.languages])
        self.from_lang_combo.pack()
        
        self.to_lang_var = tk.StringVar()
        self.to_lang_var.set('English')
        self.to_lang_label = ttk.Label(root, text="To Language:")
        self.to_lang_label.pack()
        self.to_lang_combo = ttk.Combobox(root, textvariable=self.to_lang_var, values=[lang[1] for lang in self.languages])
        self.to_lang_combo.pack()
        
        self.result_frame = ttk.Frame(root)
        self.result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.original_text = tk.Text(self.result_frame, height=5, width=50, wrap=tk.WORD)
        self.original_text.pack(pady=5, fill=tk.BOTH, expand=True)
        self.original_text.insert(tk.END, "Original text will appear here.")

        self.translated_text = tk.Text(self.result_frame, height=5, width=50, wrap=tk.WORD)
        self.translated_text.pack(pady=5, fill=tk.BOTH, expand=True)
        self.translated_text.insert(tk.END, "Translated text will appear here.")

        # Configure tags for text direction
        self.original_text.tag_configure("rtl", justify='right')
        self.original_text.tag_configure("ltr", justify='left')
        self.translated_text.tag_configure("rtl", justify='right')
        self.translated_text.tag_configure("ltr", justify='left')
        
        self.screenshot = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def take_screenshot(self):
        self.root.withdraw()
        self.screenshot = ImageGrab.grab()
        self.root.deiconify()
        self.show_selection_window()

    def show_selection_window(self):
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes('-fullscreen', True)
        self.selection_window.attributes('-alpha', 0.3)
        self.selection_window.configure(background='grey')

        self.canvas = tk.Canvas(self.selection_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        self.canvas.delete("selection")
        self.canvas.create_rectangle(self.start_x, self.start_y, cur_x, cur_y, outline="red", tags="selection")

    def on_release(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        self.selection_window.destroy()
        self.process_image()

    def preprocess_image(self, image):
        # Convert PIL Image to numpy array
        img_np = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Apply dilation
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        # Convert back to PIL Image
        return Image.fromarray(dilated)

    def process_image(self):
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
    
        cropped_image = self.screenshot.crop((x1, y1, x2, y2))
        preprocessed_image = self.preprocess_image(cropped_image)
        
        # Get the language code for OCR
        from_lang = next(lang[0] for lang in self.languages if lang[1] == self.from_lang_var.get())
        if from_lang == 'auto':
            from_lang = 'eng+ara'  # Default to English and Arabic for auto detection
        
        text = pytesseract.image_to_string(preprocessed_image, lang=from_lang)
        
        translator = Translator()
        to_lang = next(lang[0] for lang in self.languages if lang[1] == self.to_lang_var.get())
        
        # Convert Tesseract language codes to Google Translate language codes
        from_lang_google = self.lang_mapping.get(from_lang, 'auto')
        to_lang_google = self.lang_mapping.get(to_lang, 'en')
        
        translated = translator.translate(text, src=from_lang_google, dest=to_lang_google)
        
        self.original_text.delete('1.0', tk.END)
        self.translated_text.delete('1.0', tk.END)
    
        # Set text direction for original text
        if from_lang_google in ['ar', 'he', 'fa', 'ur']:
            self.original_text.insert(tk.END, text, "rtl")
        else:
            self.original_text.insert(tk.END, text, "ltr")
    
        # Set text direction for translated text
        if to_lang_google in ['ar', 'he', 'fa', 'ur']:
            self.translated_text.insert(tk.END, translated.text, "rtl")
        else:
            self.translated_text.insert(tk.END, translated.text, "ltr")
    
        # Ensure the text starts from the correct side
        self.original_text.see(tk.END if from_lang_google in ['ar', 'he', 'fa', 'ur'] else '1.0')
        self.translated_text.see(tk.END if to_lang_google in ['ar', 'he', 'fa', 'ur'] else '1.0')


if __name__ == "__main__":
    root = tk.Tk()
    app = OnScreenTranslator(root)
    root.mainloop()