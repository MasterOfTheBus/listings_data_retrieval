build : package.zip
	zip package.zip index.py

package : requirements.txt
	pip install --target ./package -r requirements.txt

package.zip : package
	cd ./package \
	&& zip -r ../package.zip . \
	&& cd ..

clean :
	rm -rf ./package package.zip
