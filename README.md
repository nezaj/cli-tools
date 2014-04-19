## Command Line Tools
Custom CLI tools to make my life easier

* `pfs` prints file directory structure
* `mdview` preview markdown file in chrome

### Setup (Mac)
Make sure `/usr/local/bin` is in your `PATH`. Install [Markdown][markdown-install] and move `Markdown.pl` to `usr/local/bin`.

Now run the following commands
```
cd
git clone https://github.com/nezaj/cli-tools.git
ln -s ~/cli-tools/pfs.py /usr/local/bin/pfs
ln -s ~/cli-tools/mdview.sh /usr/local/bin/mdview
```

[markdown-install]: http://daringfireball.net/projects/downloads/Markdown_1.0.1.zip
