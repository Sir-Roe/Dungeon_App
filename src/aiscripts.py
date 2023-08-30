from pathlib import Path
from io import BytesIO
from PIL import Image
import openai
import requests
import os


folder_dir = os.path.join(Path(__file__).parents[0], 'data')
def generateImage(selection):
    r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': f'{selection},dungeons and dragons, monster, fantasy theme, animated,',
    },
    headers={'api-key': '0fe3d007-4d4e-420a-b796-4c01badcdbc9'})

    response = requests.get(r.json()['output_url'])
    img= Image.open(BytesIO(response.content))
    img =img.convert('RGB')
    output_image_path = f'{folder_dir}\{selection}.png'
    img.save(output_image_path)
    return (output_image_path)