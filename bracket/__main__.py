from app import Bracket
import sys

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        year = 19
    else:
        try:
            year = int(sys.argv[1])
            assert year >= 15 and year <= 20
        except:
            year = 19

    Bracket(width=1200, height=600, year=year).run()
