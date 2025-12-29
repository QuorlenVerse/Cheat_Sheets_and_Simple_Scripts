import sys
import os
import random
import svgwrite
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QListWidget, QFileDialog, QColorDialog, QMessageBox)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import QSize

class VectorArtGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vector Art Generator (1024x1024)")
        self.setMinimumSize(500, 500)

        # Configuration constants
        self.IMAGE_SIZE = 1024
        self.TOTAL_GENERATE_COUNT = 300

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Trigger word input
        trigger_layout = QHBoxLayout()
        trigger_label = QLabel("Trigger Word:")
        self.trigger_input = QLineEdit()
        self.trigger_input.setPlaceholderText("e.g., Bauhaus, Minimalist")
        trigger_layout.addWidget(trigger_label)
        trigger_layout.addWidget(self.trigger_input)
        layout.addLayout(trigger_layout)

        # Color palette list
        color_label = QLabel("Color Palette (Hex Codes):")
        layout.addWidget(color_label)
        self.color_list = QListWidget()
        layout.addWidget(self.color_list)

        # Add color buttons
        add_color_layout = QHBoxLayout()
        self.hex_input = QLineEdit()
        self.hex_input.setPlaceholderText("#RRGGBB")
        add_hex_button = QPushButton("Add Hex")
        add_hex_button.clicked.connect(self.add_hex_color)
        add_picker_button = QPushButton("Color Picker")
        add_picker_button.clicked.connect(self.add_picker_color)
        add_color_layout.addWidget(self.hex_input)
        add_color_layout.addWidget(add_hex_button)
        add_color_layout.addWidget(add_picker_button)
        layout.addLayout(add_color_layout)

        # Remove selected color
        remove_button = QPushButton("Remove Selected Color")
        remove_button.clicked.connect(self.remove_color)
        layout.addWidget(remove_button)

        # Output folder
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Output Folder:")
        self.folder_input = QLineEdit()
        self.folder_input.setReadOnly(True)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_button)
        layout.addLayout(folder_layout)

        # Generate button - Updated label to show correct count
        self.generate_btn = QPushButton(f"Generate {self.TOTAL_GENERATE_COUNT} Images")
        self.generate_btn.setStyleSheet("font-weight: bold; padding: 10px; background-color: #2ecc71; color: white;")
        self.generate_btn.clicked.connect(self.generate_images)
        layout.addWidget(self.generate_btn)

    def add_hex_color(self):
        hex_code = self.hex_input.text().strip()
        if self.is_valid_hex(hex_code):
            self.color_list.addItem(hex_code.upper())
            self.hex_input.clear()
        else:
            QMessageBox.warning(self, "Invalid Hex", "Enter a valid hex code like #RRGGBB.")

    def add_picker_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            hex_code = color.name().upper()
            self.color_list.addItem(hex_code)

    def remove_color(self):
        selected = self.color_list.selectedItems()
        for item in selected:
            self.color_list.takeItem(self.color_list.row(item))

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.folder_input.setText(folder)

    def is_valid_hex(self, hex_code):
        if not hex_code.startswith('#') or len(hex_code) != 7:
            return False
        try:
            int(hex_code[1:], 16)
            return True
        except ValueError:
            return False

    def generate_images(self):
        trigger = self.trigger_input.text().strip()
        if not trigger:
            QMessageBox.warning(self, "Missing Input", "Enter a trigger word.")
            return

        colors = [self.color_list.item(i).text() for i in range(self.color_list.count())]
        if not colors:
            QMessageBox.warning(self, "Missing Input", "Add at least one color to the palette.")
            return

        output_folder = self.folder_input.text().strip()
        if not output_folder or not os.path.isdir(output_folder):
            QMessageBox.warning(self, "Missing Input", "Select a valid output folder.")
            return

        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("Generating... Please wait")
        QApplication.processEvents() # Update UI

        try:
            for i in range(self.TOTAL_GENERATE_COUNT):
                svg_path = os.path.join(output_folder, f"vector_art_{i}.svg")
                png_path = os.path.join(output_folder, f"vector_art_{i}.png")
                txt_path = os.path.join(output_folder, f"vector_art_{i}.txt")

                # Generate procedural SVG at 1024x1024
                description = self.create_svg(svg_path, colors)

                # Convert to PNG at 1024x1024
                self.svg_to_png(svg_path, png_path)

                # Clean up temporary SVG
                if os.path.exists(svg_path):
                    os.remove(svg_path)

                # Write caption to TXT
                prompt = f"{trigger}, {description} in colors {', '.join(colors)}, vector art style, clean lines, high quality, {trigger}"
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(prompt)
                
                # Small UI update every 10 images
                if i % 10 == 0:
                    self.generate_btn.setText(f"Generating ({i}/{self.TOTAL_GENERATE_COUNT})...")
                    QApplication.processEvents()

            QMessageBox.information(self, "Success", f"Batch complete! {self.TOTAL_GENERATE_COUNT} images and prompts generated at 1024x1024.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        finally:
            self.generate_btn.setEnabled(True)
            self.generate_btn.setText(f"Generate {self.TOTAL_GENERATE_COUNT} Images")

    def create_svg(self, svg_path, colors):
        size = self.IMAGE_SIZE
        dwg = svgwrite.Drawing(svg_path, size=(f'{size}px', f'{size}px'))

        # Background
        bg_color = random.choice(colors)
        dwg.add(dwg.rect(insert=(0, 0), size=(size, size), fill=bg_color))

        # Random Grid setup
        rows = random.randint(3, 8)
        cols = random.randint(3, 8)
        cell_w = size / cols
        cell_h = size / rows

        shapes_desc = []
        
        # Possible shapes
        shape_types = ['rect', 'circle', 'quarter', 'triangle', 'cross', 'dots', 'poly']

        for r in range(rows):
            for c in range(cols):
                x, y = c * cell_w, r * cell_h
                color = random.choice(colors)
                shape = random.choice(shape_types)

                if shape == 'rect':
                    dwg.add(dwg.rect(insert=(x, y), size=(cell_w, cell_h), fill=color))
                    shapes_desc.append("geometric rectangles")

                elif shape == 'circle':
                    cx, cy = x + cell_w/2, y + cell_h/2
                    rad = min(cell_w, cell_h) / 2 * random.uniform(0.6, 0.9)
                    dwg.add(dwg.circle(center=(cx, cy), r=rad, fill=color))
                    shapes_desc.append("circular motifs")

                elif shape == 'quarter':
                    # Randomize corner for variety
                    r_px = min(cell_w, cell_h)
                    path_data = f"M {x},{y+cell_h} A {r_px},{r_px} 0 0 1 {x+cell_w},{y} L {x},{y} Z"
                    dwg.add(dwg.path(d=path_data, fill=color))
                    shapes_desc.append("quarter-circle arcs")

                elif shape == 'triangle':
                    pts = [(x, y+cell_h), (x+cell_w, y+cell_h), (x+cell_w/2, y)]
                    dwg.add(dwg.polygon(points=pts, fill=color))
                    shapes_desc.append("triangular elements")

                elif shape == 'cross':
                    bw = cell_w / 5
                    dwg.add(dwg.rect(insert=(x, y + cell_h/2 - bw/2), size=(cell_w, bw), fill=color))
                    dwg.add(dwg.rect(insert=(x + cell_w/2 - bw/2, y), size=(bw, cell_h), fill=color))
                    shapes_desc.append("intersecting crosses")

                elif shape == 'dots':
                    dot_r = min(cell_w, cell_h) / 10
                    for dx in [0.3, 0.7]:
                        for dy in [0.3, 0.7]:
                            dwg.add(dwg.circle(center=(x + dx*cell_w, y + dy*cell_h), r=dot_r, fill=color))
                    shapes_desc.append("dotted patterns")

                elif shape == 'poly':
                    n = random.randint(3, 5)
                    pts = [(x + random.random()*cell_w, y + random.random()*cell_h) for _ in range(n)]
                    dwg.add(dwg.polygon(points=pts, fill=color))
                    shapes_desc.append("irregular polygons")

        dwg.save()
        unique_shapes = list(set(shapes_desc))
        return f"an abstract composition of {', '.join(unique_shapes)}"

    def svg_to_png(self, svg_path, png_path):
        renderer = QSvgRenderer(svg_path)
        # Create image at the target 1024x1024 resolution
        image = QImage(self.IMAGE_SIZE, self.IMAGE_SIZE, QImage.Format.Format_ARGB32)
        image.fill(0) # Transparent background
        
        painter = QPainter(image)
        # Antialiasing for smoother vector edges at high res
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        renderer.render(painter)
        painter.end()
        
        image.save(png_path, "PNG")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VectorArtGenerator()
    window.show()
    sys.exit(app.exec())
