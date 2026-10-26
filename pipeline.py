import subprocess
from dotenv import load_dotenv

load_dotenv()  

print("beginning job tracker pipeline execution")

subprocess.run(["python", "src/extract.py"], check=True)
subprocess.run(["python", "src/load.py"], check=True)
subprocess.run(["dbt", "run", "--project-dir", "dbt", "--profiles-dir", "dbt"], check=True)
subprocess.run(["dbt", "test", "--project-dir", "dbt", "--profiles-dir", "dbt"], check=True)

print("job tracker pipeline execution completed successfully")