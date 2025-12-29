A simple GUI application built with PyQt6 that generates 300 random abstract vector images in 1024x1024 resolution. The tool creates procedural SVG graphics based on a custom color palette. Each image is saved as a PNG file, along with a corresponding TXT file containing a generated prompt describing the IMAGE.

The generated images features abstract compositions using shapes like rectangles, circles, arcs, triangles, crosses, dots, and polygons, arranged in a random grid layout. 

The intention for this script is to be able to generate large quantities of unique images with the same colour palette with captions for training AI LoRA models.

## Features

- **User Input**: 
- Trigger word for styling the prompt   
- Custom color palette via hex codes or color picker. 
- **Batch Generation**: Automatically creates 300 unique images and prompts. 
- **Output**: - PNG images at 1024x1024 resolution. 
- TXT files with descriptive prompts for each image, suitable for use in AI image generation tools or documentation. 
- **Procedural Art**: Randomly generates grids and shapes for variety. 
- **UI Feedback**: Progress updates during generation.

## Requirements

- Python 3.6+ (tested with Python 3.12.3 compatibility in mind). 
- PyQt6: For the GUI and SVG rendering. 
- svgwrite: For creating SVG files.

## Installation

1. Clone or download the repository/script:
2.  git clone 
3. cd vector-art-generator

Install dependencies using pip: pip install PyQt6 svgwrite

## Usage

1. Run the script: python 300_random_colour_pallete_images_with_prompts.py
2. In the GUI: - Enter a **Trigger Word** (Your Colour pallet name is usually good or any activation word). 
3. Add colors to the **Color Palette** using hex codes (e.g., #FF0000) or the color picker. 
4. Select an **Output Folder** to save the generated files. 
5. Click **Generate 300 Images** to start the process.

## Output Files: 
- vector_art_{i}.png`: The generated image (1024x1024 PNG). 
- vector_art_{i}.txt`: A text file with a prompt like: "colour palette, an abstract composition of geometric rectangles, circular motifs in colors #FF0000, #00FF00, vector art style, clean lines, high quality, colour palette".

The generation process may take some time depending on your hardware, as it creates and converts 300 high-resolution images.

## Notes

- Temporary SVG files are created during generation but automatically deleted after conversion to PNG. - Ensure the output folder has write permissions. - If you encounter issues with SVG rendering, verify that PyQt6 is correctly installed. - The total number of images (300) is hardcoded but can be modified by changing `self.TOTAL_GENERATE_COUNT` in the script.