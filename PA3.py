import sys
from program import Program

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <credentials_file> <patients_file>")
        sys.exit(1)
    program = Program(sys.argv[1], sys.argv[2])
    program.start()
