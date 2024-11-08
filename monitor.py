import requests, json, base64
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from datetime import datetime

webhook = DiscordWebhook(url="")
webhook.set_content('|| @everyone ||')

def create_version_directory(version):
    if not os.path.exists('archive'):
        os.makedirs('archive')
    if not os.path.exists('archive/hsw'):
        os.makedirs('archive/hsw')
    
    today = datetime.today()
    date_str = today.strftime("%d.%m.%Y")
    
    new_dir_name = f"{date_str} - {version}"
    new_dir_path = os.path.join('archive', 'hsw', new_dir_name)
    
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    
    return new_dir_path + "/"

def create_version_directory_hcap(version):
    if not os.path.exists('archive'):
        os.makedirs('archive')
    if not os.path.exists('archive/hcaptcha'):
        os.makedirs('archive/hcaptcha')
    
    today = datetime.today()
    date_str = today.strftime("%d.%m.%Y")
    
    new_dir_name = f"{date_str} - {version}"
    new_dir_path = os.path.join('archive', 'hcaptcha', new_dir_name)
    
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    
    return new_dir_path + "/"

class Hcaptcha:
    def __init__(self) -> None:
        self.HcapVersion = ["failed"]
        self.HcapOldVersion = "None"
        self.HcapNewVersion = "None"

        self.HswVersion = ["failed"]
        self.HswOldVersion = "None"
        self.HswNewVersion = "None"

    def add_padding(self, base64_string):
        unpadded_length = len(base64_string.rstrip("="))
        padded_length = 4 * ((unpadded_length + 3) // 4)
        padding = "=" * (padded_length - unpadded_length)
        return base64_string + padding

    def get_hcaptcha_version(self) -> str:
        return requests.get(
            'https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad',
            headers={
                'authority': 'hcaptcha.com',
                'accept': '*/*',
                'accept-language': 'fr-BE,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                'referer': 'https://discord.com/',
                'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'script',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            }
        ).text.split('assetUrl:"https://newassets.hcaptcha.com/captcha/v1/')[1].split('/')[0]
    
    def get_hsw_version(self, hcaptchaVersion):
        try:
            response = requests.post(
                'https://hcaptcha.com/checksiteconfig',
                params={
                    'v': hcaptchaVersion,
                    'host': 'discord.com',
                    'sitekey': '4c672d35-0701-42b2-88c3-78380b0db560',
                    'sc': '1',
                    'swa': '1',
                    'spst': '0',
                },
                headers={
                    'accept': 'application/json',
                    'accept-language': 'se-se,se;q=0.7',
                    'content-length': '0',
                    'content-type': 'text/plain',
                    'origin': 'https://newassets.hcaptcha.com',
                    'referer': 'https://newassets.hcaptcha.com/',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-gpc': '1',
                    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                }
            )
            jwtToken = response.json()['c']["req"]
            hswVersion = str(json.loads(base64.b64decode(self.add_padding(jwtToken.split('.')[1])).decode())['l']).split('https://newassets.hcaptcha.com/c/')[1]
            return hswVersion
        except:
            return "failed"
    
    def sendHcaptchaVersionChange(self, oldVersion, newVersion):
        path = create_version_directory_hcap(newVersion)
        url = f'https://newassets.hcaptcha.com/captcha/v1/{newVersion}/hcaptcha.js'
        with open(path + "hcaptcha.js", 'w') as f:
            content = requests.get(
                url,
                headers={
                    'accept': 'application/json',
                    'accept-language': 'se-se,se;q=0.7',
                    'content-length': '0',
                    'content-type': 'text/plain',
                    'origin': 'https://newassets.hcaptcha.com',
                    'referer': 'https://newassets.hcaptcha.com/',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-gpc': '1',
                    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                }
            ).text
            f.write(content)

        embed = DiscordEmbed(
            title=f'New hcaptcha version: {newVersion}',
            description=f'**From**: `{oldVersion}`\n**To**: `{newVersion}`',
            color="03b2f8"
        )
        embed.url = url

        webhook.add_embed(embed)
        webhook.add_file(content, "hcaptcha.js")
        webhook.execute(True)

    
    def sendHswVersionChange(self, oldVersion, newVersion):
        path = create_version_directory(newVersion)
        url = f'https://newassets.hcaptcha.com/c/{newVersion}/hsw.js'
        with open(path + "hsw.js", 'w') as f:
            content = requests.get(
                url,
                headers={
                    'accept': 'application/json',
                    'accept-language': 'se-se,se;q=0.7',
                    'content-length': '0',
                    'content-type': 'text/plain',
                    'origin': 'https://newassets.hcaptcha.com',
                    'referer': 'https://newassets.hcaptcha.com/',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-gpc': '1',
                    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                }
            ).text
            f.write(content)

        embed = DiscordEmbed(
            title=f'New hsw version: {newVersion}',
            description=f'**From**: `{oldVersion}`\n**To**: `{newVersion}`',
            color="03b2f8"
        )
        embed.url = url
        webhook.remove_files(True)
        webhook.add_embed(embed)
        webhook.add_file(content, "hsw.js")
        webhook.execute(True)
    
    def monitor(self):
        while True:
            try:
                version = self.get_hcaptcha_version()
                if version not in self.HcapVersion and self.HswNewVersion != version:
                    self.HcapVersion.append(version)
                    self.HcapOldVersion = self.HcapNewVersion
                    self.HcapNewVersion = version
                    self.sendHcaptchaVersionChange(self.HcapOldVersion,version)
                    print(f'New Hcaptcha Version Detected: {version}')
                    print(f'From {self.HcapOldVersion} to {version}')
                
                version = self.get_hsw_version(version)
                if version not in self.HswVersion and self.HswNewVersion != version:
                    self.HswVersion.append(version)
                    self.HswOldVersion = self.HswNewVersion
                    self.HswNewVersion = version
                    self.sendHswVersionChange(self.HswOldVersion,version)
                    print(f'New Hsw Version Detected: {version}')
                    print(f'From {self.HswOldVersion} to {version}')
                time.sleep(60)
            except Exception as e:
                print(str(e))

if __name__ == "__main__":
    hcaptcha = Hcaptcha()
    hcaptcha.monitor()