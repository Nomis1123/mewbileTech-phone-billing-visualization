# MewbileTech - A Phone Billing & Call Visualization System

This project is a comprehensive simulation of a mobile phone company's billing and call management system, implemented entirely in Python. It is designed to showcase core Object-Oriented Programming (OOP) principles, including inheritance, polymorphism, and composition, alongside data processing from JSON files and interactive GUI development with Pygame.

## Features

*   **Complex Data Simulation:** Loads and processes a dataset of customers, their phone lines, and a chronological history of their call/SMS events from a `dataset.json` file.
*   **Object-Oriented Billing System:** Implements three distinct contract types using an inheritance hierarchy, each with unique billing logic:
    *   `TermContract`: A fixed-term contract with a monthly fee, an initial deposit, and a set number of included free minutes.
    *   `MTMContract`: A flexible month-to-month contract with a standard monthly fee and per-minute billing.
    *   `PrepaidContract`: A pay-as-you-go contract where call costs are deducted from a pre-loaded balance, with automatic top-up functionality when the balance is low.
*   **Interactive Call Visualization:**
    *   Uses **Pygame** to render an interactive map of Toronto.
    *   Plots the source and destination of each call as a visual connection line on the map.
    *   The map view supports both panning and zooming for detailed inspection.
*   **Dynamic Data Filtering:**
    *   Provides a user-friendly GUI to filter the calls displayed on the map based on various criteria.
    *   **Filter by Customer ID (`c`):** Isolates all calls made or received by a single customer.
    *   **Filter by Call Duration (`d`):** Selects calls greater (`G`) or less (`L`) than a specified time in seconds.
    *   **Filter by Geographic Location (`l`):** Displays calls where the source or destination falls within a specified rectangular coordinate area.
    *   **Reset Filter (`r`):** Clears all active filters and displays the entire dataset.
*   **On-Demand Bill Generation (`m`):**
    *   Allows the user to generate and print a detailed monthly bill for any customer directly to the console.
    *   The bill summary includes total cost, fixed fees, billed minutes, free minutes used, and per-minute rates according to the customer's contract type.
*   **Structured Architecture:** The system is built with a clear separation of concerns, dividing data models, business logic (contracts), and the presentation layer (visualizer).
dering (`Pygame`) and user input (`tkinter` for pop-ups).

## Running the Application

To launch the simulation and the visualizer, run the `application.py` script from the project's root directory:

```sh
python application.py
```

### How to Use the Interface

The application is controlled via keyboard shortcuts. When a filter key is pressed, a pop-up window will prompt for input.

| Key | Action                    | Input Format Example                                     |
|:---:|:--------------------------|:---------------------------------------------------------|
| `c` | **Filter by Customer ID** | `5716`                                                   |
| `d` | **Filter by Duration**    | `G100` (Greater than 100s) or `L60` (Less than 60s)       |
| `l` | **Filter by Location**    | `-79.6, 43.6, -79.3, 43.7`                               |
| `r` | **Reset All Filters**     | (No input needed)                                        |
| `m` | **Generate Monthly Bill** | 1st Prompt: `5716`<br>2nd Prompt: `1, 2018`            |
| `x` | **Quit Application**      |                                                          |
