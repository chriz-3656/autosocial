import os
import requests
import zipfile
import io

def download_font(url, extract_to, target_font):
    print(f"Downloading {url}...")
    r = requests.get(url)
    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        for filename in z.namelist():
            if filename.endswith(".ttf") and target_font in filename:
                z.extract(filename, extract_to)
                print(f"Extracted {filename}")

if __name__ == "__main__":
    os.makedirs("fonts", exist_ok=True)
    # Inter
    download_font("https://github.com/rsms/inter/releases/download/v3.19/Inter-3.19.zip", "fonts", "Inter-Medium.ttf")
    download_font("https://github.com/rsms/inter/releases/download/v3.19/Inter-3.19.zip", "fonts", "Inter-Regular.ttf")
    # IBM Plex Mono
    download_font("https://github.com/IBM/plex/releases/download/v6.3.0/OpenType.zip", "fonts", "IBMPlexMono-Regular")
    # Fraunces (we'll just download a direct link to a Fraunces TTF or a similar serif if Fraunces is hard to find in a zip)
    # Let's download Fraunces from Google Fonts directly via a known TTF URL or Playfair Display as fallback.
    fraunces_url = "https://github.com/googlefonts/fraunces/raw/master/fonts/ttf/Fraunces-Regular.ttf"
    r = requests.get(fraunces_url)
    with open("fonts/Fraunces-Regular.ttf", "wb") as f:
        f.write(r.content)
    
    fraunces_semi_url = "https://github.com/googlefonts/fraunces/raw/master/fonts/ttf/Fraunces-SemiBold.ttf"
    r = requests.get(fraunces_semi_url)
    with open("fonts/Fraunces-SemiBold.ttf", "wb") as f:
        f.write(r.content)
        
    print("Fonts downloaded.")
