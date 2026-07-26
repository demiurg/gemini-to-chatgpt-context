# Export Gemini Apps activity with Google Takeout

## Step 1: Access and clear the selection

1. Go to [takeout.google.com](https://takeout.google.com/).
2. At the top of the product list, select **Deselect all**. This prevents an
   unnecessarily large Google-account export.

## Step 2: Select Gemini chat activity

1. Scroll to **My Activity** — do **not** select the separate **Gemini** box.
   That option exports custom Gems settings, not the Gemini Apps chat history.
2. Select **My Activity**.
3. Select **All activity data included** beneath it.
4. In the pop-up, select **Deselect all**, then select only **Gemini Apps**.
5. Select **OK**.

## Step 3: Create the export

1. Scroll to the bottom and select **Next step**.
2. Keep the default one-time `.zip` export unless you have a reason to change
   it, then select **Create export**.
3. Wait for Google’s email, download the archive, and extract it locally.

The expected source file is:

```text
Takeout/My Activity/Gemini Apps/MyActivity.json
```

Keep the ZIP and extracted Takeout directory private and out of Git.
