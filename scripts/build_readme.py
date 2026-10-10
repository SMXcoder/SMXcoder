"""Write README.md from config.json."""
import json
c = json.load(open("config.json")); h = c["handle"]
open("README.md", "w").write(f'''<div align="center">

<h3><code>{h}@github ~ $ ./contributions.sh</code></h3>
<img src="./contrib-heatmap.svg" width="860" />

<br><br>

<h3><code>{h}@github ~ $ whoami</code></h3>
<table>
  <tr>
    <td valign="top"><img src="./ascii-banner.svg" width="370" /></td>
    <td valign="top"><img src="./info-card.svg" width="490" /></td>
  </tr>
</table>

</div>
''')
print("wrote README.md")
