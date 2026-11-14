
# STAT 159 Homework 3: Tennis Career Python Package

This repository contains `tennis_career`, a Python package developed for UC Berkeley's STAT 159 course.

The package retrieves, processes, and visualizes professional tennis players' career match data from [Tennis Abstract](https://www.tennisabstract.com/). It builds on the Serena Williams visualization from Homework 2, comparing a player's age with the ages of their opponents across their career.

## Features

The package provides two public functions:

1. `get_player_matches(player_name, gender)` retrieves and processes a player's career match data, including match dates, outcomes, opponent information, and age differences.

2. `plot_age_difference(df, player_name)` generates a scatter plot showing the player's age against the age difference between the player and their opponents, with colors distinguishing wins from losses.

The package supports both male and female players and accounts for differences in the formats of their Tennis Abstract records.

## Repository Structure

```text
hw03-2-darrensolichin/
├── README.md
├── pyproject.toml
├── .gitignore
├── explore_data.ipynb
├── src/
│   └── tennis_career/
│       ├── __init__.py
│       ├── data.py
│       └── plotting.py
└── tests/
    ├── test_data.py
    └── test_plotting.py
```

- `data.py`: Retrieves, cleans, and processes tennis match records.
- `plotting.py`: Generates the NYT-inspired scatter plot.
- `__init__.py`: Exposes the package's two public functions.
- `explore_data.ipynb`: Demonstrates the package using Serena Williams and Rafael Nadal.
- `tests/`: Contains automated tests for data processing and plotting.
- `pyproject.toml`: Defines the package configuration and dependencies.

## Installation

The package requires Python 3.9 or newer.

Install directly from GitHub:

```bash
python -m pip install git+https://github.com/UCB-stat159-f26/hw03-2-darrensolichin.git
```

Alternatively, clone the repository and install it locally:

```bash
git clone https://github.com/UCB-stat159-f26/hw03-2-darrensolichin.git
cd hw03-2-darrensolichin
python -m pip install -e ".[test]"
```

The package uses pandas, NumPy, Matplotlib, and requests. These dependencies are specified in `pyproject.toml`.

## Usage

### 1. Import the package

```python
from tennis_career import get_player_matches, plot_age_difference
import matplotlib.pyplot as plt
```

### 2. Retrieve player match data

For Serena Williams:

```python
serena_df = get_player_matches("Serena Williams", "female")
print(serena_df.head())
```

The returned DataFrame includes:

| Column | Description |
|---|---|
| `match_date` | Date of the match |
| `result` | Match outcome (`W` or `L`) |
| `opponent` | Opponent's name |
| `opponent_info` | Original opponent information |
| `player_age` | Player's age at the match |
| `opponent_age` | Opponent's age at the match |
| `age_difference` | Player's age minus opponent's age |

A positive age difference indicates that the player was older than their opponent, while a negative value indicates that the player was younger.

### 3. Generate the scatter plot

```python
fig, ax = plot_age_difference(
    serena_df,
    player_name="Serena Williams"
)

plt.show()
```

The plot displays player age on the horizontal axis and age difference on the vertical axis. Cyan points represent wins, while purple points represent losses.

### 4. Analyze another player

The same functions can be used for Rafael Nadal:

```python
nadal_df = get_player_matches("Rafael Nadal", "male")

fig, ax = plot_age_difference(
    nadal_df,
    player_name="Rafael Nadal"
)

plt.show()
```

## Testing

The package includes automated tests written using `pytest`.

The tests cover:

- Parsing Tennis Abstract JavaScript match records.
- Converting raw records into a pandas DataFrame.
- Calculating player and opponent ages.
- Handling differences between male and female data formats.
- Calculating age differences.
- Validating plot coordinates, colors, titles, legends, and formatting.

The data tests use mock records based on examples provided in the homework instructions. This avoids making requests to Tennis Abstract during automated testing.

To run the tests:

```bash
python -m pytest tests/ -v
```

At the time of submission preparation, all 21 tests passed.

## Data Source and Limitations

The data is retrieved from [Tennis Abstract](https://www.tennisabstract.com/).

The completeness of the match records depends on the data available from Tennis Abstract. For example, the retrieved Rafael Nadal dataset contains 1,096 matches from September 2001 through October 2016, rather than his entire professional career.

The package requires an internet connection to retrieve match records. Requests may occasionally fail or time out if the website is unavailable.

## Personal Reflections

One of the biggest things I learned from this assignment was how to turn code that I would normally just write in a Jupyter notebook into an actual Python package that other people can use. One of the main challenges I faced was working with the Tennis Abstract data because the files had a bunch of columns that weren't clearly labeled, and I also had to account for the differences between male and female players' data. I spent quite a bit of time figuring out how to extract the information I needed and make sure the calculations were correct. I also got more familiar with writing tests, which was something I hadn't really done much of before. I found it interesting that I could use mock data to test my functions without having to download the actual data every time. Overall, I think this assignment helped me become more comfortable with organizing my code, debugging issues, and thinking about how someone else would be able to install and use something I created, rather than just making sure it works on my own computer.