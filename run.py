from pathlib import Path
import sys
import uvicorn

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    print("\n" + "=" * 68)
    print("ASTRORISK // NASA NEOWS ANALYTICS")
    print("Developer: Eva J. Patel")
    print("=" * 68)
    print("Dashboard : http://127.0.0.1:8000")
    print("Research  : http://127.0.0.1:8000/lab")
    print("API docs  : http://127.0.0.1:8000/docs")
    print("=" * 68 + "\n")

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
