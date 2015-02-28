## Command Line Tools
Custom CLI tools to make my life easier

* `gen_log` generates daily log entries
* `pfs` prints file directory structure
* `mdview` preview markdown file in chrome

### Dependencies
Make sure `/usr/local/bin` is in `PATH`. We'll also need a couple of ruby gems
```
gem install markdown
gem install github-markup
gem install launchy
```

### Installing
```
git clone https://github.com/nezaj/cli-tools.git ~/cli-tools
cd cli-tools
./setup.sh
mkvirtualenv cli-tools
pip install -r requirements.txt
```
Commands like `pfs` and `mdview` should now be available in the terminal. Huzzah!

[markdown-install]: http://daringfireball.net/projects/downloads/Markdown_1.0.1.zip
