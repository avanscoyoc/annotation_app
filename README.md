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

### Docker Setup
The application can also be run in a Docker container.

Build Docker
```bash
docker build -t annotation_app .
```

Run the Docker Container
```bash
docker run -p 8000:8000 annotation_app
```

---

### CI/CD Pipeline
This repository includes a GitHub Actions workflow for CI/CD. The workflow automates testing, building, and pushing the Docker image to GitHub Packages.

### GitHub Actions Setup
Ensure your GitHub repository is configured for GitHub Actions.
Review the .github/workflows/main.yml file to confirm the pipeline configuration.

### Trigger the Pipeline
The pipeline runs automatically on push to the main branch, building and deploying the application.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request.

### License
This project is licensed under the MIT License.