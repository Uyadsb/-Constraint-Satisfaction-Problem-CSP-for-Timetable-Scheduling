import copy

# ==========================================
# 1. DEFINE THE DOMAIN (23 Slots)
# ==========================================
days = {"Sun": 5, "Mon": 5, "Tue": 3, "Wed": 5, "Thu": 5}
base_domain = [(day, slot) for day, slots in days.items() for slot in range(1, slots + 1)]

# ==========================================
# 2. DEFINE VARIABLES & THEIR REQUIREMENTS
# ==========================================
variables = {
    # Sécurité (Teacher 1)
    "Securite_Lec": {"groups": ["G1", "G2", "G3"], "teacher": "T1"},
    "Securite_TD_G1": {"groups": ["G1"], "teacher": "T1"},
    "Securite_TD_G2": {"groups": ["G2"], "teacher": "T1"},
    "Securite_TD_G3": {"groups": ["G3"], "teacher": "T1"},

    # Méthodes Formelles (Teacher 2)
    "Formelles_Lec": {"groups": ["G1", "G2", "G3"], "teacher": "T2"},
    "Formelles_TD_G1": {"groups": ["G1"], "teacher": "T2"},
    "Formelles_TD_G2": {"groups": ["G2"], "teacher": "T2"},
    "Formelles_TD_G3": {"groups": ["G3"], "teacher": "T2"},

    # Analyse Numérique (Teacher 3)
    "Analyse_Lec": {"groups": ["G1", "G2", "G3"], "teacher": "T3"},
    "Analyse_TD_G1": {"groups": ["G1"], "teacher": "T3"},
    "Analyse_TD_G2": {"groups": ["G2"], "teacher": "T3"},
    "Analyse_TD_G3": {"groups": ["G3"], "teacher": "T3"},

    # Entrepreneuriat (Teacher 4) - Lecture Only
    "Entrepreneuriat_Lec": {"groups": ["G1", "G2", "G3"], "teacher": "T4"},

    # Recherche Opérationnelle 2 (Teacher 5)
    "RO2_Lec": {"groups": ["G1", "G2", "G3"], "teacher": "T5"},
    "RO2_TD_G1": {"groups": ["G1"], "teacher": "T5"},
    "RO2_TD_G2": {"groups": ["G2"], "teacher": "T5"},
    "RO2_TD_G3": {"groups": ["G3"], "teacher": "T5"},

    # Distributed Architecture & Intensive Computing (Teacher 6)
    "DAIC_Lec": {"groups": ["G1", "G2", "G3"], "teacher": "T6"},
    "DAIC_TD_G1": {"groups": ["G1"], "teacher": "T6"},
    "DAIC_TD_G2": {"groups": ["G2"], "teacher": "T6"},
    "DAIC_TD_G3": {"groups": ["G3"], "teacher": "T6"},

    # Réseaux 2 (Teacher 7 + Teachers 8-9)
    "Reseaux2_Lec": {"groups": ["G1", "G2", "G3"], "teacher": "T7"},
    "Reseaux2_TD_G1": {"groups": ["G1"], "teacher": "T8"},
    "Reseaux2_TD_G2": {"groups": ["G2"], "teacher": "T8"},
    "Reseaux2_TD_G3": {"groups": ["G3"], "teacher": "T8"},
    "Reseaux2_TP_G1": {"groups": ["G1"], "teacher": "T9"},
    "Reseaux2_TP_G2": {"groups": ["G2"], "teacher": "T9"},
    "Reseaux2_TP_G3": {"groups": ["G3"], "teacher": "T9"},

    # Artificial Intelligence (Teacher 10 + Teachers 11-12)
    "AI_Lec": {"groups": ["G1", "G2", "G3"], "teacher": "T10"},
    "AI_TD_G1": {"groups": ["G1"], "teacher": "T11"},
    "AI_TD_G2": {"groups": ["G2"], "teacher": "T11"},
    "AI_TD_G3": {"groups": ["G3"], "teacher": "T11"},
    "AI_TP_G1": {"groups": ["G1"], "teacher": "T12"},
    "AI_TP_G2": {"groups": ["G2"], "teacher": "T12"},
    "AI_TP_G3": {"groups": ["G3"], "teacher": "T12"}
}

# Initialize domains for all variables
domains = {var: copy.deepcopy(base_domain) for var in variables}

# ==========================================
# 3. CONSTRAINT CHECKING FUNCTIONS
# ==========================================
def is_valid(assignment, var, value):
    """Checks Hard Constraints: Overlaps, Max 3 Consecutive, and Max 2 Lectures per day"""
    var_info = variables[var]
    day, slot = value
    
    # Track consecutive classes for each group involved
    consecutive_counts = {g: 1 for g in var_info["groups"]} 
    
    # Track the number of lectures per day for each group
    is_lecture = "Lec" in var
    lecture_counts = {g: (1 if is_lecture else 0) for g in var_info["groups"]}

    for assigned_var, assigned_val in assignment.items():
        assigned_day, assigned_slot = assigned_val
        assigned_info = variables[assigned_var]

        # Check overlapping constraints (Same time slot)
        if assigned_val == value:
            # Rule 1: No two sessions for same group at same time
            if any(g in assigned_info["groups"] for g in var_info["groups"]):
                return False
            # Rule 2: Teacher cannot teach two sessions at same time
            if var_info["teacher"] == assigned_info["teacher"]:
                return False
        
        # Check daily limits (Same day)
        if assigned_day == day:
            for g in var_info["groups"]:
                if g in assigned_info["groups"]:
                    
                    # Rule 3: Max 3 consecutive sessions per day
                    if abs(assigned_slot - slot) <= 3: 
                        consecutive_counts[g] += 1
                        if consecutive_counts[g] > 3:
                            return False
                    
                    # Rule 4: Max 2 Lectures per day
                    if "Lec" in assigned_var:
                        lecture_counts[g] += 1
                        if lecture_counts[g] > 2:
                            return False 
                            
    return True

# ==========================================
# 4. AC-3 ALGORITHM (Arc Consistency)
# ==========================================
def ac3(domains, assignment):
    """Prunes domains of unassigned variables based on current assignments"""
    for assigned_var, assigned_val in assignment.items():
        assigned_info = variables[assigned_var]
        
        for unassigned_var in domains:
            if unassigned_var not in assignment:
                unassigned_info = variables[unassigned_var]
                
                # If they share a teacher or a group, remove the occupied time slot
                shares_teacher = assigned_info["teacher"] == unassigned_info["teacher"]
                shares_group = any(g in assigned_info["groups"] for g in unassigned_info["groups"])
                
                if shares_teacher or shares_group:
                    if assigned_val in domains[unassigned_var]:
                        domains[unassigned_var].remove(assigned_val)
                        # If a domain becomes empty, this path fails
                        if len(domains[unassigned_var]) == 0:
                            return False 
    return True

# ==========================================
# 5. HEURISTICS (MRV & Degree)
# ==========================================
def select_unassigned_variable(assignment, domains):
    unassigned = [v for v in variables if v not in assignment]
    
    # MRV: Sort by the length of their remaining domain (fewest first)
    unassigned.sort(key=lambda var: len(domains[var]))
    min_domain_size = len(domains[unassigned[0]])
    mrv_ties = [v for v in unassigned if len(domains[v]) == min_domain_size]
    
    # Degree Heuristic: Break ties by picking the variable with the most groups
    if len(mrv_ties) > 1:
        mrv_ties.sort(key=lambda var: len(variables[var]["groups"]), reverse=True)
        
    return mrv_ties[0]

# ==========================================
# 6. BACKTRACKING SEARCH
# ==========================================
def backtrack(assignment, domains):
    # Base case: If all variables are assigned, we are done!
    if len(assignment) == len(variables):
        return assignment
    
    # Pick the next variable to schedule
    var = select_unassigned_variable(assignment, domains)
    
    for value in domains[var]:
        if is_valid(assignment, var, value):
            assignment[var] = value
            
            # Deep copy domains so we can undo AC-3 if this branch fails
            domains_copy = copy.deepcopy(domains)
            
            # Run AC-3 to prune future domains
            if ac3(domains_copy, assignment):
                result = backtrack(assignment, domains_copy)
                if result:
                    return result
            
            # If it failed, backtrack
            del assignment[var]
            
    return None

# ==========================================
# 7. RUN THE SOLVER & DISPLAY RESULTS
# ==========================================
print("Generating Timetable... Please wait (this may take a moment)...")
final_timetable = backtrack({}, domains)

if final_timetable:
    print("\n=== FINAL GENERATED TIMETABLE ===")
    
    days_list = ["Sun", "Mon", "Tue", "Wed", "Thu"]
    groups = ["G1", "G2", "G3"]
    col_w = 20 # Width of each box
    
    # Generate a separate table for each group
    for current_group in groups:
        print(f"\n" + "="*88)
        print(f"                                SCHEDULE FOR GROUP {current_group}")
        print("="*88)
        
        # Create an empty 5x5 grid for this specific group
        schedule = {slot: {day: "" for day in days_list} for slot in range(1, 6)}
        
        for var, time in final_timetable.items():
            day, slot = time
            if current_group in variables[var]["groups"]:
                course = var.split('_')[0]
                c_type = "Lec" if "Lec" in var else ("TD" if "TD" in var else "TP")
                teacher = variables[var]["teacher"]
                schedule[slot][day] = f"{course} {c_type} ({teacher})"
        
        header = f"| {'Slot':<5} | {'Sunday':<{col_w}} | {'Monday':<{col_w}} | {'Tuesday':<{col_w}} | {'Wednesday':<{col_w}} | {'Thursday':<{col_w}} |"
        separator = "-" * len(header)
        
        print(separator)
        print(header)
        print(separator)
        
        for slot in range(1, 6):
            row_str = f"| {slot:<5} |"
            
            for day in days_list:
                if day == "Tue" and slot > 3:
                    cell_text = "BLOCKED" 
                else:
                    cell_text = schedule[slot][day]
                
                row_str += f" {cell_text:<{col_w}} |"
                
            print(row_str)
            print(separator) 

else:
    print("No valid timetable could be found with these constraints.")