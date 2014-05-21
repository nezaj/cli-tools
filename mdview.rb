#!/usr/bin/env ruby
require 'tempfile'
require 'github/markup'
require 'launchy'

HELP = <<-help
  Usage: gfm <file>
  Preview a GitHub-Flavored Markdown file in your browser
help

if ARGV.include?('--help')
  puts HELP
  exit 0
end

# Check to see that file exists
infile_name = ARGV.first
infile_path = File.join(Dir.pwd, infile_name)
unless File.file?(infile_path)
  puts "Could not find #{infile_path}, please verify that the file exists"
  exit 0
end

# Create a temporary html file to save markdown
temp_outfile_path = File.join(Dir.tmpdir, infile_name) + '.html'
File.open(temp_outfile_path, "w") do |outfile|
  markup = GitHub::Markup.render(infile_name, File.read(infile_name))
  outfile.write(markup)
end

# Preview file in default browser
temp_outfile = 'file:///' + temp_outfile_path
Launchy.open(temp_outfile)
