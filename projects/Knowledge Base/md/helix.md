# Helix Setup Guide for Linux
## 1. Installation

### 1.1 Install Helix on Linux

1. Download Helix Binary:

   Download the Helix binary using `curl`:

   ```bash
   curl -LO https://github.com/helix-editor/helix/releases/download/22.12.0/helix-22.12.0-linux-x86_64.tar.xz
   ```

2. Extract the Tarball:

   Extract the downloaded tarball:

   ```bash
   tar -xvf helix-22.12.0-linux-x86_64.tar.xz
   ```

3. Copy Helix Binary to `$PATH`:

   Copy the `helix` binary to `/usr/local/bin` or any other directory in your `$PATH`:

   ```bash
   sudo cp helix /usr/local/bin/
   ```

4. Verify Installation:

   Check the installed version of Helix:

   ```bash
   helix --version
   ```

   You should see output like:

   ```
   Helix v22.12.0
   ```

---

## 2. Post-Installation Configuration

### 2.1 Copy the Runtime Directory

Helix requires a runtime directory for various runtime files (such as syntax definitions, keymaps, etc.).

1. Create the Runtime Directory:

   Create the `runtime` directory inside `~/.config/helix/`:

   ```bash
   mkdir -p ~/.config/helix/runtime
   ```

2. Copy the Runtime Files:

   Assuming you have access to the Helix runtime directory (usually bundled with the binary), copy the contents to `~/.config/helix/runtime` using `cp` (no `mv`):

   ```bash
   cp -r helix-runtime/* ~/.config/helix/runtime/
   ```

   If you don't have the runtime files locally, you may need to manually download or extract them from the Helix GitHub releases.

---





### 2.2 Setup Helix Configuration Files

1. Create the Helix Configuration Directory:

   Create the `~/.config/helix` directory if it doesn’t exist:

   ```bash
   mkdir -p ~/.config/helix
   ```

2. Download Configuration Files:

   Download your configuration files directly into the `~/.config/helix/` directory using `curl`:

   - Download `config.toml`:

     ```bash
     curl -L "https://raw.githubusercontent.com/nooransari911/notes/refs/heads/main/system/helix/config.toml?token=GHSAT0AAAAAAC36C7BO36WSER547MC44OB2Z3BU55A" -o ~/.config/helix/config.toml
     ```

   - Download `languages.toml`:

     ```bash
     curl -L "https://raw.githubusercontent.com/nooransari911/notes/refs/heads/main/system/helix/languages.toml?token=GHSAT0AAAAAAC36C7BOBC2GNND7BUGGUZMIZ3BUMOA" -o ~/.config/helix/languages.toml
     ```

   - Download `theme0.toml`:

     ```bash
      curl -L "https://raw.githubusercontent.com/nooransari911/notes/refs/heads/main/system/helix/themes/theme0.toml?token=GHSAT0AAAAAAC36C7BOFFRTGFU3R4M32NBMZ3BU62Q" -o ~/.config/helix/themes/theme0.toml
     ```

---


### 2.3 Download and Configure Themes

1. Verify Your Theme:

   The `theme0.toml` file is already configured for your setup. If you want to install more themes, download them and copy to the `~/.config/helix/themes/` directory:

   ```bash
   curl -L "<theme-url>" -o ~/.config/helix/themes/custom_theme.toml
   ```

2. Set the Active Theme:

   In your `~/.config/helix/config.toml`, set the active theme:

   ```toml
   [editor]
   theme = "theme0"
   ```

   Replace `"theme0"` with the name of any theme you add.

---

### 2.4 Configure Language Servers

1. Install Language Servers:

   Install the required language servers for the languages you are using. For example, for Python (`pyright`):

   ```bash
   npm install -g pyright
   ```

2. Configure Language Servers in `languages.toml`:

   Make sure the `languages.toml` file has the correct configuration for the language servers you installed. For example:

   ```toml
   [[languages]]
   name = "python"
   server = "pyright"
   ```

   You can add more language servers for other languages as needed.


#### Bash to install all required lsps

```
# AWK
sudo npm i -g "awk-language-server@>=0.5.2"


# Python
pip install -U 'python-lsp-server[all]'

# Markdown
# Download the binary from github. Rename it to marksman and then move it to ~/.local/bin/
# Then add ~/.local/bin to $PATH by adding "export PATH="$HOME/.local/bin:$PATH"" to bashrc file
```



---

That’s it! Helix should now be installed and configured properly on your Linux system with the necessary runtime files, themes, and language servers.




---
---
---
---


# Compiled bash
```bash
#!/bin/bash

# Helix Setup Guide for Linux

# 1. Installation

## 1.1 Install Helix on Linux

# Step 1: Download Helix Binary
echo "Downloading Helix binary..."
curl -LO https://github.com/helix-editor/helix/releases/download/22.12.0/helix-22.12.0-linux-x86_64.tar.xz

# Step 2: Extract the Tarball
echo "Extracting the tarball..."
tar -xvf helix-22.12.0-linux-x86_64.tar.xz

# Step 3: Copy Helix Binary to $PATH
echo "Copying Helix binary to /usr/local/bin..."
sudo cp helix /usr/local/bin/

# Step 4: Verify Installation
echo "Verifying Helix installation..."
helix --version

# 2. Post-Installation Configuration

## 2.1 Copy the Runtime Directory

# Step 1: Create the Runtime Directory
echo "Creating runtime directory..."
mkdir -p ~/.config/helix/runtime

# Step 2: Copy the Runtime Files
echo "Copying runtime files..."
# Assuming you have the helix-runtime folder from the extraction step, adjust the source path if needed
cp -r helix-runtime/* ~/.config/helix/runtime/

# If you don't have the runtime files locally, you can download them manually from the Helix releases page.

## 2.2 Setup Helix Configuration Files

# Step 1: Create the Helix Configuration Directory
echo "Creating Helix configuration directory..."
mkdir -p ~/.config/helix

# Step 2: Download Configuration Files
echo "Downloading configuration files..."

# Download config.toml
curl -L "https://raw.githubusercontent.com/nooransari911/notes/refs/heads/main/system/helix/config.toml?token=GHSAT0AAAAAAC36C7BO36WSER547MC44OB2Z3BU55A" -o ~/.config/helix/config.toml

# Download languages.toml
# curl -L "https://raw.githubusercontent.com/nooransari911/notes/refs/heads/main/system/helix/languages.toml?token=GHSAT0AAAAAAC36C7BOBC2GNND7BUGGUZMIZ3BUMOA" -o ~/.config/helix/languages.toml

# Download theme0.toml
curl -L "https://raw.githubusercontent.com/nooransari911/notes/refs/heads/main/system/helix/themes/theme0.toml?token=GHSAT0AAAAAAC36C7BOFFRTGFU3R4M32NBMZ3BU62Q" -o ~/.config/helix/themes/theme0.toml

## 2.3 Download and Configure Themes

# Step 1: Verify Your Theme (Already configured as theme0.toml in previous step)
echo "Themes are configured. If you want to add custom themes, download them now."

# Step 2: Set the Active Theme
# In case you need to add a new theme, you can download more themes and configure them here.
# Example:
# curl -L "<theme-url>" -o ~/.config/helix/themes/custom_theme.toml

echo "To set a different theme, edit the '~/.config/helix/config.toml' file and change the theme key."

## 2.4 Configure Language Servers

# Step 1: Install Language Servers
echo "Installing language servers..."
# Example: Install Python language server (pyright) using npm
npm install -g pyright

# Step 2: Configure Language Servers in languages.toml
# Example: Python language server configuration
echo "Configuring language servers..."

# Make sure the languages.toml file is updated, here is an example for Python:
# [[languages]]
# name = "python"
# server = "pyright"

echo "Helix setup completed successfully!"
echo "You may need to configure more language servers and themes as per your preferences."

# End of the script


```






