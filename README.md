# gpg-expiration

Check if a GPG key will expire soon.

## Usage

gpg-expiration needs a key ID, or other uniquely identifying search term;
`gpg --list-keys SEARCH_TERM` should return exactly one key.

gpg-expiration also takes an interval, specified in days.
If the key (or any of its subkeys) expires within that interval,
it will print the primary UID and the expiration date(s),
then exit with a return code of 1.
If not, it will silently exit with a return code of 0.

```sh
$ ./gpg-expiration.py --days 30 2B38BD955557647E7C26B53C19E27469767CFC68
```

Add it as a cron job:

```sh
$ crontab -e
```

```
# m  h dom mon dow command
  0 12  *   *  Mon ~/dev/gpg-expiration/gpg-expiration.py --days 30 2B38BD955557647E7C26B53C19E27469767CFC68
```

As a special case, you can use the value "all" to check all keys in the current keyring.

```sh
./gpg-expiration.py --days 0 all
```

## Dependencies

gpg-expiration depends on the official
[GPGME](https://www.gnupg.org/related_software/gpgme/index.html)
Python bindings.

The Python bindings are available in the Debian package
[python3-gpg](https://packages.debian.org/stable/python3-gpg):

```sh
$ sudo apt install python3-gpg
```
