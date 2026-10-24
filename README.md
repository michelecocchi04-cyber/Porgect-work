# Agricultural Management and Simulation System

This repository contains a **Python**-based software solution designed to optimize and simulate cultivation, harvesting, and logistics processes for an agricultural enterprise. 

The application enables efficient management of agricultural resources, harvest planning (both manual and automated), and precise calculation of production timelines and domestic shipping schedules.

## Key Features & Menu Structure

The software is organized into a user-friendly, **3-menu interface**:

### Menu 1: Cultivation Catalog
* **Product Inventory:** Displays the complete list of crops available for cultivation.
* **Overview:** Provides comprehensive details on available seeds and crop varieties within the system.

### Menu 2: Order Planning, Management, and Timelines
This module allows users to configure custom orders, with the system dynamically calculating processing times:
* **Product Selection:** Select up to **5 different products** simultaneously.
* **Quantity Input:** Specify the target weight in kilograms (kg) for each selected crop.
* **Harvest Mode:** Choose between **manual** or **automated** harvesting. 
  * *Note: Automated harvesting includes a queue management system that locks and queues tasks if the **2 available automatic harvesters** are currently occupied.*
* **Timeline Calculations & Display:**
  * Displays the **individual cultivation time** for each selected product.
  * Calculates the **total harvesting time** required to process the entire order.
  * Estimates the **final delivery time** to the destination (automatically excluding weekends/holidays and restricting shipping exclusively to domestic destinations).

### Menu 3: Quick Single-Product Random Simulation
Unlike the user-driven configuration in Menu 2, this module runs an automated test simulation:
* **Random Generation:** The system automatically picks **a single random product** from the catalog.
* **Timeline Simulation:** Instantly calculates and displays the full workflow timeline (cultivation, harvesting, and domestic shipping excluding holidays) specifically for the selected crop.

## Tech Stack & Architecture
* **Language:** Python 3.14.3
* **Paradigma:** Procedural and modular programming focusing on robust conditional workflow control.
