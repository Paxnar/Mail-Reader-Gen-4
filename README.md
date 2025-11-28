<p align="center">
  <img src="https://github.com/Paxnar/mailreaderHGSS/blob/main/mails/Heart_Mail.png" alt="icon"/>
</p>
<h1 align="center">Mail Reader</h1>
<p align="center">
  <a href="https://github.com/Paxnar/mailreaderHGSS/releases/latest"><img src="https://img.shields.io/github/v/release/Paxnar/mailreaderHGSS?labelColor=30373D&label=Release&logoColor=959DA5&logo=github&filter=*" alt="release"/></a>
</p>

<!-- For users: [Quick Setup Guide](https://github.com/kuroppoi/entralinked/wiki/Setup) -->

## Usage

1. Run Mail Reader.
1. Click Open Save.
1. Select the Generation IV save.
1. If you have any mail stored in your game's PC, you can scroll the slider to see them.
1. If you want to change the language of the text on the mail, select the desired language. (There are certain issues with this feature on Platinum saves)
1. Click Export to export the selected mail as an image.
1. Click Export All to export all of the mail as images in a desired location.

![image](https://github.com/user-attachments/assets/f402e268-cbde-4bf3-8f1e-511e440745c2)
![image](https://github.com/user-attachments/assets/c420c891-4637-442e-a470-d22a562a3b8d)


## Building

#### Prerequisites

- numpy~=1.23.5
- Pillow~=9.3.0
- PyQt5~=5.15.4

```
pyinstaller --onefile --noconsole main.py
```
