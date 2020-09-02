from app import Bracket
import sys

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        year = 19
        print('asdfjkl;')
    else:
        try:
            year = int(sys.argv[1])
            assert year >= 15 and year <= 20
            print('bruh')
        except:
            year = 19
            print('dood')

    Bracket(width=1200, height=600, year=year).run()
