
# Loua Assistant

Loua is a voice-activated assistant powered by Python, designed to assist with various tasks using voice commands. This project utilizes several libraries and APIs to provide a seamless and interactive user experience.

## Installation

### Prerequisites

- Python 3.11.7 or later
- `ffmpeg` for audio processing

### Install FFmpeg

The following builds are available through package managers:

- **Release Essentials**:
  ```sh
  choco install ffmpeg
  winget install "FFmpeg (Essentials Build)"
  ```

- **Release Full**:
  ```sh
  choco install ffmpeg-full
  scoop install ffmpeg
  winget install ffmpeg
  ```

- **Release Full Shared**:
  ```sh
  scoop install ffmpeg-shared
  winget install "FFmpeg (Shared)"
  ```

- **Git Master**:
  ```sh
  scoop install ffmpeg-gyan-nightly
  ```

### Install Python Dependencies

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd loua_assistant
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   .\venv\Scripts\ctivate  # On Windows
   source venv/bin/activate  # On Unix or MacOS
   ```

3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the project root directory with the following content:

```
GROQ_API_KEY=<YOUR KEY>
OPENWEATHERMAP_API_KEY=<YOUR KEY>
```

Replace `<YOUR KEY>` with your actual API keys.

## Running the Application

To start the Loua assistant, simply run:

```sh
python .\loua.py
```

## Author

- **Igor Santos de Medeiros**
  - Email: igor.medeiros@gmail.com
  - LinkedIn: [Igor Medeiros](https://www.linkedin.com/in/igormedeiros)
  - GitHub: [Igor Medeiros](https://github.com/igormedeiros)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
