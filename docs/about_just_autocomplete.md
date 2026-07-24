# Shell Completion for `just`

`just` can generate completion scripts for Bash, Zsh, Fish, PowerShell,
Elvish, and Nushell. Completion suggests `just` options, variables, groups,
and recipes from the current `justfile`.

Before configuring completion, make sure `just` is installed and available in
`PATH`:

```sh
just --version
```

Some package managers install completion scripts automatically. If completion
already works after restarting your shell, no additional configuration is
needed.

## Bash

The recommended setup uses the `bash-completion` package and lazy-loads the
generated script:

```bash
mkdir -p ~/.local/share/bash-completion/completions
just --completions bash > ~/.local/share/bash-completion/completions/just
```

Start a new Bash session after creating the file.

If `bash-completion` is not installed, add the following line to `~/.bashrc`
instead:

```bash
source <(just --completions bash)
```

Then reload the configuration:

```bash
source ~/.bashrc
```

## Zsh

Generate the completion script:

```zsh
mkdir -p ~/.zsh/completions
just --completions zsh > ~/.zsh/completions/_just
```

Add the following lines to `~/.zshrc`:

```zsh
fpath=(~/.zsh/completions $fpath)
autoload -U compinit
compinit
```

The `fpath` assignment must appear before `compinit` runs. If you use Oh My
Zsh, put it before the line that sources `oh-my-zsh.sh`.

Restart Zsh or reload the configuration:

```zsh
source ~/.zshrc
```

## Fish

Save the generated script in Fish's completions directory:

```fish
mkdir -p ~/.config/fish/completions
just --completions fish > ~/.config/fish/completions/just.fish
```

Fish will lazy-load it in new shell sessions.

## PowerShell

Create the PowerShell profile if it does not exist:

```powershell
if (!(Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}
```

Add this line to `$PROFILE`:

```powershell
just --completions powershell | Out-String | Invoke-Expression
```

Reload the profile:

```powershell
. $PROFILE
```

This setup works with both Windows PowerShell and PowerShell 7.

## Elvish

Add the following code to `~/.elvish/rc.elv`:

```elvish
set edit:completion:arg-completer[just] = { |@args|
  eval (just --completions elvish | slurp)
  set @result = (edit:completion:arg-completer[just] $@args)
  put $@result
}
```

Start a new Elvish session to apply the change.

## Nushell

Generate the completion script in the Nushell configuration directory:

```nu
just --completions nushell | save -f ($nu.default-config-dir | path join just.nu)
```

Add this line to `config.nu`:

```nu
source just.nu
```

Start a new Nushell session after saving the configuration.

## Verify the Setup

Open a new shell in the project directory, type the following command, and
press <kbd>Tab</kbd>:

```text
just <Tab>
```

The shell should suggest recipes such as `app`, `sync`, `setup`,
`migrations`, `migrate`, and `downgrade`.

For shells that use a generated file (Bash, Zsh, Fish, and Nushell), regenerate
that file after upgrading `just` if completion behavior changes.

See the official
[`just` shell completion documentation](https://just.systems/man/en/shell-completion-scripts.html)
for additional details.
