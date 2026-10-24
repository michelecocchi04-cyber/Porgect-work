# FarmProduction Simulator

A command-line simulator of a fruit & vegetable farm. Pick products, choose how to harvest them, and the program calculates growth time, harvest time, workforce allocation, resource conflicts and the final **delivery date**, taking weekends, Italian public holidays and random weather events into account.

> **Note:** the program's interface (menus and messages) is in **Italian**.

---

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [How to use it](#how-to-use-it)
- [How the simulation works](#how-the-simulation-works)
- [Product catalogue](#product-catalogue)
- [Project structure](#project-structure)
- [Customisation](#customisation)
- [Known limitations](#known-limitations)

---

## Features

- **15 products** across 3 categories (vegetables, fruit, cereals & seeds), each with its own growth time, harvest priority and harvest rates.
- **Multi-product orders**: up to **5 products in parallel** in a single order.
- **Two harvest methods**: manual (workers) or automatic (industrial machines).
- **Resource conflict management**: limited workers and machines, with automatic or manual conflict resolution.
- **Random events**: variable growth times and seasonal weather disasters (floods, drought, heavy rain, frost).
- **Realistic delivery date**: skips weekends, Italian public holidays and the Christmas break.
- **Shipping estimate** depending on the customer's location.
- **Quick random simulation** mode for a one-shot demo.

---

## Requirements

- **Python 3.6+**
- No external dependencies: only the standard library (`datetime`, `locale`, `os`, `random`, `math`).

---

### Locale (day and month names)

The program tries to switch to the Italian locale (`it_IT.UTF-8`, `it_IT`, `ita_it`, `Italian`) to print day and month names in Italian. If none of them is available on your system, it silently falls back to the default locale and dates will appear in that language.

## How to use it

When launched, the program shows the main menu:

| Option | Action |
|:------:|--------|
| `1` | Show the list of all products offered by the farm |
| `2` | Request a product (build a real production plan, up to 5 products) |
| `3` | Run a quick **random** simulation |
| `4` | Exit |

### Option 2 – Production plan

1. Choose a **category** (vegetables, fruit, cereals & seeds).
2. Type the **product** you want.
3. Enter the **quantity in kg** (minimum 100 kg, and not above the field capacity shown).
4. Choose the **harvest method**: manual or automatic.
5. Add another product (up to 5) or proceed to the order execution.
6. If needed, resolve **resource conflicts** (see below).
7. Enter your **location** to get the shipping estimate.

At the end you get a summary with cultivation days, harvest days, total work hours, the date the order will be ready at the farm and the final delivery date.

### Option 3 – Random simulation

Picks a random product, quantity (100–7000 kg), harvest method and customer location, then prints the whole process and the delivery date. Great for a quick demo.

---

## How the simulation works

### Growth time

Each product has a base growth time (in days). The actual value is randomised by **±15%**. On top of that, each cultivation has a **5% chance** of a disaster that adds **10–30 days** of delay. The message depends on the current season:

| Period | Event |
|--------|-------|
| 21 Mar – 20 Jun | Spring floods |
| 21 Jun – 22 Sep | Summer drought |
| 23 Sep – 20 Dec | Autumn heavy rain |
| 21 Dec – 20 Mar | Winter frost |

### Availability

When a product is selected there is a small random chance that its production capacity is **exhausted** and it cannot be ordered. Otherwise, a random **maximum field capacity** (up to 7000 kg) is generated, and the requested quantity must stay within it.

### Harvest priority

Products are sorted by **harvest priority** (3 = most urgent, 1 = least), based on how quickly they deteriorate (e.g. tomatoes, lettuce, grapes and strawberries are priority 3; potatoes, olives and cereals are priority 1).

### Manual harvest

- The farm has **10 workers** in total.
- Each manual product starts with **2 workers**; remaining workers are then distributed one at a time, starting from the products with the largest quantities, up to **5 workers per product**.
- Daily output per worker varies randomly by **±7%**.

### Automatic harvest

- The farm has **2 machines**.
- Machines work every day at a constant rate.

### Resource conflicts

If **more than 2 products** use the automatic method, the program asks how to handle the conflict:

- **Automatic management** – the product that can't get a machine is moved to manual harvest if at least 2 workers are free; otherwise it waits.
- **Manual management** – you choose between making the product **wait in the queue** or **switching it to manual** harvest.

### Organisation day

If the longest job of the order takes **8 hours or more**, **1 extra day** is added to organise machines and workers.

### Working calendar and delivery date

Days are counted only if they are **not**:

- Saturdays or Sundays
- Italian public holidays (1 Jan, 6 Jan, 25 Apr, 1 May, 2 Jun, 15 Aug, 1 Nov, 8 Dec, 25 Dec, 26 Dec)
- Part of the **Christmas break** (25 Dec – 6 Jan)

### Shipping

The farm is based in **Rome**. Delivery time is added after the order is ready:

| Customer location | Extra time |
|-------------------|-----------|
| Same city | +1 day |
| Province and surroundings | +2 to 3 days |
| Elsewhere in Italy | +4 to 6 days |
| Outside Italy | ❌ Not available |

---

## Product catalogue

| Category | Products |
|----------|----------|
| **Vegetables** (*ortaggi e verdure*) | tomatoes, lettuce, potatoes, onions, carrots |
| **Fruit** (*frutta*) | grapes, apples, oranges, pears, strawberries, olives |
| **Cereals & seeds** (*cereali e semi*) | wheat, corn, rice, sunflowers |

> Product names inside the program are typed in Italian (`pomodori`, `lattuga`, `patate`, `cipolle`, `carote`, `uva`, `mele`, `arance`, `pere`, `fragole`, `olive`, `grano`, `mais`, `riso`, `girasoli`).

---

## Project structure

The whole program lives in a single file, `tesi_agricoltura.py`:

| Function | Role |
|----------|------|
| `DATASET_AZIENDA` | Dictionary with all products and their parameters |
| `titolo()` | Prints the title banner with the current date |
| `menu_principale()` | Main menu loop |
| `esegui_menu_uno()` | Option 1: product list |
| `esegui_menu_due()` | Option 2: production plan |
| `esegui_menu_tre()` / `generazione_casuale()` | Option 3: random simulation |
| `scelta()` | Product/quantity selection and validation |
| `seleziona_metodo_lavoro()` | Manual vs automatic selection |
| `distribuisci_operai()` | Worker allocation across products |
| `lavoro_parallelo_()` | Day-by-day parallel simulation with conflict handling |
| `calcolo_totale()` | Hours and days needed for a harvest |
| `variabile_crescita_base()` / `stagione()` | Random growth time and seasonal disasters |
| `calcola_data_consegna()` | Working-day calendar (weekends, holidays) |
| `spedizione()` | Shipping time based on location |
| `stampa_finale()` | Final order summary |

---

## Customisation

All product data is stored in the `DATASET_AZIENDA` dictionary at the top of the file. To add a product, add an entry under the right category:

```python
"zucchine": {
    "crescita_base": 60,            # growth time (days)
    "priorità_raccolta": 3,         # 1 (low) to 3 (urgent)
    "manuale": {
        "tempo_raccolta_kg": 2.0,               # minutes per kg
        "capacita_giornaliera_singolo": 240     # kg/day per worker
    },
    "automatico": {
        "tempo_raccolta_kg": 1.0,               # minutes per kg
        "capacita_giornaliera": 1500            # kg/day per machine
    }
},
```

Other tweakable values: number of workers (`operai_disponibili` in `distribuisci_operai`), number of machines (limit of 2 in `lavoro_parallelo_`), disaster probability and delay range (`variabile_crescita_base`), and holidays (`festivi` in `calcola_data_consegna`).

---

## Known limitations

- The interface is in Italian only.
- The simulation is stochastic: results change at every run.
- Shipping is only available within Italy, from a fixed origin (Rome).
- No data is saved between runs.

---

## License

Add your preferred license here (e.g. MIT).
