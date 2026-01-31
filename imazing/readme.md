# Backup using Imazing

This proccess will show you step-by-step how to backup your Procreate files using Imazing (you don't need to buy the software). Do mind, you'll need space to store all iPad's files.

---

## Step 01 – Backup Now
Start the backup process by choosing **Backup Now**.

![Step 00](./00-backup-now.png)

---

## Step 02 – Select Backup
Choose what you want to back up (files, folders, or application data).

![Step 01](./01-backup-select.png)

---

## Step 03 – Start Backup
Confirm your selection and start the backup process.

![Step 02](./02-backup-start.png)

---

## Step 04 – Backing Up
The system is actively backing up your data.

![Step 03](./03-backing-up.png)

---

## Step 05 – Verify Backup
Verify that the backup completed successfully and data integrity is intact.

![Step 04](./04-backup-verify.png)

---

## Step 06 – Backup Complete
Backup finished successfully.

![Step 05](./05-complete.png)

---

## Step 07 – Choose Location
Select where the backup is stored or where it should be restored from.

![Step 06](./06-location.png)

---

## Step 08 – Select File System
Choose the target file system.

![Step 07](./07-select-file-system.png)

---

## Step 09 – Application Export (Procreate)
Export application-specific data (example shown: Procreate).

![Step 08](./08-application-support-procreate.png)

---

## Step 10 – Copy to Mac
Copy the backup files to your Mac.

![Step 09](./09-copy-to-mac.png)

---

## Step 11 – Copying Files
Files are being transferred.

![Step 10](./10-copying.png)

---

## Step 12 – Extraction Complete
All files have been successfully extracted.

![Step 11](./11-extracted-complete.png)

---

## Step 13 – Using Python Script
![Step 12](./12-using-python-script.png)

Run a Python script to organize the extracted files.

A. Copy the python script into the same Procreate folder.
B. Open Terminal: cd your_procreate_folder (drag your folder) -> Enter
C. In terminal:

```bash
python3 export_procreate.py /path/to/Application\ Support/
```

---

## Step 14 – Python Script Done
Python script finished running successfully.

![Step 13](./13-py-done.png)

---

## Step 15 – Select All
Select all relevant files or folders -> CTRL+CMD+N to create a folder that will put inside the files.

![Step 14](./14-select-all.png)

---

## Step 16 – Single Folder Output
All data is now organized into a single folder 🎉.
Highly suggest to [Download Prospect](https://jaromvogel.com/prospect/Prospect_v1_2_1.zip) that way you could preview your Procreate files.

![Step 15](./15-one-folder.png)

---

## Backup Folder Structure
Final backup folder structure for reference.

![Backup Folder](./backup-folder.png)



