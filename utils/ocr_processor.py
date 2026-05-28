import requests
import re
import os

OCR_SPACE_API_KEY = 'helloworld' # Note: 'helloworld' is a valid free tier test key, tapi ada limit harian

def extract_total_from_receipt(image_path):
    if not os.path.exists(image_path):
        return None, 0.0

    try:
        # Panggil API OCR.space
        with open(image_path, 'rb') as f:
            payload = {
                'isOverlayRequired': False,
                'apikey': OCR_SPACE_API_KEY,
                'language': 'eng', 
            }
            files = {
                'file': f
            }
            # Kirim gambar ke server OCR
            response = requests.post('https://api.ocr.space/parse/image', files=files, data=payload, timeout=20)
            response.raise_for_status()
            result = response.json()
            
            if result.get('IsErroredOnProcessing'):
                return None, 0.0
                
            parsed_results = result.get('ParsedResults')
            if not parsed_results:
                return None, 0.0
                
            text = parsed_results[0].get('ParsedText', '')
            
            # Pola Regex untuk mendeteksi kata kunci seperti 'TOTAL', 'JUMLAH', atau 'GRAND TOTAL'
            lines = text.split('\n')
            keyword_pattern = re.compile(r'(?i)(total|jumlah|grand\s*total)')
            amount_pattern = re.compile(r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)')
            
            total_amount = None
            confidence = 1.0 # API OCR.space versi gratis tidak memberikan confidence per kata
            
            found_keyword = False
            for line in lines:
                if keyword_pattern.search(line):
                    found_keyword = True
                    # Cek apakah nominal ada di baris yang sama
                    amounts = amount_pattern.findall(line)
                    if amounts:
                        clean_amount = amounts[-1].replace('.', '').replace(',', '')
                        try:
                            total_amount = float(clean_amount)
                            break
                        except ValueError:
                            pass
                
                # Jika keyword sudah ditemukan di baris sebelumnya, cari di baris ini
                elif found_keyword:
                    amounts = amount_pattern.findall(line)
                    if amounts:
                        clean_amount = amounts[-1].replace('.', '').replace(',', '')
                        try:
                            total_amount = float(clean_amount)
                            break
                        except ValueError:
                            pass

            if total_amount is not None:
                return total_amount, confidence
            
            return None, 0.0
            
    except Exception as e:
        print(f"OCR Error: {e}")
        return None, 0.0
