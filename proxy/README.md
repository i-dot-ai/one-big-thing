## proxy whitelisting and basic auth

If basic auth is enabled you can add a user by ssh'ing to the relevant proxy server. i.e `etf-proxy-staging` using `cf ssh`

```
cf ssh etf-proxy-staging
```

Then run the following command replacing <username> as needed and typing in the password when prompted.

NOTE: **MAKE SURE YOU LEAVE THE `:`** (colon) inside the single quotes after the `username`
```
echo -n '<username>:' >> /app/.htpasswd
openssl passwd -apr1 >> /app/.htpasswd
```