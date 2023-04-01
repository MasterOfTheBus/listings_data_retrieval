build : get_listings.zip
	zip get_listings.zip index.py

package : requirements.txt
	pip install --target ./package -r requirements.txt

package.zip : package
	cd ./package \
	&& zip -r ../get_listings.zip . \
	&& cd ..

clean :
	rm -rf ./package get_listings.zip
