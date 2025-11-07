## Use GDB

1. `tmux` This ensures your codespace terminal could run gdb
2. `gdb ./format-me` start gdb
3. `break xxx` You can set the breakpoint by this command
4. `run` run to the breakpoint
5. `n` run step by step
6. If you want to print a var value, please use `p var_name`, if you want to print a var value in hex, please use `p/x var_name`
7. If you want to see current stack frame, use `backtrace`, to switch to current stack frame, use `frame [frame_name]`
8. See stack, `x/20gx $rsp`
9. 