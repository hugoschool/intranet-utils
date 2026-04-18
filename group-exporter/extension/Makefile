SRC	:=	$(shell \
			find . -name "*" -type f \
			-not -name "Makefile" \
			-not -name "README.md" \
			-not -name "*.xpi" \
			-not -name "*.zip" \
			-not -name ".gitignore" \
			-not -name ".amo-upload-uuid" \
		)

FIREFOX_BIN	:=	group-exporter-firefox.xpi
CHROMIUM_BIN	:=	group-exporter-chromium.zip

.PHONY:	default
default:	firefox chromium

.PHONY:	firefox
firefox:	$(FIREFOX_BIN)

$(FIREFOX_BIN):	$(SRC)
	zip -r -FS $(FIREFOX_BIN) $^

.PHONY:	chromium
chromium:	$(CHROMIUM_BIN)

$(CHROMIUM_BIN): $(SRC)
	zip -r -FS $(CHROMIUM_BIN) $^

.PHONY:	clean
clean:
	$(RM) $(CHROMIUM_BIN)
	$(RM) $(FIREFOX_BIN)
