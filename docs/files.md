## POSIX Files

This is just a short note about the POSIX files API, and it doesn't cover all of
the details.

There are 5 operations implemented by the kernel: open, close, read, write,
seek. These are made available to userspace via syscalls.

Each process has a list of open files, which might look something like:
<pre>struct file {
    int f_type;     // type (regular file? device file?)
    int f_flags;    // flags provided at open()
    int f_pos;      // current position in file, set by lseek()
    int f_inode;    // inode number of open regular file
    ... additional fields (e.g. if device file, the dev ID)
};

struct task {
    // process fields
    ...
    file** file_list;   // pointers to objects in a kmem_cache for file structs
    ...
};</pre>

File descriptors are integers referring to an open file, and can be thought of
as indices into the running process' file list. open returns a file descriptor,
close/read/write/seek takes one. The C library's fopen/fclose/fread/fwrite/fseek
are abstractions of this interface, and pass around FILE structs, whose contents
are implementation-defined but contain at minimum a file descriptor.

The open() operation takes various flags bitwise OR'd together in an argument,
the key ones being:

* **O_RDONLY** - can only be read

* **O_WRONLY** - can only be written

* **O_RDWR** - can be read or written

* **O_CREAT** - create file if it doesn't exist, or open if it does

* **O_EXCL** - if O_CREAT and the file exists, open() fails

* **O_TRUNC** - truncate file to size 0 when opened

* **O_APPEND** - before each write(), set f_pos to length of the file (1 past EOF)

Note that **(O_RDONLY | O_WRONLY) != O_RDWR** on _most_ Unix-likes; each flag is
defined as a unique bit. You must provide only 1 of the first 3 flags listed
above when opening a file.

Writing past the end of a file first expands the file. Reading past the end of a
file reads back zeroes but doesn't affect file size.

O_EXCL is necessary to avoid race conditions where you might try opening a file
multiple times concurrently, and overwrite contents without noticing (especially
if O_TRUNC is specified). open() acts atomically and performs that "file already
exists" check that a multithreaded program may desire to do as part of a single
operation.
