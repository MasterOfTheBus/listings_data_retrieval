build : get_listings_info.zip
	zip get_listings_info.zip index.py

package : requirements.txt
	pip install --target ./package -r requirements.txt

get_listings_info.zip : package
	cd ./package \
	&& zip -r ../get_listings_info.zip . \
	&& cd ..

clean :
	rm -rf ./package get_listings_info.zip

test :
	python -m unittest
