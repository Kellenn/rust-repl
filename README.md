# rust-repl
A REPL for Rust made in Python.

This program isn't a "standard" REPL, it will not evaluate individual lines.

Instead the program will read chunks of code until an empty line is sent, then evaluate the entire chunk.

## Requirements
  - [Rust](https://www.rust-lang.org/tools/install) (duh?)
  - [Python 3.8<](https://www.python.org/downloads/)

## Example
```rust
>>> fn factorial(: u64) -> u64 {
...     match n {
...         0 | 1 => 1,
...         _ => factorial(n - 1) * n,
...     }
... }
... println!("{}", factorial(5));
...
120
```

## Help
```
git clone https://github.com/Kellenn/rust-repl
cd rust-repl
python3 . -h
```

The REPL will only display results from stdout.
