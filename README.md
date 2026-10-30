# MLC Ward-wise List

Ward-wise voter/member list with a common WhatsApp/SMS message (`{name}`, `{ward}`, `{street}`... are replaced
for each member), search, add/edit/delete, CSV import. React runs straight from `www/` with no build step.

## IMPORTANT: privacy
`www/data.js` contains names, addresses and phone numbers of about 16,600 people.
- Keep the GitHub repository **Private**.
- Do **not** run the GitHub Pages workflow unless you want this data public on the internet.
- The APK you build is for your own team. Do not post it publicly.

## Get the Android APK (recommended)
1. On GitHub create a new **private** repository.
2. Upload everything in this folder (keep the `.github` folder). With the web page: *Add file > Upload files*,
   drag the folder contents in. Make sure `.github/workflows/android-apk.yml` is included.
3. Open the **Actions** tab, choose **Build Android APK**, press **Run workflow**.
4. When the run turns green, open it and download **MLC-Ward-wise-List-apk** under *Artifacts* (a zip with `app-debug.apk`).
5. Copy the APK to the phone and install it (allow "install unknown apps" for your file manager once).

The first run takes about 5 to 10 minutes. This is a debug-signed APK, fine for sideloading.
For the Play Store you would need a release build with your own signing key.

## Run it on a computer
```
npm run serve        # then open http://localhost:8080
```
or just open `www/index.html` in a browser (works offline, the libraries are in `www/vendor`).

## Update the records
Records live in `www/data.js` (`BASE_RAW`). Each row is
`[ward, name, relType, relName, house, street, phone, village, age, reviewNote]`, ward `"1"`..`"48"` or `"mixed"`.
- Rebuild from an Excel file: `pip install pandas openpyxl` then `python tools/xlsx_to_data.py my-list.xlsx`
  (this replaces `www/data.js`; the Mixed Data list from the PDF is not rebuilt by this script).
- Or keep the built-in data and use **Settings > Add or import member records** in the app. Those
  additions are saved only in that phone's browser storage.
Commit the change and run **Build Android APK** again.

## Files
- `www/index.html` the app (React via `htm`, no compiler). `www/data.js` the records. `www/vendor/` React 18.3.1, htm 3.1.1.
- `capacitor.config.json`, `package.json` wrap `www/` as an Android app (Capacitor 6).
- `.github/workflows/android-apk.yml` builds the APK. `.github/workflows/pages.yml` optional, manual, public web hosting.
- `tools/xlsx_to_data.py` Excel to `data.js` converter.

## Known limits
- WhatsApp links carry text only; a photo cannot be attached automatically. WhatsApp always needs a person to tap send.
- Phone numbers that are not 10-digit Indian mobiles (6 to 9 first digit) have their buttons disabled.
- Saved edits/messages live in the app's local storage on that phone only.
