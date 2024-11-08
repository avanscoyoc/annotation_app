# Annotation App

This is a Tkinter-based tool for annotating audio clips. The application is built to assist researchers in bioacoustics with the efficient annotation of datasets, enabling users to listen to audio clips, view spectrograms, and save their annotations. It also supports a CI/CD pipeline through GitHub Actions for streamlined development and deployment.

---

## Features

- Load and annotate audio datasets.
- Play audio clips and view corresponding spectrograms.
- Save annotations with options for different labels.
- Automated deployment using Docker and GitHub Actions.

---

## Requirements

- Python 3.9
- Tkinter (GUI library for Python)
- `pydub`, `matplotlib`, and other dependencies (see `environment.yaml`)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/annotation_app.git
cd annotation_app
```

### 2. Set Up the Environment with Conda
Install Miniconda and set up the environment by running:

```bash
conda env create -f environment.yaml
conda activate annotation_app
```

### 3. Run the Application
```bash
python main.py
```

### Usage
- *Load Dataset:* Select a dataset folder to load.
- *Annotate Clips:* Each audio file will play with a spectrogram. Select an annotation label and save your response.
- *Export Annotations:* Saved annotations can be exported for further analysis.

### License
This project is licensed under the MIT License.