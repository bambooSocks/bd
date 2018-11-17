# > Menu item 1
#   Menu item 2
#   Menu item 3
#   Menu item 4

import sys
import termios
import tty
import time

# https://stackoverflow.com/questions/22397289/finding-the-values-of-the-arrow-keys-in-python-why-are-they-triples
def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(3)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def showMenu(menu_items):
	current = 0
	while True:
		sys.stdout.write("\x1b[1J")

		menu = ""
		for idx, mi in enumerate(menu_items):
			menu += ("> " if idx == current else "  ") + mi + "\n"
		
		sys.stdout.write(menu)
		sys.stdout.flush()

		# wait for arrow input or Enter
		k = getch()
		if k == '': break
		if k == '\x1b[A' and current > 0:
			current -= 1
		elif k == '\x1b[B' and current < len(menu_items)-1:
			current += 1
		elif k == '\x1b[C':
			return current

		
		# sys.stdout.write("\x1b[F")
		# sys.stdout.write("\x1b[F")
		# sys.stdout.write("\x1b[F")

def clearLines(lines):
	for _ in range(lines):
		sys.stdout.write(" " * 50 + "\n")
	for _ in range(lines):
		sys.stdout.write("\x1b[F")


m = showMenu(["test1","test2","test3","test4"])
print("chosen:", m)
# clearLines(4)
m = showMenu(["1","2","3","4"])
print("chosen:", m)