import json
from datetime import date

def main():
    jobs = []
    
    filename = f"raw/jobs_{date.today()}.json"
    with open (filename, "w") as f:
        json.dump(jobs, f)
        
    print(f"Saved {len(jobs)} jobs to {filename}")
    
def lambda_handler(event, context):
    main()
    
if __name__ == "__main__":
    main()