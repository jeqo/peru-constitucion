all:

run:
	mdbook serve

build:
	mdbook build

prepare-deploy:
	git worktree add public gh-pages

deploy: build
	rm -rf public/*
	cp -rp book/* public/.
	cd public && \
		git add -A && git commit -m "publish" && git push origin gh-pages
	

get:
	mkdir -p static/consticiones
	wget ${URL} -O static/consticiones/${YEAR}.pdf

get.1979:
	make YEAR=1979 URL=http://www.leyes.congreso.gob.pe/Documentos/constituciones_ordenado/CONSTIT_1979/Cons1979_TEXTO_CORREGIDO.pdf get
get.1993:
	make YEAR=1993 URL=http://www.leyes.congreso.gob.pe/Documentos/constituciones_ordenado/CONSTIT_1993/Texto_actualizado_CONS_1993.pdf get