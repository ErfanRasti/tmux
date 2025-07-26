# TMUX Configurations

Here I share my `tmux` configurations.

## Install pre-requirements

```bash
sudo pacman -S tmux
```

The default prefix is `CTRL+b`.

### Install Tmux Plugin Manager (TPM)

1. Close the repo:

    ```bash
    git clone https://github.com/tmux-plugins/tpm ~/.config/plugins/tpm
    ```

2. Put these lines at your `~/.config/tmux/tmux.conf`:

    ```conf
    # List of plugins
    set -g @plugin 'tmux-plugins/tpm'
    set -g @plugin 'tmux-plugins/tmux-sensible'

    run '~/.tmux/plugins/tpm/tpm'
    ```

3. Open `tmux` and press `<prefix>+I`.

### Other plugin pre-requirements

```sh
sudo pacman -S python-tzlocal python-icalendar yz fzf
```

For more info about `tmux` check [this](https://github.com/ErfanRasti/arch-setup/blob/main/docs/09_Shell_and_Terminal/1_shell_and_terminal.md#tmux).
