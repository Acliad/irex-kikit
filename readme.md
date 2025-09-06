# IRex KiCad Kit

A collection of workflow helpers, templates, settings, etc. that I regularly use for KiCad.

# Scripts
This folder contains helper scripts and a Python module for various automation tasks. 

## Releaser
This is a set of tools to help with releasing a finished PCB design. It includes:
- Generating a complete set of manufacturing files (Gerbers, Drill files, BOM, Pick and Place, etc.)
- Generating a PDF documentation package

See the [Releaser README](scripting/readme.md) for more details and instructions on setup and usage.

# ☑️ TODOs And Wants
- Create a way to auto-sync updated Drawing Page templates to embedded files in project templates
- Create a way to auto-sync updated Release.kicad_jobset
  - Different layer number templates require slightly altered jobsets, but generally want to keep the same

## 📄 License

This repository uses a dual licensing approach:

### Technical Components
**MIT License** - Applies to:
- Project templates
- Configuration files
- Custom scripts and automation tools
- Documentation and tutorials

### Branding and Visual Assets
**All Rights Reserved** - Applies to:
- IRex logos and branding materials
- Custom worksheet templates containing logos
- Any proprietary visual designs

See [LICENSE](LICENSE) for full MIT license text.

**Note**: The IRex logo and associated branding materials are proprietary and may not be used, modified, or distributed without explicit permission.