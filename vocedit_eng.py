from vocedit import *
import sys

if __name__ == '__main__':
	init_e()
	flist = sys.argv[1:]

	set_debug_level = 0
	if len(sys.argv) <= 1:
		log(0, "Pass1")
		flist = [ "default.jpg" ]
	elif len(sys.argv) >= 3 and sys.argv[len(sys.argv) - 1].startswith("-g") and len(sys.argv[len(sys.argv) - 1]) >= 2:
		set_debug_level = int(sys.argv[len(sys.argv) - 1][2:])
		flist = flist[:-1]

	log(1, flist)
	VocEditor(flist)

	mainloop()

