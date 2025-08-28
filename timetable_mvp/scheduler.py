"""
Simple Course Timetable Generator (MVP)
- Callable generate_schedule() for Streamlit
"""
import pandas as pd
from itertools import combinations
from ortools.sat.python import cp_model

def generate_schedule(courses, rooms, instr, slots, enroll):
    # Compute enrollment per course from enrollments
    enrollment_counts = enroll.groupby("course_id")["student_id"].nunique().to_dict()

    # Map helpers
    course_ids = courses["course_id"].tolist()
    room_ids   = rooms["room_id"].tolist()
    slot_ids   = slots["slot_id"].tolist()

    # Instructor availability
    inst_avail = {row["instructor_id"]: set(str(row["available_slots"]).split("|")) 
                  for _, row in instr.iterrows()}

    # Which instructor teaches which course
    course_instructor = {row["course_id"]: row["instructor_id"] for _, row in courses.iterrows()}

    # Students in each course
    students_in_course = {c: set(enroll[enroll["course_id"] == c]["student_id"].tolist())
                          for c in course_ids}

    # For capacity filtering
    room_capacity = {row["room_id"]: int(row["capacity"]) for _, row in rooms.iterrows()}

    # ---- Build model ----
    model = cp_model.CpModel()

    # Decision variables x[c,t,r] = 1 if course c is scheduled at timeslot t in room r
    x = {}
    for c in course_ids:
        for t in slot_ids:
            # course c allowed at t only if instructor is available at t
            if t not in inst_avail[course_instructor[c]]:
                continue
            for r in room_ids:
                # room must satisfy capacity
                if room_capacity[r] < enrollment_counts.get(c, 0):
                    continue
                x[(c,t,r)] = model.NewBoolVar(f"x_{c}_{t}_{r}")

    # Each course must be assigned exactly one (t,r)
    for c in course_ids:
        vars_ctr = [x[(c,t,r)] for (c2,t,r) in x.keys() if c2 == c]
        if not vars_ctr:
            dummy = model.NewBoolVar(f"dummy_{c}")
            model.Add(dummy == 1)
            model.Add(dummy == 0)
        else:
            model.Add(sum(vars_ctr) == 1)

    # No room double-booking at the same time
    for t in slot_ids:
        for r in room_ids:
            vars_ctr = [x[(c,t,r)] for (c,t2,r2) in x.keys() if t2==t and r2==r and (c,t,r) in x]
            if vars_ctr:
                model.Add(sum(vars_ctr) <= 1)

    # No instructor teaching two courses at the same time
    for t in slot_ids:
        for inst_id in instr["instructor_id"].tolist():
            vars_ctr = [x[(c,t,r)] for (c,t2,r) in x.keys()
                        if t2==t and course_instructor[c] == inst_id and (c,t,r) in x]
            if vars_ctr:
                model.Add(sum(vars_ctr) <= 1)

    # No student conflicts
    for c1, c2 in combinations(course_ids, 2):
        if students_in_course[c1].intersection(students_in_course[c2]):
            for t in slot_ids:
                lhs = []
                for r in room_ids:
                    if (c1,t,r) in x: lhs.append(x[(c1,t,r)])
                    if (c2,t,r) in x: lhs.append(x[(c2,t,r)])
                if lhs:
                    model.Add(sum(lhs) <= 1)

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError("No feasible schedule found. Check availability, room capacity, or increase slots/rooms.")

    # Extract solution
    rows = []
    for (c,t,r), var in x.items():
        if solver.Value(var) == 1:
            course_name = courses.loc[courses["course_id"]==c, "course_name"].iloc[0]
            inst_id = course_instructor[c]
            day = slots.loc[slots["slot_id"]==t, "day"].iloc[0]
            start = slots.loc[slots["slot_id"]==t, "start"].iloc[0]
            end = slots.loc[slots["slot_id"]==t, "end"].iloc[0]
            rows.append({
                "course_id": c,
                "course_name": course_name,
                "instructor_id": inst_id,
                "room_id": r,
                "slot_id": t,
                "day": day,
                "start": start,
                "end": end,
                "enrollment": enrollment_counts.get(c, 0)
            })

    schedule_df = pd.DataFrame(rows).sort_values(["day","start","room_id"]).reset_index(drop=True)
    return schedule_df
