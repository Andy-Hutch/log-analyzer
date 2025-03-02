def parse_log_file(log_file):
    patterns = {
        "ERROR": ["level: error", "level: critical"],
        "WARNING": ["level: warning"],
        "FAILED LOGIN": ["failed login", "invalid credentials", "unauthorized access"]
    }
    
    findings = {key: [] for key in patterns}
    current_event = []  # Initialize the current event list

    # Open and read the file
    with open(log_file, "r", encoding="latin-1") as file:
        for line in file:
            line = line.strip()  
            print(f"Processing line: {line}")  # Debugging output

            if line:  # Ignore empty lines
                current_event.append(line)  

            # Check if it's the end of an event (modify condition if needed)
            if line.startswith("Report Id:") or line.startswith("Event["):
                if current_event:
                    event_text = "\n".join(current_event).lower()  # Convert to lowercase
                    print(f"\nProcessing Event:\n{event_text}")  # Debugging output
                    for key, triggers in patterns.items():
                        if any(trigger in event_text for trigger in triggers):
                            findings[key].append(event_text)
                            print(f"Match found in category: {key}")  # Debugging output
                    current_event = []  # Reset for next event

    # Process the last event if needed
    if current_event:
        event_text = "\n".join(current_event).lower()
        print(f"\nCaptured Event:\n{event_text}")
        for key, triggers in patterns.items():
            if any(trigger in event_text for trigger in triggers):
                findings[key].append(event_text)
                print(f"Match found in category: {key}")  # Debugging output

    return findings

def generate_report(findings, report_file="log_analysis_report.txt"):
    with open(report_file, "w") as file:
        for category, logs in findings.items():
            file.write(f"\n--- {category} ---\n")
            for log in logs:
                file.write(f"\n{log}\n")
                file.write("-" * 50 + "\n")

    print(f"Report generated: {report_file}")

if __name__ == "__main__":
    log_path = "C:\\Users\\proud\\OneDrive\\Desktop\\Python scripts\\sample.log"  # Update to sample.log
    findings = parse_log_file(log_path)

    if not any(findings.values()):
        print("No matching logs found. Try adjusting search keywords.")
    else:
        generate_report(findings)
