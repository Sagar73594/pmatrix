import curses
import optparse
import random
import string
import time

COLOR = curses.COLOR_GREEN
COLORS = {
	"BLUE" : curses.COLOR_BLUE,
	"CYAN" : curses.COLOR_CYAN,
	"GREEN" : curses.COLOR_GREEN,
	"MAGENTA" : curses.COLOR_MAGENTA,
	"RED" : curses.COLOR_RED,
	"WHITE" : curses.COLOR_WHITE,
	"YELLOW" : curses.COLOR_YELLOW,
}

LETTERS_PER_UPDATE = 2
UPDATE_DELAY = 0.03
rand_string = lambda c, l: "".join(random.choice(c) for i in xrange(l))

def main(stdscr):
	curses.curs_set(0)
	curses.init_pair(9, COLOR, curses.COLOR_BLACK)
	curses.start_color()

	back = [rand_string(string.printable.strip(), curses.COLS) for i in xrange(curses.LINES)]
	dispense = []
	visible = []
	
	while 1:
		stdscr.clear()

		for i in xrange(LETTERS_PER_UPDATE):
			dispense.append([0, random.randint(0, curses.COLS - 1)])

		for i, c in enumerate(dispense):
			# here we copy the list with [:]. otherwise, we can't
			# delete from dispense without deleting from visible
			# (python reference problems)
			visible.append(c[:])
			if not random.randint(0, 5):
				del dispense[i]

		for i, c in enumerate(visible):
			if c[0] < curses.LINES - 1:
				stdscr.addstr(c[0], c[1], back[c[0]][c[1]], curses.color_pair(9))
				c[0] += 1
			else:
				# can't use del obj since it's not a reference to the
				# list, but instead a copy. we have to delete by index.
				del visible[i]

		stdscr.refresh()
		time.sleep(UPDATE_DELAY)

def start():
	parser = optparse.OptionParser()
	parser.add_option("-c", "--color", default="green",
			help="The colour of the falling text.")
	parser.add_option("-d", "--delay", type=float, default=0.03,
			help="The update delay.")
	parser.add_option("-l", "--letters", type=int, default=2,
			help="The number of letters produced per update.")
	options, args = parser.parse_args()

	global COLOR, LETTERS_PER_UPDATE, UPDATE_DELAY
	COLOR = COLORS.get(options.color.upper(), curses.COLOR_GREEN)
	LETTERS_PER_UPDATE = abs(options.letters)
	UPDATE_DELAY = abs(options.delay)

	try:
		curses.wrapper(main)
	except KeyboardInterrupt:
		exit(0)

if __name__ == "__main__":
	start()
