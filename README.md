# Doctor Static

Doctor Static is a static website generator, using Markdown for source content source, and Jinja2 for templating.

## What's good

### Portable content
Source files are Markdown with the addition of a small meta data header.  The header is easily parsed for conversion to another system, or outright removal.

### Template powered
Most publishing systems mistakenly cram functionality into the generator.  Doctor Static prefers to broadly collect and expose data, keeping the application flexible and agnostic to its implementation.

This strategy allows powerful template driven systems to more fully control the presentation without cluttering application with implementation specific features.

### Quick start
* Baked in support for tags and Atom syndication.  
* Starting templates
* An example site is included, ready to be customized and used.
* Minimal technical configuration (zero configuration if using example site).

### Light weight
Doctor Static is <500 lines, not including tests.  It is well factored, completely tested and easily extended.

## Why not Doctor Static?
Doctor Static is not a "website in a box".  It is a deliberately light weight generator, intended for developers that are already familiar with web development.

There are many, more fully featured, Markdown based site generators that may want to consider, such as Jekyll and Nikola.  

## Dependencies
* Python 3.5/3.x.  
	
	The application is compatible with 3.x, except dynamic module loading which changed in 3.5.  

* Modules:
	* Markdown
	* Jinja2
	* Feedgen

## Usage

Doctor Static should exist outside of your site project, allowing you to manage your source content, templates, css, etc in its own repository.  

Your project should include a Doctor Static config module, which is given to the build script.  

I recommend creating a script to wrap the build command.  An example is included the example site.

### Generate site
	/path/to/doctor_static/build path/to/config.py
	
### config.py
Your config should paths to your content, template, render directories and syndication configuration.  A complete example is included in the example site.

	CONTENT_SOURCE_DIR = 'path/to/content_source'
	TEMPLATE_DIR = 'path/to/templates'
	RENDER_DIR = 'path/to/render_dir'
	SYNDICATION = {}
