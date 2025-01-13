# Fantasy Frontier

Fantasy Frontier is a city management game set in a low-magic, fantasy-inspired world. Players build and manage a city, balancing resources, expanding infrastructure, and ensuring their citizens thrive in a challenging and dynamic environment. The game leverages a hex-based system for city layouts and resource management.

---

## Features

- **Hex-Based City Layout**: Build your city one hex at a time with modular building placements.
- **Resource Management**: Gather resources from surrounding areas and allocate them to grow your city.
- **Strategic Expansion**: Manage resources and choose the best strategies for expanding your city.
- **Dynamic Challenges**: Adapt to evolving scenarios and ensure your city survives and thrives.

---

## Getting Started

### Prerequisites

To run the game, ensure you have the following installed:

- Python 3.12 or higher(it may work on lower versions, but it was developed on 3.12)
- Virtual environment tools (e.g., `venv`)
- Alternately, if binary releases are available, download one of those for your system.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/hamshrew/fantasy-frontier.git
    cd fantasy-frontier
    ```

2. Set up a virtual environment and install dependencies:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Run tests to confirm everything is working:

    ```bash
    pytest
    ```

### Running the Game

Use the following command to start the game:

```bash
python -m ffrontier.main
```
