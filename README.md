# Booru Image Downloader

A simple Python script to download images from [*.booru.org](https://booru.org/) websites.  
Supports Cloudflare-protected booru sites (requires your `cf_clearance`, `user_id`, and `pass_hash` cookies).

---

## Features
- Works on any `*.booru.org` domain (e.g. `censored.booru.org`, `rule34.xxx`, etc.)
- Handles Cloudflare protection via cookies
- Automatically names the download folder based on domain and search tags  
  e.g. `downloads_censored_booru_user_trs`
- Skips already-downloaded images so you can re-run the script later
- Prints progress while downloading

---

## Requirements
- Python 3.8+
- Install dependencies:
  ```bash
  pip install requests beautifulsoup4
  ```

---

## Usage

```bash
python booru.py [URL] --cf-clearance CF_CLEARANCE --user-id USER_ID --pass-hash PASS_HASH
```

## Arguments
- `URL`  
  The booru search results URL.  
  Example:  
  ```
  https://some.booru.org/index.php?page=post&s=list&tags=your_favorite_tag
  ```

- `--cf-clearance`  
  The value of the `cf_clearance` cookie (from your browser).

- `--user-id`  
  The value of the `user_id` cookie (from your browser).

- `--pass-hash`  
  The value of the `pass_hash` cookie (from your browser).

---

## Example

```bash
python booru.py "https://some.booru.org/index.php?page=post&s=list&tags=your_favorite_tag" --cf-clearance "aBcDeFgHiJkLmNoPqRsTuVwXyZ" --user-id "1234567890abcdef1234567890abcdef12345678" --pass-hash "12345"
```

This will save all images into:

```
downloads_some_booru_your_favorite_tag/
```

---

## Getting Cookie Values
To obtain the required cookie values:

Log into the booru website in your browser

Open Developer Tools (F12)

Go to the Application/Storage tab

Find Cookies for the booru domain

Copy the values for:

cf_clearance

pass_hash

user_id
