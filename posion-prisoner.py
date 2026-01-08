import math 
import argparse
import random
import sys
import time


# constraints are that bottle_number <= 2 ^ prisoner_number 

def to_fixed_binary(n: int, width: int) -> str:
    binary = str(bin(n))[2:] 
    if len(binary) > width:
        raise ValueError("Number does not fit in width")
    return '0' * (width - len(binary)) + binary

def required_prisoners(num_bottles: int)->int: 
    return math.ceil(math.log2(num_bottles))

def validate (bottles:int, prisoners:int): 
    if bottles > (1 << prisoners): 
        raise ValueError ( 
            f" Invalid configuration: {bottles} bottles require at least {required_prisoners(bottles)} prisoners"
        )
    
def encode_bottle (bottle_id:int,prisoners:int)->str: 
    return to_fixed_binary(bottle_id,prisoners)

def simulate_deaths (poisoned_bottle:int, prisoners:int)->list[int]: 
    binary = encode_bottle(poisoned_bottle,prisoners)
    return [i for i, bit in enumerate(binary)if bit =='1']

def decode_bottle(dead_prisoners:list[int], prisoners:int)->int:
    bits = ["0"]* prisoners
    for i in dead_prisoners: 
        bits[i] = "1"
    return int ("".join(bits),2) 

def run (bottles: int, prisoners: int | None, poisoned: int | None): 
    if prisoners is None: 
        prisoners = required_prisoners(bottles)

    validate(bottles, prisoners)

    if poisoned is None: 
        poisoned = random.randrange(bottles)

    dead = simulate_deaths(poisoned,prisoners)
    guessed = decode_bottle(dead,prisoners)

    return { 
        "bottles": bottles, 
        "prisoners": prisoners, 
        "poisoned": poisoned, 
        "dead_prisoners": dead, 
        "guessed": guessed, 
        "correct": poisoned==guessed
    }
    
def main (): 
    parser = argparse.ArgumentParser(description="Posioned bottle identifier using binary encoding")
    parser.add_argument('--bottles',type=int, default=1000)
    parser.add_argument('--prisoners',type=int)
    parser.add_argument('--poisoned',type=int)
    parser.add_argument('--random',action="store_true")

    args = parser.parse_args()

    poisoned = None if args.random else args.poisoned
    boot_screen() 
    try: 
        result = run(args.bottles,args.prisoners,poisoned)
        selection_sequence(result)
        feeding_sequence(result)
        waiting_sequence(result)
        visualize(result)
    except ValueError as e: 
        print(e)
        sys.exit(1)

    for k,v in result.items(): 
        print (f"{k}:{v}")
    

# ========= {{vc}} =========== #

class C:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    
ALIVE = """
    O
   ╱│╲
   ╱ ╲
"""

DEAD = """
    X
   ╱│╲
   ╱ ╲
   """

def render_prisoners(prisoners: int, dead: set[int]):
    print(C.BOLD + C.CYAN + "━" * 50 + C.RESET)
    print(C.BOLD + "  PRISONER STATUS" + C.RESET)
    print(C.CYAN + "━" * 50 + C.RESET)
    
    for row_start in range(0, prisoners, 5):
        row_end = min(row_start + 5, prisoners)
        
        for i in range(row_start, row_end):
            print(f"  P{i:02d}  ", end="")
        print()
        
        lines = [line for line in (DEAD if row_start in dead else ALIVE).split('\n') if line]
        for line_idx in range(len(lines)):
            for i in range(row_start, row_end):
                status = DEAD if i in dead else ALIVE
                color = C.RED if i in dead else C.GREEN
                line = status.split('\n')[line_idx] if line_idx < len(status.split('\n')) else ""
                print(color + f"{line:^6}" + C.RESET, end="")
            print()
        print()

def render_binary_mapping(poisoned: int, prisoners: int):
    binary = encode_bottle(poisoned, prisoners)
    print(C.BOLD + C.YELLOW + "━" * 50 + C.RESET)
    print(C.BOLD + "  🍷 POISONED BOTTLE ENCODING" + C.RESET)
    print(C.YELLOW + "━" * 50 + C.RESET)
    print(f"  Bottle ID : {C.RED}{poisoned}{C.RESET}")
    print(f"  Binary    : {C.CYAN}{' '.join(binary)}{C.RESET}")
    print(C.YELLOW + "━" * 50 + C.RESET)

def render_decoding(dead_prisoners: list[int], prisoners: int):
    bits = []
    for i in range(prisoners):
        bits.append("1" if i in dead_prisoners else "0")

    print(C.BOLD + C.GREEN + "━" * 50 + C.RESET)
    print(C.BOLD + "  🔍 DECODED RESULT" + C.RESET)
    print(C.GREEN + "━" * 50 + C.RESET)
    print(f"  Binary : {C.CYAN}{' '.join(bits)}{C.RESET}")
    print(f"  Bottle : {C.BOLD}{int(''.join(bits), 2)}{C.RESET}")
    print(C.GREEN + "━" * 50 + C.RESET)

def visualize(result: dict):
    dead = set(result["dead_prisoners"])
    
    print()
    render_binary_mapping(result["poisoned"], result["prisoners"])
    print()
    render_prisoners(result["prisoners"], dead)
    print()
    render_decoding(result["dead_prisoners"], result["prisoners"])
    print()
    
    if result["correct"]:
        print(C.GREEN + C.BOLD + "  ✓ SUCCESS! Poisoned bottle identified correctly!" + C.RESET)
    else:
        print(C.RED + C.BOLD + "  ✗ FAILED! Something went wrong." + C.RESET)
    print()
    print()
    print()
    print()

def selection_sequence(result: dict):
    print(C.YELLOW + C.BOLD + "\n📦 BOTTLE SELECTION PHASE" + C.RESET)
    print(C.DIM + "━" * 50 + C.RESET)
    pause(1.0)
    
    print(C.DIM + "  Scanning wine cellar..." + C.RESET)
    for i in range(3):
        pause(0.4)
        print(C.DIM + f"  🍷 Bottles checked: {random.randint(1, result['bottles'])}" + C.RESET, end='\r')
    print()
    pause(0.8)
    
    print(C.RED + C.BOLD + f"\n  ☠️  POISON DETECTED in Bottle #{result['poisoned']}" + C.RESET)
    pause(1.2)
    print(C.DIM + f"  Binary signature: {encode_bottle(result['poisoned'], result['prisoners'])}" + C.RESET)
    pause(1.0)

def feeding_sequence(result: dict):
    print(C.MAGENTA + C.BOLD + "\n🍷 FEEDING PHASE" + C.RESET)
    print(C.DIM + "━" * 50 + C.RESET)
    pause(1.0)
    
    binary = encode_bottle(result['poisoned'], result['prisoners'])
    
    print(C.DIM + "  Preparing wine samples according to binary protocol..." + C.RESET)
    pause(1.2)
    
    for i in range(result['prisoners']):
        bit = binary[i]
        if bit == '1':
            print(C.YELLOW + f"  ➜ Prisoner {i:02d}: " + C.RED + "RECEIVES wine sample" + C.RESET)
        else:
            print(C.DIM + f"  ➜ Prisoner {i:02d}: no sample (control group)" + C.RESET)
        pause(0.5)
    
    pause(1.0)
    print(C.DIM + "\n  All samples administered." + C.RESET)
    pause(0.8)

def waiting_sequence(result: dict):
    print(C.CYAN + C.BOLD + "\n⏳ OBSERVATION PERIOD" + C.RESET)
    print(C.DIM + "━" * 50 + C.RESET)
    pause(1.0)
    
    print(C.DIM + "  Monitoring subjects for symptoms..." + C.RESET)
    pause(1.5)
    
    stages = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(12):
        for stage in stages:
            print(C.CYAN + f"  {stage} Waiting..." + C.RESET, end='\r')
            pause(0.15)
    print()
    
    pause(1.0)
    print(C.RED + C.BOLD + "\n  ⚠️  CASUALTIES DETECTED" + C.RESET)
    pause(1.2)
    
    dead = result['dead_prisoners']
    if dead:
        for prisoner_id in dead:
            print(C.RED + f"  ✝ Prisoner {prisoner_id:02d} has perished" + C.RESET)
            pause(0.6)
    else:
        print(C.GREEN + "  ✓ No casualties - poison bottle was #0 (all zeros)" + C.RESET)
    
    pause(1.5)

def pause(sec=0.8):
    time.sleep(sec)

def boot_screen():
    print(C.CYAN + C.BOLD + TITLE + C.RESET)
    print(C.DIM + SUBTITLE + C.RESET)
    pause(1.5)
    print(C.DIM + "🔧 Initializing experiment protocol..." + C.RESET)
    pause(1.2)
    print(C.DIM + "👥 Assembling test subjects..." + C.RESET)
    for i in range(3):
        pause(0.5)
        print(C.DIM + "   ." * (i + 1) + C.RESET)
    pause(1.0)
    print(C.GREEN + "   ✓ Prisoners ready" + C.RESET)
    pause(0.8)
    print(C.DIM + "🍷 Preparing wine bottles..." + C.RESET)
    pause(1.2)
    print(C.GREEN + "   ✓ Wine cellar accessible" + C.RESET)
    pause(1.0)


TITLE = r"""



██████╗  ██████╗ ██╗███████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔═══██╗██║██╔════╝██╔═══██╗████╗  ██║
██████╔╝██║   ██║██║███████╗██║   ██║██╔██╗ ██║
██╔═══╝ ██║   ██║██║╚════██║██║   ██║██║╚██╗██║
██║     ╚██████╔╝██║███████║╚██████╔╝██║ ╚████║
╚═╝      ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝

      Binary Poisoned Bottle Identification
"""

SUBTITLE = """
      🍷 1000 bottles  |  ☠️  1 poison
      🔢 Binary encoding  |  📊 Information theory
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


if __name__ == "__main__": 
    main()