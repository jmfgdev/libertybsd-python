#!/usr/bin/env python3

"""
Name: libdeblob.py
Main: JimmyBot(jmfgdev)
Lisc: GPLV3
Desc: Functions to be
      used for deblobbing
      and rebranding OBSD
      sources for the LBSD
      project.
"""

# Turns a file and it's path into a friendly filename
# Usage: filetize $filepath
def filetize(): 
	system("echo "%s" | sed 's|/|\^|g'") % (sys.argv[1])

# Vice-versa, clearly.
# Usage: unfiletize $filetizedpath
def unfiletize(): 
	system("echo "%s" | sed 's|\^|/|g'") % (sys.argv[1])

# Prints $1 number of spaces.
# Usage: space $number
def space(): 
	typeset -i i=0
	while [ $i != sys.argv[1] ]
	do
		sys.stdout.write(" ")
		i=i+1
	done

# Replace a string in a file
# Usage: rep $replacee $replacer $file
def rep():
	local file_ft = "$(filetize "$3")"
	if [ -e "$PATCH_DIR/$file_ft" ]
	then
		sed 's^'"$1"'^'"$2"'^g' "$PATCH_DIR/$file_ft" > "$PATCH_DIR/$file_ft.tmp"
		mv "$PATCH_DIR/$file_ft.tmp" "$PATCH_DIR/$file_ft"
		diff "$SRC_DIR/$3" "$PATCH_DIR/$file_ft" > "$PATCH_DIR/$file_ft.patch"
	else
		sed 's^'"$1"'^'"$2"'^g' "$SRC_DIR/$3" > "$PATCH_DIR/$file_ft"
		diff "$SRC_DIR/$3" "$PATCH_DIR/$file_ft" > "$PATCH_DIR/$file_ft.patch"
	fi

# Delete a string in a file
# Usage: strdel $string $file
def strdel():
	rep "$1" "" $2

# Inserts a new line after another
# Usage: lineadd $string $newline $file
def lineadd(): 
	local file_ft="$(filetize "$3")"
	if [ -e "$PATCH_DIR/$file_ft" ]
	then
		sed 's^'"$1"'^'"$1"' \
'"$2"'^' "$PATCH_DIR/$file_ft" > "$PATCH_DIR/$file_ft.tmp"
		mv "$PATCH_DIR/$file_ft.tmp" "$PATCH_DIR/$file_ft"
		diff "$SRC_DIR/$3" "$PATCH_DIR/$file_ft" > "$PATCH_DIR/$file_ft.patch"
	else
		sed 's^'"$1"'^'"$1"' \
'"$2"'^' "$SRC_DIR/$3" > "$PATCH_DIR/$file_ft"
		diff "$SRC_DIR/$3" "$PATCH_DIR/$file_ft" > "$PATCH_DIR/$file_ft.patch"
	fi

# Removes a line.
# Usage linedel $string $file
def linedel(): 
	local file_ft="$(filetize "$2")"
	if [ -e "$PATCH_DIR/$file_ft" ]
	then
		grep -v "$1" "$PATCH_DIR/$file_ft" > "$PATCH_DIR/$file_ft.tmp"
		mv "$PATCH_DIR/$file_ft.tmp" "$PATCH_DIR/$file_ft"
		diff "$SRC_DIR/$2" "$PATCH_DIR/$file_ft" > "$PATCH_DIR/$file_ft.patch"
	else
		echo otherwise
		grep -v "$1" "$SRC_DIR/$2" > "$PATCH_DIR/$file_ft"
		diff "$SRC_DIR/$2" "$PATCH_DIR/$file_ft" > "$PATCH_DIR/$file_ft.patch"
		echo otherhell
	fi

# "Copies" a dir
# Usage: dircp $file $dest
def dircp(): 
	if echo "$1" | grep -q "^files/"
	then
		echo "FILES"
		cp -r "$1" "$PATCH_DIR/ADD_$(filetize "$2")"
	else
		echo "NO FILES"
		cp -r "$SRC_DIR/$1" "$PATCH_DIR/ADD_$(filetize "$2")"
	fi

# "Copies" a file
# Usage: filecp $file $dest
def filecp(): 
	if echo "$1" | grep -q "^files/"
	then
		echo "FILES"
		cp "$1" "$PATCH_DIR/ADD_$(filetize "$2")"
	else
		echo "FILES"
		cp "$SRC_DIR/$1" "$PATCH_DIR/ADD_$(filetize "$2")"
	fi

# "Deletes" a file
# Usage: filedel $file
def filedel(): 
	echo "$PATCH_DIR $1"
	touch "$PATCH_DIR/RM_$(filetize "$1")"

# Applies patches.
def apply(): 
	local file

	for file in "$PATCH_DIR"/*
	do
		local realname_prefixed="$(unfiletize "$(basename "$file")")"

		if echo "$realname_prefixed" | grep -q "^RM_"
		then
			realname="${realname_prefixed#RM_}"
			echo "Deleting $realname..."
			if rm -rf "$SRC_DIR/$realname"
			then
				echo "$realname deleted" >> apply.log
				echo "$realname deleted"
			else
				echo "!!! $realname NOT deleted" >> apply.log
				echo "!!! $realname NOT deleted"
			fi
		elif echo "$file" | grep -q "ADD_"
		then
			realname="${realname_prefixed#ADD_}"
			echo "Copying $file to $realname..."
			if cp -r "$file" "$SRC_DIR/$realname"
			then
				echo "$realname copied from $file" >> apply.log
			else
				echo "!!! $realname NOT copied from $file" >> apply.log
			fi
		elif echo "$file" | grep -q ".patch$"
		then
			realname="$realname_prefixed"
			if patch "$SRC_DIR/${realname%.patch}" < "$file"
			then
				echo "$SRC_DIR/${realname%.patch} patched from $file" >> apply.log
			else
				echo "!!! $SRC_DIR/${realname%.patch} NOT patched from $file" \
					>> apply.log
			fi
		fi
	done

def self_destruct_sequence(): 
	print("%s will be deleted in three seconds.") % (sys.argv[1])
	print("CTRL-C now to avoid this fate!")
	print("3") 
	sleep(1)
	print("2") 
	sleep(1)
	print("1")
	sleep(1)
	print("0\nDestruction!")
	system("rm -rf %s") % (sys.argv[1])
