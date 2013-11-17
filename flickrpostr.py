import flickrapi
import sys
import os

flickr_api_key = '4cd738c10a50fc3920624d4dd467b173'
flickr_api_secret = 'f64c969340275b76'

def main():
    flickr = flickrapi.FlickrAPI(flickr_api_key, flickr_api_secret)

    (token, frob) = flickr.get_token_part_one(perms='write')
    if not token:
        raw_input("Press ENTER after you authorized this program")

    flickr.get_token_part_two((token, frob))

    print "Uploading new set %s" % sys.argv[1]

#    flickr.photosets_create(title=sys.argv[1]

    files_to_upload = []
    for files in os.listdir(sys.argv[1]):
        if files.endswith(".jpg") or files.endswith(".JPG"):
            files_to_upload.append(files)
    files_to_upload = sorted(files_to_upload)

    number_of_files = len(files_to_upload)
    files_uploaded = 0;
    photo_ids = []
    for f in files_to_upload:
        result = flickr.upload(os.path.join(sys.argv[1], f),
                               is_public=1,
                               content_type=1)
        photo_ids.append(result.getchildren()[0].text)
        files_uploaded += 1
        print "({done}/{total}) {file}\r".format(
                done = files_uploaded,
                total = number_of_files,
                file = f,
                ),


    # Create set and add photos
    photoset_result = flickr.photosets_create(title=sys.argv[2],
                                              primary_photo_id=photo_ids[0])
    photoset_id = photoset_result.getchildren()[0].get('id')

    for pid in photo_ids:
        try:
            flickr.photosets_addPhoto(photoset_id=photoset_id, photo_id=pid)
        except flickrapi.exceptions.FlickrError as e:
            print "Exn! %s" % e


main()
