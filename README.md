## Sublime Text Support for the [Ring](https://ring-lang.net/) Programming Language

This bundle provides [Ring](https://ring-lang.net/) syntax highlighting for Sublime Text.

## Features

- **Syntax Highlighting**: Complete support for Ring keywords, comments, strings, numbers, and operators
- **Interactive Tooltips**: Hover over Ring functions to see documentation, syntax, and examples
- **Code Completion**: Intelligent keyword and function completions
- **Build System Integration**: Run Ring files directly from Sublime Text (Ctrl+B/Cmd+B)
- **Menu Integration**: Access Ring tools via Tools > Ring menu
- **Settings Management**: Easy access to plugin settings via Preferences menu

## Installation

### Using Package Control

1. Open the Command Palette in Sublime Text by pressing `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).
2. Type `Package Control: Install Package` and select from the dropdown list.
3. Type `Ring` in the search box and select the `Ring` package from the list.

### Manual Installation

1. Download or clone this repository.
```bash
git clone https://github.com/ysdragon/ring-sublime
```
2. Copy the `ring-sublime` folder into your Sublime Text `Packages` directory. You can find the `Packages` directory by going to `Preferences` > `Browse Packages...` in Sublime Text.
3. Restart Sublime Text.

## Usage

Once installed, Sublime Text should automatically detect `.ring`, `.rform` and `.rh` files and apply the syntax highlighting. If it does not, you can manually set the syntax by:

1. Opening a `.ring` file.
2. Going to `View` > `Syntax` > `Open all with current extension as...` > `Ring`.

### Interactive Features

- **Tooltips**: Hover over Ring functions and keywords to see interactive documentation with examples
- **Menu Access**: Use `Tools > Ring` to access plugin features like running files, toggling tooltips, and opening Ring resources
- **Settings**: Configure the plugin via `Preferences > Package Settings > Ring`
- **Quick Build**: Press `Ctrl+B` (Windows/Linux) or `Cmd+B` (macOS) to run Ring files directly

## Screenshots

![Ring Syntax Highlighting Example 1](img/1.png)
![Ring Syntax Highlighting Example 2](img/2.png)
![Ring Syntax Highlighting Example 3](img/3.png)

## License
This project is open-source and available under the MIT License. See the [LICENSE](https://github.com/ysdragon/ring-sublime/blob/master/LICENSE) file for more details.