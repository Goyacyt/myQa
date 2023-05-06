import argparse

parser=argparse.ArgumentParser(description="input MR type")

parser.add_argument("--mr",default=1,help="MR type")
parser.add_argument("--module",default="allenai/unifiedqa-t5-base",help="choose between allenai/unifiedqa-t5-large or\
                    t5-base or t5-3b")


args=parser.parse_args()

if __name__=='__main__':
    print()