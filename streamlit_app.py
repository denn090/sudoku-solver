import streamlit as st
import json
import time
from solver import solve, solve_step_by_step, reset_attempts, get_attempts
from difficulty import count_empty, estimate_difficulty

st.set_page_config(page_title="Sudoku Solver", layout="centered")
st.title("Sudoku Solver")

examples = {}
try:
    with open("examples/sudoku_examples.json", "r", encoding="utf-8") as f:
        examples = json.load(f)
except FileNotFoundError:
    st.warning("Beispiel-Datei `examples/sudoku_examples.json` nicht gefunden.")

if "load_example" in st.session_state:
    beispiel = examples.get(st.session_state["load_example"])
    if beispiel:
        for i in range(9):
            for j in range(9):
                st.session_state[f"{i}-{j}"] = str(beispiel[i][j])
    del st.session_state["load_example"]
    st.rerun()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Beispielrätsel")
    if examples:
        auswahl = st.selectbox("Wähle ein Beispiel", list(examples.keys()))
        if st.button("Beispiel übernehmen"):
            st.session_state["load_example"] = auswahl
            st.rerun()

with col2:
    grid = []
    html = """
    <style>
        input {
            text-align: center;
            font-size: 20px;
            width: 42px;
            height: 42px;
            border: none;
            background-color: #1e1e1e;
            color: white;
        }
        td {
            padding: 0;
        }
    </style>
    """
    html += '<form><table style="border-collapse:collapse;margin:auto;margin-top:1rem;margin-bottom:1rem;">'

    for i in range(9):
        html += "<tr>"
        row = []
        for j in range(9):
            key = f"{i}-{j}"
            top = "2px solid white" if i % 3 == 0 else "1px solid #444"
            left = "2px solid white" if j % 3 == 0 else "1px solid #444"
            right = "2px solid white" if j == 8 else ""
            bottom = "2px solid white" if i == 8 else ""
            style = f'border-top:{top};border-left:{left};'
            if right: style += f'border-right:{right};'
            if bottom: style += f'border-bottom:{bottom};'
            if key not in st.session_state:
                st.session_state[key] = "0"
            val = st.session_state[key]
            html += f'<td style="{style}"><input name="{key}" value="{val}" maxlength="1" inputmode="numeric"></td>'
            row.append(int(val) if val.isdigit() else 0)
        html += "</tr>"
        grid.append(row)

    html += "</table></form>"
    st.markdown(html, unsafe_allow_html=True)

def render_sudoku_board(grid, highlight=None, fixed_cells=None):
    html = """
    <style>
        .sudoku-table {
            border-collapse: collapse;
            margin: auto;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .sudoku-table td {
            width: 42px;
            height: 42px;
            text-align: center;
            font-size: 20px;
            color: white;
            padding: 0;
        }
        .fixed-cell {
            background-color: #1e1e1e;
        }
        .solved-cell {
            background-color: #296e30;
        }
        .active-cell {
            background-color: #e3b505 !important;
        }
    </style>
    """
    html += '<table class="sudoku-table">'
    for i in range(9):
        html += "<tr>"
        for j in range(9):
            val = grid[i][j]
            top = "3px solid white" if i % 3 == 0 else "1px solid #666"
            left = "3px solid white" if j % 3 == 0 else "1px solid #666"
            right = "3px solid white" if j == 8 else ""
            bottom = "3px solid white" if i == 8 else ""
            style = f'border-top:{top};border-left:{left};'
            if right: style += f'border-right:{right};'
            if bottom: style += f'border-bottom:{bottom};'

            if highlight == (i, j):
                cell_class = "active-cell"
            elif fixed_cells and fixed_cells[i][j]:
                cell_class = "fixed-cell"
            else:
                cell_class = "solved-cell"

            html += f'<td class="{cell_class}" style="{style}">{val if val != 0 else ""}</td>'
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

for key, default in {
    "generator": None,
    "grid_copy": None,
    "last_step": None,
    "run_animation": False,
    "animation_speed": "Normal",
    "animation_finished": False,
    "paused_animation": False,
    "fixed_cells": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

speed_option = st.selectbox("Geschwindigkeit", ["Langsam", "Normal", "Schnell"], index=["Langsam", "Normal", "Schnell"].index(st.session_state.animation_speed))
st.session_state.animation_speed = speed_option
speed_delay = {"Langsam": 0.9, "Normal": 0.6, "Schnell": 0.02}[speed_option]

# Buttons anzeigen und logische Steuerung
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if not st.session_state.run_animation and not st.session_state.animation_finished:
        if not st.session_state.paused_animation:
            if st.button("▶️ Starten"):
                st.session_state.grid_copy = [[int(cell) for cell in row] for row in grid]
                st.session_state.fixed_cells = [[st.session_state[f"{i}-{j}"] != "0" for j in range(9)] for i in range(9)]
                st.session_state.generator = solve_step_by_step(st.session_state.grid_copy)
                st.session_state.run_animation = True
                st.session_state.paused_animation = False
                st.session_state.animation_finished = False
                st.rerun()
        else:
            if st.button("▶️ Fortsetzen"):
                st.session_state.run_animation = True
                st.session_state.paused_animation = False
                st.rerun()

with col2:
    if st.session_state.run_animation:
        if st.button("⏸️ Pause"):
            st.session_state.run_animation = False
            st.session_state.paused_animation = True
            st.rerun()

with col3:
    if st.button("🔄 Zurücksetzen"):
        for i in range(9):
            for j in range(9):
                st.session_state[f"{i}-{j}"] = "0"
        for key in ["run_animation", "generator", "grid_copy", "last_step", "animation_finished", "paused_animation", "fixed_cells"]:
            st.session_state[key] = False if isinstance(st.session_state.get(key), bool) else None
        st.rerun()

# Frame-by-Frame Animation
if st.session_state.run_animation and st.session_state.generator:
    step = next(st.session_state.generator, None)
    if step is None:
        st.session_state.run_animation = False
        st.session_state.animation_finished = True
        st.rerun()
    else:
        i, j, num = step
        st.session_state.grid_copy[i][j] = num
        st.session_state.last_step = (i, j)
        render_sudoku_board(
            st.session_state.grid_copy,
            highlight=st.session_state.last_step,
            fixed_cells=st.session_state.fixed_cells
        )
        time.sleep(speed_delay)
        st.rerun()

elif st.session_state.grid_copy:
    render_sudoku_board(
        st.session_state.grid_copy,
        highlight=st.session_state.last_step if not st.session_state.animation_finished else None,
        fixed_cells=st.session_state.fixed_cells
    )

# Direkt lösen
if st.button("Sudoku direkt lösen"):
    grid_int = [[int(cell) for cell in row] for row in grid]
    empty_start = count_empty(grid_int)
    reset_attempts()
    if solve(grid_int):
        attempts = get_attempts()
        st.success("Sudoku gelöst!")
        show_classic = st.checkbox("Klassisches Sudoku-Feld anzeigen", value=True)
        if show_classic:
            fixed_cells = [[st.session_state[f"{i}-{j}"] != "0" for j in range(9)] for i in range(9)]
            render_sudoku_board(grid_int, fixed_cells=fixed_cells)
        else:
            st.table(grid_int)
        st.info(f"Leere Felder am Anfang: **{empty_start}**")
        st.info(f"Versuche (valid calls): **{attempts}**")
        st.info(f"Geschätzte Schwierigkeit: **{estimate_difficulty(empty_start, attempts)}**")
    else:
        st.error("Keine Lösung gefunden.")
