.POSIX:
NAME=mbi-ck
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
BUILDDIR=$(abspath ../build)
SRCDIR=$(abspath .)
DOCDIR=$(abspath ../doc)
ROOTDIR=$(abspath ../)


# Detect operating system in Makefile.
# Author: He Tao
# Date: 2015-05-30

OSFLAG :=
ifeq ($(OS),Windows_NT)
	DISTDIR=$(abspath ../dist-win)
	OSFLAG += WIN
	SEPARATOR=;
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		DISTDIR=$(abspath ../dist-linux)
		OSFLAG += LINUX
		SEPARATOR=:
	endif
	ifeq ($(UNAME_S),Darwin)
		DISTDIR=$(abspath ../dist-macos)
		OSFLAG += MACOS
		SEPARATOR=:
	endif
endif


.PHONY: all help clean cleancache build 
all:
	@echo $(OSFLAG)
	@echo $(SRCDIR)
	@echo $(BUILDDIR)
	@echo $(DISTDIR)


# self-documenting function is made based on https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Shows this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'


clean: ## Delete build/ and dist-macos/ directories made by PyInstaller
	@echo "Cleaning.."
	@[ ! -d $(DISTDIR) ] || rm -rf $(DISTDIR)
	@[ ! -d $(BUILDDIR) ] || rm -rf $(BUILDDIR)


cleancache: ## Clean PyInstaller cache
	@echo "Cleaning.."
	pyinstaller --clean --distpath $(DISTDIR) --workpath $(BUILDDIR) $(SRCDIR)/main.py


build: ## Make executable binary for OS system by PyInstaller
	pyinstaller -y --name $(NAME) --distpath $(DISTDIR) --workpath $(BUILDDIR) --windowed -D --add-data "indicators_complete_template.html$(SEPARATOR)." --add-data "$(DOCDIR)/CTIME.txt$(SEPARATOR)." --add-data "$(ROOTDIR)/CHANGELOG.md$(SEPARATOR)." $(SRCDIR)/main.py

