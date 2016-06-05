# sli.mg Python Api Helper

Written in Python 2.7

-----

This wrapper is designed to help Python developers use the image hosting website `sli.mg` in their scripts!

----

To begin using it, you must import it using `from slimghelper import slimgHelper`

Then initialize it, you will need your Client ID and Client Secret for this next step. You can get those by reading through [this simple tutorial - https://sli.mg/public/api#getstarted.](https://sli.mg/public/api#getstarted)

Now, using any variable name you choose, call the class! For these next few examples, I will use `helper` as our name. Example: `helper = slimgHelper('<YOUR_CLIENT_ID>', '<YOUR_CLIENT_SECRET>')`

Next, run `helper.getAccessRefreshTokens()` If it returns True, you have access to every function in the script, and API (as of June 4, 2016)!

Here's a nice list of Functions:

  - `getAccessRefreshTokens(returnTokens=False)`

    - You need to run this in order to run the rest of the methods, as it aquires the needed Access Token. ***This reruns itself every 23 hours!***

    - Other Possible Arguments: returnTokens (false by default)

      - This will return the Access and Refresh Tokens if you want them! (Note: They expire after 24 hours!)


  - `getUserAlbums(username)`

    - This returns a list of albums (in dictionary form) from the specified user!


  - `getUserMedia(username)`

    - This returns a list of images (in dictionary form) from the specified user!


  - `getMediaInfo(mediaKey)`

    - This returns a dictionary of info for the requested image


  - `createMedia(type, data, size=None, title=None, description=None, shared=None, albumKey=None, albumSecret=None, tags=None, waitForUploadCompletionForDataReturn=False)`

    - This will take an image (either binary image, URL, or base64) and upload it.

    - Other Possible Arguments:

      - 'size' is the size of the file in bytes (integer)

      - 'shared' is whether it's public or not

      - 'album_key' is the key for the album you want it to go into (if supplied)

      - 'album_secret' is not working yet.

      - Extra info:

        - Using type 'binary' will turn it into a base64 image (temp workaround)

        - Type has to be either 'binary', 'URL', or 'base64'

        - waitForUploadCompletionForDataReturn will wait until the image is done uploading (or fails), and will return it's data.


  - `updateMedia(` same as createMedia except without `type, data, size, and waitForUploadCompletionForDataReturn)`

    - Updates image based on given arguments


  - `deleteMedia(mediaKey)`

    - Deletes image based on media key


  - `getAlbumInfo(albumKey)`

      - This returns a dictionary of info for the requested album


  - `createAlbum(description=None, shared=None, mediaKeys=None, mediaSecrets=None, tags=None)`

    - Creates an album.

    - Other Possible Arguments:

      - `mediaKeys` are photos you want to include in the album

      - `mediaSecrets` does not work yet.


- `updateAlbum(albumKey, same as createAlbum)`

    - Updates album based on arguments


- `deleteAlbum(albumKey)`

  - Deletes album based on album key


- `getAlbumMedia(albumKey)`

  - Gets album media in the same fashion as getUserMedia, as a list of images (in dictionary form) from the specified album.


- `browsePublic(page=1)`

  - Lets you browse the public list of images. Page by default is 1.

  - Note: Times out a lot of the time.


- `browsePublicByTag(tag, type="sfw", page=1)`

  - Browses public images based on tag.

  - Notes:

    - Type can either be 'all', 'sfw', or 'nsfw'
