
```markdown
# 📅 Course Timetable Generator (MVP)

A **Simple Course Timetable Generator** that automatically creates a **conflict-free class schedule** using **Google OR-Tools CP-SAT Solver**.  
The project reads course, instructor, room, and enrollment data from CSV files, applies scheduling constraints, and produces a feasible timetable.  

We also built a **Streamlit interface** so users can generate and preview schedules easily without touching the backend code.

---

## 🔍 Project Overview

This project was developed as a **minimum viable product (MVP)** to solve the classic **course timetabling problem**.  
We explored:
- How to model scheduling constraints (room capacity, instructor availability, student conflicts).  
- How to use **constraint programming (CP)** with OR-Tools to find feasible schedules.  
- How to integrate backend logic with a **simple web UI (Streamlit)**.  

The output is stored in `output/schedule.csv` and also displayed in a neat interactive table in the browser.

---

## ✨ Features

✔️ Reads input data from CSV files (`data/` folder).  
✔️ Generates a **feasible timetable** ensuring:  
   - No double-booked rooms  
   - No instructor double-teaching  
   - Room capacity is respected  
   - Student conflicts are avoided  
   - Instructor availability is considered  
✔️ Exports results to `output/schedule.csv`.  
✔️ Interactive **Streamlit app** to run and preview schedules.  

---

## 📂 Folder Structure

```

timetable\_mvp/
│── app.py              # Streamlit web interface
│── scheduler.py        # Core scheduling logic (OR-Tools model)
│── requirements.txt    # Python dependencies
│
├── data/               # Input data
│   ├── courses.csv
│   ├── instructors.csv
│   ├── rooms.csv
│   ├── timeslots.csv
│   └── enrollments.csv
│
├── output/             # Output folder
│   └── schedule.csv    # Generated timetable

````

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/timetable_mvp.git
   cd timetable_mvp
````

2. **Create virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Linux/Mac
   venv\Scripts\activate       # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

### Option 1: Run Scheduler Script (CLI)

Generate schedule and export as CSV:

```bash
python scheduler.py
```

This will create `output/schedule.csv`.

### Option 2: Run Streamlit Web App

Launch interactive interface:

```bash
streamlit run app.py
```

* Upload/modify your CSV data in the `data/` folder.
* Click **Generate Schedule**.
* Preview and download the timetable directly.

---

## 📊 Example Output

A sample timetable might look like this:

| course\_id | course\_name | instructor\_id | room\_id | day | start | end   | enrollment |
| ---------- | ------------ | -------------- | -------- | --- | ----- | ----- | ---------- |
| C1         | Math 101     | I1             | R2       | Mon | 09:00 | 10:00 | 45         |
| C2         | Physics 201  | I2             | R1       | Tue | 11:00 | 12:00 | 35         |

---

## 🔮 Future Improvements

* Add objective functions (e.g., minimize gaps, balance room usage).
* Support soft constraints (e.g., preferred times).
* Multi-day or semester planning.
* User-uploadable data through Streamlit instead of preloaded CSVs.

---

## 👨‍💻 Tech Stack

* **Python 3**
* **Pandas** – Data handling
* **Google OR-Tools (CP-SAT)** – Constraint solving
* **Streamlit** – Web interface

---

## 🏁 Conclusion

Through this project, we:

* Learned how to model real-world scheduling as a **constraint satisfaction problem**.
* Explored **OR-Tools CP-SAT** solver for handling complex constraints.
* Built a simple yet effective interface for end users to **generate and visualize schedules**.

This MVP demonstrates the core idea and lays the foundation for more advanced timetable generation systems. 🚀

