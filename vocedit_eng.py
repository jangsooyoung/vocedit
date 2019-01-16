from vocedit import *
import sys

if __name__ == '__main__':
	init_e()
	if len(sys.argv) <= 1:
		print("python3  vocedit.py image_list [-g0]")
		sys.exit(-1)

	flist = sys.argv[1:]
	set_debug_level = 0
	if len(sys.argv) >= 3 and sys.argv[len(sys.argv) - 1].startswith("-g") and len(sys.argv[len(sys.argv) - 1]) >= 2:
		set_debug_level = int(sys.argv[len(sys.argv) - 1][2:])
		flist = flist[:-1]

	log(1, flist)
	VocEditor(flist)

	mainloop()


