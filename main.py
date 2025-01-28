import base64
import requests
from PIL import Image, ImageDraw
from io import BytesIO
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import filedialog, messagebox
from wand.image import Image as WandImage

# Client settings
CLIENT_ID = '-----------------'
CLIENT_SECRET = '-----------------'

# Auth
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = Spotify(auth_manager=auth_manager)

def get_track_id(spotify_url):
    """
    Downloading ID of song based on URL.
    """
    results = sp.track(spotify_url)
    return results['id']

def generate_spotify_code(track_id, output_path='spotify_code.png'):
    """
    Generating Spotify Code.
    """
    api_url = f'https://scannables.scdn.co/uri/plain/png/000000/white/640/spotify:track:{track_id}'

    # downloading PNG
    response = requests.get(api_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(output_path)
        print(f'Spotify Code saved as {output_path}')
        return output_path
    else:
        print('Error downloading Spotify Code.')
        return None

def convert_png_to_svg(png_path, svg_path):
    """
    Converrting PNG to SVG using Wand (ImageMagick).
    """
    with WandImage(filename=png_path) as img:
        img.format = 'svg'
        img.save(filename=svg_path)
    print(f'PNG file converted to SVG and saved as {svg_path}')

def on_generate():
    spotify_url = url_entry.get()
    if not spotify_url:
        messagebox.showerror("Error", "Please insert URL from Spotify.")
        return

    track_id = get_track_id(spotify_url)
    png_path = generate_spotify_code(track_id)
    
    if png_path:
        svg_path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG files", "*.svg")])
        if svg_path:
            convert_png_to_svg(png_path, svg_path)
            messagebox.showinfo("Success", "Spotify Code generated and saved as SVG.")

#GUI
root = tk.Tk()
root.title("Spotify Code Generator")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="song URL from Spotify:").grid(row=0, column=0, sticky="w")
url_entry = tk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

generate_button = tk.Button(frame, text="GENERATE CODE", command=on_generate)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()