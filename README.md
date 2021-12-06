# rust-repl
A REPL for Rust made in Python because why not?

This program isn't a "standard" REPL, it will not evaluate individual lines.

Instead the program will read chunks of code until an empty line is sent, then evaluate that entire chunk.

Additionaly, this program will not retain the same scope as previous executions.

## Requirements
  - [Rust](https://www.rust-lang.org/tools/install) (duh?)
  - [Python 3.7<](https://www.python.org/downloads/)

## Example
```rust
>>> fn factorial(n: u64) -> u64 {
...     match n {
...         0 | 1 => 1,
...         _ => factorial(n - 1) * n,
...     }
... }
... println!("{}", factorial(5));
...
120
```

## Installing & Running
```
git clone https://github.com/Kellenn/rust-repl
cd rust-repl
python3 . -h
```

The REPL will only display results from stdout.
