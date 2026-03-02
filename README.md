# masks_sim

`masks_sim` is a small COVID-era class project that simulates how people move between buildings, tracks infections over time, and then uses the generated data for a dashboard and an LSTM-based forecast.

The repository has three parts:

- `src/`: the simulation itself.
- `dashboard.py`: a Dash app for exploring the generated CSV files.
- `prediction_LSTM.py`: a forecasting script that trains on the simulation output.

## What the simulation does

The model creates a synthetic population with three person types:

- workers
- students
- people who stay at home

Each person moves between locations such as homes, workplaces, hospitals, pharmacies, schools, markets, and a mall. Infection status, PCR status, recovery, immunity, hospital admission, and mortality are updated as the simulation advances hour by hour.

At the end of the run, the project exports CSV files with:

- daily totals for deaths, infections, immunity, and severity
- per-building PCR snapshots over time
- per-building positive ratios
- person-level infection and severity histories

## Repository layout

- `src/main.py`: entry point for generating the simulation data.
- `src/people.py`: person classes, infection logic, and daily test aggregation.
- `src/buildings.py`: building definitions and contact logic.
- `src/utils.py`: shared helpers and constants.
- `src/errors.py`: custom exceptions for closed/full buildings.
- `dashboard.py`: dashboard built with Dash and Plotly.
- `prediction_LSTM.py`: LSTM training and prediction script.

## Running it

Run the project from the repository root so the generated CSV files stay next to the scripts that consume them.

1. Generate the simulation data:

```powershell
py -3 src/main.py
```

2. Train the forecasting model and export predictions:

```powershell
py -3 prediction_LSTM.py
```

3. Start the dashboard:

```powershell
py -3 dashboard.py
```

## Notes

- The simulation parameters are hard-coded in `src/main.py`.
- Generated CSV files are intentionally ignored by git.
- This is a coursework project and the code keeps the original project structure rather than trying to turn it into a polished package.

## License

This project is licensed under the MIT License. See `LICENSE`.
